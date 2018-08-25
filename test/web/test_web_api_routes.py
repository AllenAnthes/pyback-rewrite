from flask import url_for
import pytest

from pyback.web.api_routes import get_messages, get_logs_dict, delete
from pyback.web import api_routes


@pytest.fixture
def get_messages(mocker):
    return mocker.patch.object(api_routes, 'get_messages', return_value=['messages'])


@pytest.fixture
def get_logs_dict(mocker):
    return mocker.patch.object(api_routes, 'get_logs_dict', return_value=['logs'])


@pytest.fixture
def delete(mocker):
    return mocker.patch.object(api_routes, 'delete', return_value={'ok': True})


def test_api_message_url_works(client, get_messages):
    response = client.get(url_for('web.api_messages'))
    assert response.status_code == 200


def test_api_message_has_data_payload(client, get_messages):
    """
    Required to work with jQuery Datatables api
    """
    response = client.get(url_for('web.api_messages'))

    assert response.status_code == 200
    assert 'data' in response.json


def test_api_logs_url_works(client, get_logs_dict):
    response = client.get(url_for('web.api_logs'))
    assert response.status_code == 200


def test_api_logs_has_data_payload(client, get_logs_dict):
    """
    Required to work with jQuery Datatables api
    """
    response = client.get(url_for('web.api_logs'))

    assert response.status_code == 200
    assert 'data' in response.json


def test_delete_message_url_works(client, delete):
    response = client.get(url_for('web.delete_message', channel='channel', ts='123'))
    assert response.status_code == 200
