import logging
from functools import lru_cache

from pyback import app

from slackclient import SlackClient

logger = logging.getLogger(__name__)

configs = app.config

VERIFICATION_TOKEN = configs['VERIFICATION_TOKEN']
TOKEN = configs['TOKEN']


class Slack:
    client = SlackClient(TOKEN)

    @classmethod
    def api_call(cls, method, **kwargs):
        result = cls.client.api_call(method, **kwargs)
        logger.info(f'API call method: {method} || Result: {result}')
        return result

    @classmethod
    def post_message(cls, channel, message, **kwargs):
        return cls.api_call('chat.postMessage', channel=channel, username='test2bot', **message, **kwargs)

    @classmethod
    def update_message(cls, **kwargs):
        return cls.api_call('chat.update', **kwargs)

    @classmethod
    def open_dialog(cls, **kwargs):
        return cls.api_call('dialog.open', **kwargs)

    @classmethod
    @lru_cache(64)
    def user_id_from_email(cls, email, fallback=None):
        response = cls.api_call('users.lookupByEmail', email=email)
        if response['ok']:
            user_id = response['user']['id']
            return f'<@{user_id}>'
        else:
            return fallback or 'Slack User'

    @classmethod
    @lru_cache(64)
    def user_name_from_id(cls, user_id: str) -> str:
        response = cls.api_call('users.info', user=user_id)
        logger.debug(f'username from id response: {response}')
        try:
            if response['user']['real_name']:
                return response['user']['real_name'].title()
            elif response['user']['name']:
                return response['user']['name'].title()
        except KeyError as error:
            logging.exception(error)
        else:
            return 'New Member'

    @classmethod
    def user_info_from_id(cls, user_id: str):
        return cls.api_call('users.info', user=user_id)
