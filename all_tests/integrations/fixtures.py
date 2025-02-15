import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True  # test mode activated
    with app.test_client() as client:
        yield client


class MockData:

    # Données mockées pour remplacer le contenu de `clubs`
    mock_clubs = [
        {"name": "Club 1", "email": "club1@example.com"},
        {"name": "Club 2", "email": "club2@example.com"}
    ]
