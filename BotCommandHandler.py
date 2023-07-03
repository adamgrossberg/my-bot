from PlayerDatabase import PlayerDatabase
from slack.web.client import WebClient
import os

def handle_message(event: dict, player_database: PlayerDatabase, slack_client: WebClient):
    
    CHANNEL_ID = os.environ['CHANNEL_ID']
    player_table = player_database.players
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

        # Handle different point amounts
        if words[0] == "!recovery":
            for user_id in user_ids:
                player_table.update_one({"_id": user_id}, {"$inc": {"points": 0.5}})
            slack_client.reactions_add(name='person_in_lotus_position', channel=CHANNEL_ID, timestamp=message_timestamp)
        elif words[0] == "!cardio":
            for user_id in user_ids:
                player_table.update_one({"_id": user_id}, {"$inc": {"points": 1}})
            slack_client.reactions_add(name='runner', channel=CHANNEL_ID, timestamp=message_timestamp)
        elif words[0] == "!gym" or words[0] == "!jim":
            for user_id in user_ids:
                player_table.update_one({"_id": user_id}, {"$inc": {"points": 1}})
            slack_client.reactions_add(name='weight_lifter', channel=CHANNEL_ID, timestamp=message_timestamp)
        elif words[0] == "!workout" or words[0] == "!field":
            for user_id in user_ids:
                player_table.update_one({"_id": user_id}, {"$inc": {"points": 1.5}})
            slack_client.reactions_add(name='athletic_shoe', channel=CHANNEL_ID, timestamp=message_timestamp)
        elif words[0] == "!throw":
            if len(words) > 1 and str (words[1]).isnumeric():
                for user_id in user_ids:
                    player_table.update_one({"_id": user_id}, {"$inc": {"minutes": int (words[1])}})
                slack_client.reactions_add(name='flying_disc', channel=CHANNEL_ID, timestamp=message_timestamp)
            else:
                slack_client.reactions_add(name='stopwatch', channel=CHANNEL_ID, timestamp=message_timestamp)
        elif words[0] == "!leaderboard":
            leaderboard_helper('points', player_table, slack_client, CHANNEL_ID)
            slack_client.reactions_add(name='octopus', channel=CHANNEL_ID, timestamp=message_timestamp)
        elif words[0] == "!throwerboard" or words[0] == "!throwboard":
            leaderboard_helper('minutes', player_table, slack_client, CHANNEL_ID)
            slack_client.reactions_add(name='octopus', channel=CHANNEL_ID, timestamp=message_timestamp)
        else:
            slack_client.reactions_add(name='interrobang', channel=CHANNEL_ID, timestamp=message_timestamp)
            

def leaderboard_helper(points_or_minutes: str, player_table, slack_client: WebClient, CHANNEL_ID: str):
    leaderboard_text = ""
    points_dict = {}
    for player in player_table.find():
        points_dict[player['name']] = player[points_or_minutes]
    sorted_leaderboard = sorted(points_dict.items(), key=lambda x: x[1], reverse=True)
    standing = 1
    for player_tuple in sorted_leaderboard:
        leaderboard_text += str (standing) + ") " + player_tuple[0] + ": " + str (player_tuple[1]) + " " + points_or_minutes + "\n"
        standing += 1
    slack_client.chat_postMessage(**{
        'channel': CHANNEL_ID,
        'icon_emoji': ':robot_face:',
        'blocks': [{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': (
                    '*' + points_or_minutes.upper() + " LEADERBOARD:* \n" + leaderboard_text
                )
            }
        }]
    })