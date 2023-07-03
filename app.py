import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from PlayerDatabase import *
from BotCommandHandler import handle_message
import threading

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)

SLACK_CLIENT = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = SLACK_CLIENT.api_call('auth.test')['user_id']
DATABASE = PlayerDatabase(os.environ['DATABASE_URI'])
PLAYER_TABLE = DATABASE.players
CHANNEL_NAME = os.environ['CHANNEL_NAME']
CHANNEL_ID = os.environ['CHANNEL_ID']

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    if BOT_ID != event.get('user'):
        x = threading.Thread(
                target=handle_message,
                args=(event, DATABASE, SLACK_CLIENT)
            )
        x.start()

@app.route('/initialize-roster', methods=['POST'])
def initialize_roster():
    player_ids = SLACK_CLIENT.conversations_members(channel=CHANNEL_ID).get('members')
    PLAYER_TABLE.delete_many({})
    PLAYER_TABLE.insert_many({
        "_id": id,
        "name": SLACK_CLIENT.users_info(user=id).get('user')['real_name'],
        "points": 0,
        "minutes": 0,
        "team": None
    } for id in player_ids)
    PLAYER_TABLE.delete_one({"_id": BOT_ID})
    SLACK_CLIENT.chat_postMessage(channel=CHANNEL_NAME, text=f"Roster initialized.", icon_emoji=':robot_face:')
    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True)
