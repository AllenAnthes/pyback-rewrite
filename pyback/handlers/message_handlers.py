from pprint import pprint

import requests
from flask import render_template

from pyback import app

APP_TOKEN = app.config['APP_TOKEN']

def get_messages():
    data = {
        'token': APP_TOKEN,
        'query': 'from:test2bot',
        'count': 100,
        'sort': 'timestamp'
    }
    res = requests.post('https://slack.com/api/search.messages', data=data)

    # TODO
    if not res.ok:
        return None

    matches = res.json()['messages']['matches']
    messages = [{
        'ts': match['ts'],
        'channel': match['channel']['id'],
        'text': match['text']
    } for match in matches]

    return render_template('messages.html', messages=messages)


if __name__ == '__main__':
    get_messages()
