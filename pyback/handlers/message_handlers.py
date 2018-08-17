from datetime import datetime
from functools import lru_cache

import requests
from flask import render_template, url_for, logging

from pyback import app
from pyback.external.slack_client import Slack

APP_TOKEN = app.config['APP_TOKEN']
logger = app.logger

bot_name = Slack.get_bot_name()


def get_messages():
    data = {
        'token': APP_TOKEN,
        'query': f'from:{bot_name}',
        'count': 100,
        'sort': 'timestamp'
    }
    res = requests.post('https://slack.com/api/search.messages', data=data)
    logger.debug(f'API call method: search.messages || Result: {res}')
    res.raise_for_status()

    json_response = res.json()
    matches = json_response['messages']['matches']
    messages = [Message(match['ts'], match['channel']['id'], match['text']) for match in matches]

    return render_template('messages.html', messages=messages)


def delete(ts, channel):
    return Slack.delete_message(ts, channel)


@app.template_filter('timestamp')
def convert_ts(ts):
    return datetime.fromtimestamp(float(ts))


class Message:
    def __init__(self, ts, channel, text):
        self.ts = ts
        self.channel = channel
        self.text = text

    @property
    def channel_name(self):
        return Message.get_channel_name(self.channel)

    @property
    def delete_url(self):
        return url_for('delete_message', ts=self.ts, channel=self.channel)

    @classmethod
    @lru_cache(64)
    def get_channel_name(cls, channel):
        response = Slack.api_call('conversations.info', channel=channel)
        if response['ok']:
            channel = response['channel']
            if 'name' in channel:
                return response['channel']['name']
            elif channel['is_im']:
                return Slack.user_name_from_id(channel['user'])
            else:
                return channel
        else:
            return channel
