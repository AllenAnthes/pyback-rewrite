import pprint


def test_api_message(client):
    response = client.get('/api/botMessages')
    assert response.status_code == 200


def test_thing(client):
    response = client.get("/admin/messages")
    pprint.pprint(response)
