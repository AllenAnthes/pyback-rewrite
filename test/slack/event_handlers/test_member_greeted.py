import pytest

from pyback.slack.event_handlers import member_greeted, slack_client
from pyback.slack import event_handlers
from pyback.slack.event_handlers import greeted_response, not_greeted_response, reset_greet_message

# My god this is so ugly...but it's how slack formats their attachments
claim_button_name = not_greeted_response()[0]['actions'][0]['name']


@pytest.fixture
def slack_client(mocker):
    return mocker.patch.object(event_handlers, slack_client.__name__)


@pytest.fixture
def args():
    return {
        'user': {'id': '123'},
        'actions': [{'value': claim_button_name}],
        'original_message': {'text': 'original text'},
        'channel': {'id': 'community channel'},
        'message_ts': '111222333444',
    }


def test_updates_original_message(mocker, slack_client, args):
    member_greeted(**args)

    assert slack_client.update_message.called


def test_greeted_response_called_when_greeted(mocker, slack_client, args):
    spy = mocker.spy(event_handlers, greeted_response.__name__)

    member_greeted(**args)

    assert spy.called


def test_not_greeted_response_called_when_not_greeted(mocker, slack_client, args):
    spy = mocker.spy(event_handlers, not_greeted_response.__name__)
    args['actions'][0]['value'] = 'Something else'

    member_greeted(**args)

    assert spy.called

def test_new_member_resets_greet_message_when_needed(mocker, slack_client, args):
    spy = mocker.spy(event_handlers, reset_greet_message.__name__)
    args['actions'][0]['value'] = 'reset_greet'

    member_greeted(**args)

    assert spy.called