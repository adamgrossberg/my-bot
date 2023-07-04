import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from TribeDatabase import *
from MessageHandler import handle_message
from SlashCommandHandler import handle_slash_command
import threading

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)

slack_client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = slack_client.api_call('auth.test')['user_id']
DATABASE = Database(os.environ['DATABASE_URI'])
PLAYER_TABLE = DATABASE.players
CHANNEL_NAME = os.environ['CHANNEL_NAME']
CHANNEL_ID = os.environ['CHANNEL_ID']

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    if BOT_ID != event.get('user'):
        thread = threading.Thread(
                target=handle_message,
                args=(event, DATABASE, slack_client)
            )
        thread.start()

@app.route('/initialize-roster', methods=['POST'])
def initialize_roster():
    thread = threading.Thread(
        target=handle_slash_command,
        args=('initialize-roster', DATABASE, slack_client)
    )
    thread.start()
    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True)
