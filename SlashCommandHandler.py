from TribeDatabase import Database
from slack.web.client import WebClient
import os

def handle_slash_command(command_name: str, database: Database, slack_client: WebClient):
    if command_name == 'initialize-roster':
        channel_id = os.environ['CHANNEL_ID']
        BOT_ID = slack_client.api_call('auth.test')['user_id']
        player_ids = slack_client.conversations_members(channel=channel_id).get('members')
        database.delete_all_players()
        database.insert_many_players({
            'id': id,
            'name': slack_client.users_info(user=id).get('user')['real_name'],
            'team': None
        } for id in player_ids)
        database.delete_player(BOT_ID)
        slack_client.chat_postMessage(channel=channel_id, text=f"Roster initialized.", icon_emoji=':robot_face:')