import copy
from .fixtures import client, MockData
from server import get_club_by_email, loadClubs, clubs, get_club, manage_club_points_in_db


def test_get_club_from_email_valid(client, mocker):
    """Test that get_club_from_email return the club corresponding to the email"""
    # Mock clubs variable
    mocker.patch("server.clubs", copy.deepcopy(MockData.mock_clubs))

    # call get_club_by_email function
    club = get_club_by_email(copy.deepcopy(MockData.mock_clubs[0]["email"]))

    # check the club returned
    assert club is not None
    assert club["name"] == "Club 1"


def test_get_club_from_email_invalid(client, mocker):
    """Test that get_club_from_email return None if the email is not found."""
    # Mock loadClubs function
    mocker.patch("server.clubs", copy.deepcopy(MockData.mock_clubs))

    club = get_club_by_email(copy.deepcopy(MockData.invalid_email))

    assert club is None


def test_loadClubs(client):
    """Test that the clubs are loaded correctly at the start of the application."""
    assert clubs is not None
    assert len(clubs) != 0


def test_get_club(client, mocker):
    """Test that the get_club function returns the corresponding club."""
    mocker.patch("server.clubs", copy.deepcopy(MockData.mock_clubs))

    club = get_club(copy.deepcopy(MockData.mock_clubs[0]["name"]))

    assert club is not None
    assert club["name"] == "Club 1"


def test_manage_club_points_in_db(client):
    """manage_club_points_in_db should update the club points in the database."""
    club = clubs[0]
    club["points"] = 10
    manage_club_points_in_db(club)

    assert clubs[0]["points"] == '10'


def test_not_get_club(client, mocker):
    """Test that the get_club function returns None if no name matches."""
    mocker.patch("server.clubs", copy.deepcopy(MockData.mock_clubs))

    club = get_club(copy.deepcopy(MockData.invalid_club_name))

    assert club is None
