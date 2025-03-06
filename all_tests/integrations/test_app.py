from .fixtures import client


def test_should_start_app(client):
    """Test that the application starts correctly."""
    # Simulates a GET request on the home page
    response = client.get('/')

    # Check that the status code is 200
    assert response.status_code == 200