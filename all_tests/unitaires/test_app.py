from .fixtures import client, MockData
from server import (get_club_by_email, loadClubs, clubs, competitions, get_competition, get_club, get_place_required,
                    manage_over_competitions)


def test_get_club_from_email_valid(client, mocker):
    """Test que get_club_from_email retourne le club correspondant à l'email."""

    # Mock de la variable clubs
    mocker.patch("server.clubs", MockData.mock_clubs)

    # appel de la fonction get_club_by_email
    club = get_club_by_email(MockData.mock_clubs[0]["email"])

    # Verification du club retourné
    assert club is not None
    assert club["name"] == "Club 1"


def test_get_club_from_email_invalid(client, mocker):
    """Test que get_club_from_email retourne None si l'email n'est pas trouvé."""

    # Mock de la fonction loadClubs
    mocker.patch("server.clubs", MockData.mock_clubs)

    club = get_club_by_email(MockData.invalid_email)

    assert club is None


def test_loadClubs(client):
    """Test que les clubs sont chargés correctement au demarrage de l'application."""
    assert clubs is not None
    assert len(clubs) != 0


def test_loadClubs_test(client, monkeypatch):
    """Test que les clubs sont chargés correctement au demarrage de l'application."""
    assert clubs is not None
    assert len(clubs) != 0


def test_loadCompetitions(client):
    """Test que les compétitions sont chargées correctement au demarrage de l'application."""
    assert competitions is not None
    assert len(competitions) != 0


def test_get_competition(client, mocker):
    """Test que la fonction get_competition retourne la compétition correspondante."""

    # Mock de la variable competitions
    mocker.patch("server.competitions", MockData.mock_competitions)

    competition = get_competition(MockData.mock_competitions[0]["name"])

    assert competition is not None
    assert competition["name"] == "Competition 1"


def test_not_get_competition(client, mocker):
    """Test que la fonction get_competition retourne none si aucune nom ne correspond."""

    # Mock de la variable competitions
    mocker.patch("server.competitions", MockData.mock_competitions)

    competition = get_competition(MockData.invalid_competition_name)

    assert competition is None


def test_get_club(client, mocker):
    """Test que la fonction get_club retourne le club correspondante."""

    # Mock de la variable clubs
    mocker.patch("server.clubs", MockData.mock_clubs)

    club = get_club(MockData.mock_clubs[0]["name"])

    assert club is not None
    assert club["name"] == "Club 1"


def test_not_get_club(client, mocker):
    """Test que la fonction get_club retourne le club correspondante."""

    # Mock de la variable clubs
    mocker.patch("server.clubs", MockData.mock_clubs)

    club = get_club(MockData.invalid_club_name)

    assert club is None


def test_get_place_required(client):
    """Test que la fonction get_place_required retourne les places requises."""

    place_required = get_place_required(10)

    assert place_required is not None
    assert place_required == 10
    assert isinstance(place_required, int)  # place_required should be an integer


def test_not_get_place_required(client):
    """Test que la fonction get_place_required retourne les places requises."""

    place_required = get_place_required(MockData.invalid_place_required)

    assert place_required is not None
    assert place_required == 0
    assert isinstance(place_required, int)  # place_required should be an integer


def test_get_over_competitions_list(client):
    """manage_over_competitions should return a list of competitions that are over."""

    over_competitions = manage_over_competitions(MockData.mock_competitions)

    assert over_competitions is not None
    assert len(over_competitions) == 1
    assert over_competitions[0]["name"] == "Competition 3"
