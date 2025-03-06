import copy
from .fixtures import client, MockData
from server import competitions, get_competition, manage_over_competitions, manage_competition_places_in_db


def test_loadCompetitions(client):
    """Test that the competitions are loaded correctly at the start of the application."""
    assert competitions is not None
    assert len(competitions) != 0


def test_get_competition(client, mocker):
    """Test that the get_competition function returns the corresponding competition."""
    # Mock competitions variable
    mocker.patch("server.competitions", copy.deepcopy(MockData.mock_competitions))

    competition = get_competition(copy.deepcopy(MockData.mock_competitions[0]["name"]))

    assert competition is not None
    assert competition["name"] == "Competition 1"


def test_not_get_competition(client, mocker):
    """Test that the get_competition function returns None if no name matches."""
    mocker.patch("server.competitions", copy.deepcopy(MockData.mock_competitions))

    competition = get_competition(copy.deepcopy(MockData.invalid_competition_name))

    assert competition is None


def test_get_over_competitions_list(client):
    """manage_over_competitions should return a list of competitions that are over."""
    over_competitions = manage_over_competitions(copy.deepcopy(MockData.mock_competitions))

    assert over_competitions is not None
    assert len(over_competitions) == 1
    assert over_competitions[0]["name"] == "Competition 3"


def test_manage_competition_places_in_db(client):
    """manage_competition_places_in_db should update the competition places in the database."""
    competition = competitions[0]
    competition["numberOfPlaces"] = 100
    manage_competition_places_in_db(competition)

    assert competitions[0]["numberOfPlaces"] == '100'
