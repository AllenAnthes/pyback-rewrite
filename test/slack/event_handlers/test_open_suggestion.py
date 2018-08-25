import pytest

from pyback.slack import event_handlers
from pyback.slack.event_handlers import open_suggestion


@pytest.fixture
def slack_client(mocker):
    return mocker.patch.object(event_handlers, 'slack_client')


def test_open_dialog_requested(slack_client):

    open_suggestion(trigger_id='112233')

    assert slack_client.open_dialog.called