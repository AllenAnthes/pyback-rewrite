from typing import Dict, List

from slack.methods import Methods
from functools import lru_cache
from flask import url_for, current_app
import requests
from werkzeug.local import LocalProxy

from pyback import slack_client as slack

APP_TOKEN = LocalProxy(lambda: current_app.config['APP_TOKEN'])
logger = LocalProxy(lambda: current_app.logger)


class Message:
    def __init__(self, ts, channel, text):
        self.ts = ts
        self.channel = channel
        self.text = text

    @property
    def channel_name(self) -> str:
        return Message.get_channel_name(self.channel)

    @property
    def delete_url(self) -> str:
        return url_for('web.delete_message', ts=self.ts, channel=self.channel)

    @classmethod
    @lru_cache(64)
    def get_channel_name(cls, channel: str) -> str:
        response = slack.api_call(Methods.CONVERSATIONS_INFO, channel=channel)
        if response['ok']:
            channel = response['channel']
            if 'name' in channel:
                return response['channel']['name']
            elif channel['is_im']:
                return slack.user_name_from_id(channel['user'])
            else:
                return channel
        else:
            return channel

    def serialize(self) -> Dict[str, str]:
        return {
            'ts': self.ts,
            'channel': self.channel,
            'text': self.text,
            'delete_url': self.delete_url,
        }


def get_messages() -> List[Dict[str, str]]:
    bot_name = slack.bot_name

    data = {
        'token': str(APP_TOKEN),
        'query': f'from:{bot_name}',
        'count': 100,
        'sort': 'timestamp'
    }
    json_response = _call_slack_api(data)
    matches = json_response['messages']['matches']
    messages = [Message(match['ts'], match['channel']['id'], match['text']).serialize() for match in matches]
    return messages


def _call_slack_api(data):
    res = requests.post('https://slack.com/api/search.messages', data=data)
    logger.debug(f'API call method: search.messages || Result: {res.status_code}')
    res.raise_for_status()

    return res.json()


def delete(ts: str, channel: str):
    return slack.delete_message(ts, channel)
