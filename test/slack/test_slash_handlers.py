import pytest

from pyback.slack import slash_handlers
from pyback.slack.slash_handlers import slash_here

"""
**NOTE  Although it isn't called client needs
to be passed into these calls in order to instantiate
the context
"""


@pytest.fixture
def mock_slack(mocker):
    return mocker.patch.object(slash_handlers, 'slack_client')


@pytest.fixture
def can_here(mocker):
    return mocker.patch.object(slash_handlers, 'can_here')


def test_slash_here_returns_200(client, mock_slack, can_here):
    res = slash_here('channel', 'text', 'slack_id')

    assert res.status_code == 200


def test_slash_here_returns_not_authorized_correctly(client, mock_slack, can_here):
    can_here.return_value = False

    res = slash_here('channel', 'text', 'slack_id')
    assert res.status_code == 200
    assert 'not authorized' in str(res.data)
    assert not mock_slack.called
