import pytest

from pyback.slack import event_handlers


@pytest.fixture
def slack_client(mocker):
    return mocker.patch.object(event_handlers, 'slack_client')
