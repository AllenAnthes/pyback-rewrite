import pytest

from pyback.slack.event_handlers import new_member
from pyback.slack import event_handlers


@pytest.fixture
def slack_client(mocker, app):
    slack_client = mocker.patch.object(event_handlers, 'slack_client')
    slack_client.channels = {'community': app.config['COMMUNITY_CHANNEL']}
    return slack_client


@pytest.fixture
def user():
    return {'id': '123'}


def test_new_member_gets_user_name(slack_client, user):
    new_member(user)
    assert slack_client.user_name_from_id.called


def test_new_member_posts_to_slack(slack_client, user):
    new_member(user)

    assert 4 == slack_client.post_message.call_count


def test_new_member_sends_message_to_user(slack_client, user):
    new_member(user)

    calls = slack_client.post_message.call_args_list
    for call in calls:
        channel = call[1]['channel']
        if channel == user['id']:
            break
    else:
        assert False


def test_new_member_sends_message_to_community_channel(slack_client, user):
    community_channel = slack_client.channels['community']

    new_member(user)

    calls = slack_client.post_message.call_args_list
    for call in calls:
        channel = call[1]['channel']
        if channel == community_channel:
            break
    else:
        assert False
