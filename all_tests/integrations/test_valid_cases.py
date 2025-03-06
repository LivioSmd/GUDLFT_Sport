import copy
from .fixtures import client, MockData


def test_should_valid_email(client, mocker):
    """Test that the application redirects to the welcome page if the email is valid."""
    # Mock loadClubs function
    mocker.patch("server.clubs", copy.deepcopy(MockData.mock_clubs))  # deepcopy for get a copy of the list

    # Simulates a POST request with a valid email
    response = client.post('/showSummary', data={'email': 'club1@example.com'})

    # Check that the redirection and the status code are correct
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Check for the presence of the word “Welcome” in the page content


def test_should_valid_purchase_places(client, mocker):
    """Test that we can book places in a competition."""
    # Mock functions
    mocker.patch("server.clubs", copy.deepcopy(MockData.mock_clubs))
    mocker.patch("server.competitions", copy.deepcopy(MockData.mock_competitions))

    # Mock functions that writes to the json file so that it does nothing
    mocker.patch("server.manage_competition_places_in_db")
    mocker.patch("server.manage_club_points_in_db")

    # Simulates a POST request with only the modified number of places
    response = client.post('/purchasePlaces', data={
        **MockData.purchase_place_data
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data


def test_should_display_showSummary_with_valid_competition(client, mocker):
    """Test that the showSummary page is displayed with valid competition"""
    mocker.patch("server.clubs", copy.deepcopy(MockData.mock_clubs))
    mocker.patch("server.competitions", [copy.deepcopy(MockData.mock_competitions[0])])
    mocker.patch("server.manage_competition_places_in_db")
    mocker.patch("server.manage_club_points_in_db")

    response = client.post('/showSummary', data={'email': 'club1@example.com'})

    # Check find a valid competition
    assert response.status_code == 200
    assert b"Competition 1" in response.data
    assert b"Date: 2030-01-01 13:00:00" in response.data
    assert b"Number of Places: 14" in response.data
    assert b"Book Places" in response.data


def test_should_display_list_of_clubs_and_their_points(client, mocker):
    """Test that the displayClubsList page is displayed with the list of clubs and their points"""
    mocker.patch("server.clubs", copy.deepcopy(MockData.mock_clubs))
    response = client.get('/displayClubsList')

    # Check find the list of clubs
    assert response.status_code == 200
    assert b"Clubs List: " in response.data
    assert b"Club 1" in response.data
    assert b"Club 2" in response.data
    assert b"Points: 17" in response.data
    assert b"Points: 0" in response.data
    assert b"club1@example.com" not in response.data
    assert b"club2@example.com" not in response.data
