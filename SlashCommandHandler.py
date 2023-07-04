from PlayerDatabase import PlayerDatabase
from slack.web.client import WebClient
import os

def handle_slash_command(command_name: str, player_database: PlayerDatabase, slack_client: WebClient):
    if command_name == 'initialize-roster':
        player_table = player_database.players
        channel_id = os.environ['CHANNEL_ID']
        BOT_ID = slack_client.api_call('auth.test')['user_id']
        player_ids = slack_client.conversations_members(channel=channel_id).get('members')
        player_table.delete_many({})
        player_database.insert_many_players({
            'id': id,
            'name': slack_client.users_info(user=id).get('user')['real_name'],
            'team': None
        } for id in player_ids)
        player_table.delete_one({"_id": BOT_ID})
        slack_client.chat_postMessage(channel=channel_id, text=f"Roster initialized.", icon_emoji=':robot_face:')