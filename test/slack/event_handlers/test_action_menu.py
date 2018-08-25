import pytest

from pyback.slack import event_handlers
from pyback.slack.event_handlers import action_menu


@pytest.fixture
def slack_client(mocker):
    return mocker.patch.object(event_handlers, slack_client.__name__)


@pytest.fixture
def args():
    return {
        'actions': [
            {'name': 'slack'}
        ],
        'channel': {
            'id': '123'
        },
        'message_ts': '111222333'
    }


def test_updates_message(slack_client, args):
    action_menu(**args)

    assert slack_client.update_message.called


@pytest.mark.parametrize('action_type', ['slack', 'python', 'mentor', 'javascript', 'ruby'])
def test_handler_works_for_all_choices(slack_client, args, action_type):
    args['actions'][0]['name'] = action_type

    action_menu(**args)

    assert slack_client.update_message.called
