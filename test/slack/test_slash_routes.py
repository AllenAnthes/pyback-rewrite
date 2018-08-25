from flask import url_for, make_response


def test_here_works_with_post(app, mocker, client):
    data = {
        'channel_id': 'abc23',
        'text': 'Some text',
        'user_id': 'U123',
        'token': app.config['VERIFICATION_TOKEN']
    }

    mocker.patch('pyback.slack.slash_routes.slash_here', return_value=make_response('', 200))

    response = client.post(url_for('slack.here'), data=data,
                           content_type='application/x-www-form-urlencoded')
    assert 200 == response.status_code


def test_here_fails_with_get(client):
    response = client.get(url_for('slack.here'))
    assert response.status_code == 405


def _test_here_fails_with_invalid_token(client):
    data = {
        'channel_id': 'abc23',
        'text': 'Some text',
        'user_id': 'U123',
        'token': 'bad_token'
    }

    response = client.post(url_for('slack.here'), data=data,
                           content_type='application/x-www-form-urlencoded')

    assert 403 == response.status_code


def test_logs_works_with_post(app, client):
    data = {'token': app.config['VERIFICATION_TOKEN']}

    response = client.post(url_for('slack.get_logs'), data=data, )

    assert 200 == response.status_code


def test_logs_fails_with_get(client):
    response = client.get(url_for('slack.get_logs'))
    assert response.status_code == 405


def _test_logs_fails_with_invalid_token(client):
    data = {'token': 'bad_token'}

    response = client.post(url_for('slack.get_logs'), data=data,
                           content_type='application/x-www-form-urlencoded')
    assert 403 == response.status_code
