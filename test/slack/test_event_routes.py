from flask import url_for
import pytest
import json

from pyback.slack.event_routes import route_request
from pyback.slack import event_routes


@pytest.fixture
def router(mocker):
    return mocker.patch.object(event_routes, route_request.__name__)


def test_slack_event_redirects_on_missing_token(client):
    res = client.post(url_for('slack.slack_event'),
                      content_type='application/json')

    assert res.status_code == 400


def test_slack_event_denies_on_invalid_token(client):
    data = {
        'type': 'event'
    }
    res = client.post(url_for('slack.slack_event'),
                      data=json.dumps(data),
                      content_type='application/json')

    assert 403 == res.status_code


def test_slack_event_returns_200(app, client, router):
    data = {
        'type': 'event',
        'event': {},
        'token': app.config['VERIFICATION_TOKEN']
    }

    res = client.post(url_for('slack.slack_event'),
                      data=json.dumps(data),
                      content_type='application/json')

    assert 200 == res.status_code


def test_slack_event_routes_request(app, client, router):
    data = {
        'type': 'event',
        'event': {},
        'token': app.config['VERIFICATION_TOKEN']
    }

    res = client.post(url_for('slack.slack_event'),
                      data=json.dumps(data),
                      content_type='application/json')

    assert 200 == res.status_code
    assert router.called


def test_slack_event_returns_challenge_token(app, client):
    data = {
        'type': 'url_verification',
        'challenge': 'test_challenge'
    }

    res = client.post(url_for('slack.slack_event'),
                      data=json.dumps(data),
                      content_type='application/json')

    assert 'test_challenge' in str(res.data)


def test_slack_interaction_denies_on_invalid_token(client):
    data = {
        'type': 'event'
    }
    json_data = json.dumps(data)

    res = client.post(url_for('slack.slack_interaction'),
                      data=dict(payload=json_data),
                      content_type='application/x-www-form-urlencoded')

    assert 403 == res.status_code


def test_slack_interaction_returns_200(mocker, app, client, router):
    """
    I honestly don't know why we have to convert this from a dict
    to json back to a dict but it's the only way I can get it to
    read it correctly as form data.
    """
    data = {
        'type': 'event',
        'event': '',
        'token': app.config['VERIFICATION_TOKEN']
    }
    json_data = json.dumps(data)

    res = client.post(url_for('slack.slack_interaction'),
                      data=dict(payload=json_data),
                      content_type='application/x-www-form-urlencoded')

    assert 200 == res.status_code


def test_slack_interaction_routes_request(mocker, app, client, router):
    data = {
        'type': 'event',
        'event': '',
        'token': app.config['VERIFICATION_TOKEN']
    }
    json_data = json.dumps(data)

    res = client.post(url_for('slack.slack_interaction'),
                      data=dict(payload=json_data),
                      content_type='application/x-www-form-urlencoded')

    assert 200 == res.status_code
    assert router.called
