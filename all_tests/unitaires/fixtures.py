import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True  # test mode activated
    with app.test_client() as client:
        yield client


class MockData:

    # Données mockées pour remplacer le contenu de "clubs"
    mock_clubs = [
        {"name": "Club 1", "email": "club1@example.com", "points": "10"},
        {"name": "Club 2", "email": "club2@example.com", "points": "0"}
    ]

    # Données mockées pour remplacer le contenu de "clubs"
    mock_competitions = [
        {
            "name": "Competition 1",
            "date": "2030-01-01 13:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Competition 2",
            "date": "2030-01-01 13:00:00",
            "numberOfPlaces": "10"
        },
        {
            "name": "Competition 3",
            "date": "2000-01-01 13:00:00",
            "numberOfPlaces": "10"
        },
        {
            "name": "Competition 4",
            "date": "2030-01-01 13:00:00",
            "numberOfPlaces": "0"
        }
    ]

    # Données mockées pour avoir des données invalide
    invalid_email = "invalid@example.com"
    invalid_club_name = "invalid_club_name"
    invalid_competition_name = "invalid_competition_name"
    invalid_place_required = "invalid_place_required"
