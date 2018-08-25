from functools import lru_cache
import requests
import logging

from slack import methods
from slack.io.requests import SlackAPI

logger = logging.getLogger('slack_client')
session = requests.session()


class SlackClient:
    def __init__(self, app=None, token=None, channels=None, other_keys=None):
        self.token = token
        self.channels = channels
        self.other_keys = other_keys
        self.client = None

        if app is not None and token is not None:
            self.init_app(app, token)

    def init_app(self, app, token, channels=None, other_keys=None):
        self.token = token
        self.channels = channels
        self.client = SlackAPI(token=token, session=session)
        self.other_keys = other_keys

        app.extensions['slack_client'] = self

    def _api_call(self, method, **kwargs):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        url = f'https://slack.com/api/{method}'

        return requests.post(url, headers=headers, data=kwargs).json()

    def api_call(self, method, **kwargs):
        if type(method) is methods:
            result = self.client.query(method, data=kwargs)
        else:
            result = self._api_call(method, **kwargs)

        logger.debug(f'API call method: {method} || Result: {result}')
        return result

    def post_message(self, channel, message, **kwargs):
        if 'as_user' not in kwargs:
            kwargs['as_user'] = True
            kwargs['username'] = self.bot_name

        return self.api_call(methods.CHAT_POST_MESSAGE, channel=channel, **message, **kwargs)

    def update_message(self, **kwargs):
        return self.api_call(methods.CHAT_UPDATE, **kwargs)

    def delete_message(self, ts: str, channel: str) -> dict:
        return self.api_call(methods.CHAT_DELET, ts=ts, channel=channel)

    def open_dialog(self, **kwargs):
        return self.api_call(methods.DIALOG_OPEN, **kwargs)

    @lru_cache(64)
    def user_id_from_email(self, email, fallback=None):
        response = self._api_call('users.lookupByEmail', email=email)
        if response['ok']:
            user_id = response['user']['id']
            return f'<@{user_id}>'
        else:
            return fallback or 'Slack User'

    @lru_cache(64)
    def user_name_from_id(self, user_id: str) -> str:
        response = self.api_call(methods.USERS_INFO, user=user_id)
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
        return self.api_call(methods.USERS_INFO, user=user_id)

    @property
    @lru_cache(4)
    def bot_name(self):
        res = self.api_call(methods.AUTH_TEST)
        return res['user']
