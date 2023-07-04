from PlayerDatabase import *
from slack.web.client import WebClient
import os
from enum import Enum

def handle_message(event: dict, player_database: PlayerDatabase, slack_client: WebClient):
    activities = {
        '!recovery': (0.5, 'person_in_lotus_pose'),
        '!cardio': (1, 'runner'),
        '!gym': (1, 'weight_lifter'),
        '!jim': (1, 'weight_lifter'),
        '!workout': (1.5, 'athletic_shoe'),
        '!field': (1.5, 'athletic_shoe')
    }
    CHANNEL_ID = os.environ['CHANNEL_ID']
    player_table = player_database.players
    # team_table = player_database.teams
    message_timestamp = event.get('ts')
    text = event.get('text')
    words = text.split()


    if words[0][0] == "!":
        user_ids = {event.get('user')}
        # Determine if anyone was mentioned in the message
        rich_text_elements = event.get('blocks')[0].get('elements')[0].get('elements')
        for text_element in rich_text_elements:
            if text_element.get('type') == 'user':
                user_ids.add(text_element.get('user_id'))
        # Handle different commands
        if words[0] == "!throw":
            if len(words) > 1 and str (words[1]).isnumeric():
                for user_id in user_ids:
                    player_table.update_one({"_id": user_id}, {"$inc": {"minutes": int (words[1])}})
                slack_client.reactions_add(name='flying_disc', channel=CHANNEL_ID, timestamp=message_timestamp)
            else:
                slack_client.reactions_add(name='stopwatch', channel=CHANNEL_ID, timestamp=message_timestamp)
        elif words[0] == "!leaderboard" or words[0] == "!throwerboard" or words[0] == "!throwboard":
            leaderboard_helper('points' if words[0] == "!leaderboard" else 'minutes', player_database, slack_client, CHANNEL_ID)
            slack_client.reactions_add(name='octopus', channel=CHANNEL_ID, timestamp=message_timestamp)
        else:
            activity_result = activities.get(words[0], None)
            if activity_result != None:
                for user_id in user_ids:
                    player_table.update_one({"_id": user_id}, {"$inc": {"points": activity_result[0]}})
                slack_client.reactions_add(name=activity_result[1], channel=CHANNEL_ID, timestamp=message_timestamp)
            else:
                slack_client.reactions_add(name='interrobang', channel=CHANNEL_ID, timestamp=message_timestamp)
            
# Helper method to build and send the leaderboard or throwerboard message
def leaderboard_helper(points_or_minutes: str, player_database: PlayerDatabase, slack_client: WebClient, CHANNEL_ID: str):
    player_table = player_database.players
    leaderboard_text = ""
    points_dict = {}
    for player in player_table.find():
        points_dict[player['name']] = player[points_or_minutes]
    sorted_leaderboard = sorted(points_dict.items(), key=lambda x: x[1], reverse=True)
    standing = 1
    for player_tuple in sorted_leaderboard:
        leaderboard_text += str (standing) + ") " + player_tuple[0] + ": " + str (player_tuple[1]) + " " + points_or_minutes + "\n"
        standing += 1
    slack_client.chat_postMessage(
        channel=CHANNEL_ID,
        icon_emoji=':robot_face:',
        blocks=[{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': (
                    '*' + points_or_minutes.upper() + " LEADERBOARD:* \n" + leaderboard_text
                )
            }
        }]
    )