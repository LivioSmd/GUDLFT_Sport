from .fixtures import client, MockData
from server import get_club_by_email, loadClubs, clubs, competitions


def test_get_club_from_email_valid(client, mocker):
    """Test que get_club_from_email retourne le club correspondant à l'email."""

    # Mock de la fonction loadClubs
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
