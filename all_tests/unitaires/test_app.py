from .fixtures import client


def test_should_start_app(client):
    """
    should status code 200
    """
    response = client.get('/')
    assert response.status_code == 200
