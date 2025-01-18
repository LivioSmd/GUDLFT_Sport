import pytest
from ...server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True  # test mode activated
    with app.test_client() as client:
        yield client
