import logging
from functools import lru_cache

import requests

logger = logging.getLogger('slack_client')


class SlackClient:
    def __init__(self, app=None, token=None, channels=None):
        self.token = token
        self.channels = channels

        if app is not None and token is not None:
            self.init_app(app, token)

    def init_app(self, app, token, channels=None):
        self.token = token
        self.channels = channels

        app.extensions['slack_client'] = self

    def _api_call(self, method, **kwargs):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        url = f'https://slack.com/api/{method}'

        return requests.post(url, headers=headers, data=kwargs).json()

    def api_call(self, method, **kwargs):
        result = self._api_call(method, **kwargs)
        logger.debug(f'API call method: {method} || Result: {result}')
        return result

    def post_message(self, channel, message, **kwargs):
        return self.api_call('chat.postMessage', channel=channel, username='test2bot', **message, **kwargs)

    def update_message(self, **kwargs):
        return self.api_call('chat.update', **kwargs)

    def delete_message(self, ts, channel):
        return self.api_call('chat.delete', ts=ts, channel=channel)

    def open_dialog(self, **kwargs):
        return self.api_call('dialog.open', **kwargs)

    @lru_cache(64)
    def user_id_from_email(cls, email, fallback=None):
        response = cls.api_call('users.lookupByEmail', email=email)
        if response['ok']:
            user_id = response['user']['id']
            return f'<@{user_id}>'
        else:
            return fallback or 'Slack User'

    @lru_cache(64)
    def user_name_from_id(self, user_id: str) -> str:
        response = self.api_call('users.info', user=user_id)
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

    def user_info_from_id(self, user_id: str):
        return self.api_call('users.info', user=user_id)

    @lru_cache(4)
    def get_bot_name(self):
        res = self.api_call('auth.test')
        return res['user']
