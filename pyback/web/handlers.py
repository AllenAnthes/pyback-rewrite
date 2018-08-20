from functools import lru_cache
from os import path, remove
from urllib import parse

import requests
from flask import url_for, current_app as app, json, jsonify, after_this_request, request, send_file
from werkzeug.local import LocalProxy
from werkzeug.utils import secure_filename

from pyback import slack_client as slack

logger = LocalProxy(lambda: app.logger)
APP_TOKEN = LocalProxy(lambda: app.config['APP_TOKEN'])


def get_logs_dict():
    f = open(f'logs/log.log')
    return [dictify_log(*line.split(" -- ")) for line in f.readlines()]


def get_messages():
    bot_name = slack.get_bot_name()

    data = {
        'token': str(APP_TOKEN),
        'query': f'from:{bot_name}',
        'count': 100,
        'sort': 'timestamp'
    }
    res = requests.post('https://slack.com/api/search.messages', data=data)
    logger.debug(f'API call method: search.messages || Result: {res.status_code}')
    res.raise_for_status()

    json_response = res.json()
    matches = json_response['messages']['matches']
    messages = [Message(match['ts'], match['channel']['id'], match['text']).serialize() for match in matches]
    return messages


def delete(ts, channel):
    return slack.delete_message(ts, channel)


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
        return url_for('web.delete_message', ts=self.ts, channel=self.channel)

    @classmethod
    @lru_cache(64)
    def get_channel_name(cls, channel):
        response = slack.api_call('conversations.info', channel=channel)
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

    def serialize(self):
        return {
            'ts': self.ts,
            'channel': self.channel,
            'text': self.text,
            'delete_url': self.delete_url,
        }


def dictify_log(timestamp, level, message):
    return {
        'timestamp': timestamp,
        'level': level,
        'message': message
    }


def handle_submission(form):
    save_logo(form.logo.data)
    url = f"https://api.github.com/repos/{app.config['GITHUB_REPO_PATH']}/issues"
    headers = {"Authorization": f"Bearer {app.config['GITHUB_JWT']}"}

    params = make_params(**form.data)
    res = requests.post(url, headers=headers, data=json.dumps(params))

    if res.ok:
        return jsonify({'redirect': f'https://github.com/{repo_path}/issues'})
    else:
        return res.reason


def save_logo(file):
    filename = secure_filename(file.filename)
    filepath = path.join(app.static_folder, 'logos', filename)
    file.save(filepath)


def get_logo_and_users(logo):
    school_logo = parse.quote(secure_filename(logo.filename))
    if app.configs['ENV'] == 'development':
        # users = '@wimo7083 @AllenAnthes,'
        users = '@AllenAnthes,'
        logo_url = f'https://pybot.ngrok.io/static/logos/{school_logo}'
        return logo_url, users
    else:
        url_root = request.url_root
        # users = '@hpjaj @wimo7083 @jhampton @kylemh @davidmolina @nellshamrell @hollomancer @maggi-oc'
        users = ''
        logo_url = f'{url_root}static/logos/{school_logo}'
        return logo_url, users


def get_logo(filename):
    filepath = path.join(app.static_folder, 'logos', filename)
    file_handle = open(path.normpath(filepath), 'r')

    @after_this_request
    def remove_file(response):
        try:
            remove(filepath)
            file_handle.close()
        except Exception as error:
            logger.exception("Error removing or closing downloaded file handle", error)
        return response

    return send_file(filepath)


def make_params(logo, name, url, address1, city, state, zipcode, country, rep_name, rep_email, csrf_token, recaptcha,
                address2=None, fulltime=False, hardware=False, has_online=False, only_online=False, accredited=False,
                housing=False, mooc=False):
    logo_url, notify_users = get_logo_and_users(logo)

    return ({
        'title': f'New Code School Request: {name}',
        'body': (
            f"Name: {name}\n"
            f"Website: {url}\n"
            f"Full Time: {fulltime}\n"
            f"Hardware Included: {hardware}\n"
            f"Has Online: {has_online}\n"
            f"Only Online: {only_online}\n"
            f"VA Accredited: {accredited}\n"
            f"Housing Included: {housing}\n"
            f"MOOC Only: {mooc}\n"

            f"Address: {address1} {address2}\n"
            f"City: {city}\n"
            f"State: {state}\n"
            f"Country: {country}\n"
            f"Zip: {zipcode}\n\n"
            f"Representative Name: {rep_name}\n"
            f"Representative Email: {rep_email}\n"

            f"logo: ![school-logo]({logo_url})\n"

            'This code school is ready to be added/updated:\n'
            f"{notify_users}\n"
            "Please close this issue once you've added/updated the code school."
        )
    })
