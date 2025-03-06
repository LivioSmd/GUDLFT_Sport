import copy
from .fixtures import client, MockData


def test_should_redirect_to_index_if_invalid_email(client, mocker):
    """Test that the application redirects to the home page if the email is invalid."""
    mocker.patch("server.clubs", copy.deepcopy(MockData.mock_clubs))

    response = client.post('/showSummary', data={'email': 'invalid@example.com'})

    assert response.status_code == 302
    assert response.headers['Location'] == '/'  # Check redirection to home page


def test_should_not_valid_purchase_places_if_places_required_is_empty(client, mocker):
    """Test that we cannot book places if the number of places is empty."""
    mocker.patch("server.clubs", copy.deepcopy(MockData.mock_clubs))
    mocker.patch("server.competitions", copy.deepcopy(MockData.mock_competitions))
    mocker.patch("server.manage_competition_places_in_db")
    mocker.patch("server.manage_club_points_in_db")

    response = client.post('/purchasePlaces', data={
        **MockData.purchase_place_data,
        'places': ""
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Sorry, select a number of places greater than 0." in response.data


def test_should_not_valid_purchase_places_if_places_required_are_grater_than_number_of_club_points(client, mocker):
    """Test that we cannot book places if the number of places required is greater than the number of club points."""
    mocker.patch("server.clubs", copy.deepcopy(MockData.mock_clubs))
    mocker.patch("server.competitions", copy.deepcopy(MockData.mock_competitions))
    mocker.patch("server.manage_competition_places_in_db")
    mocker.patch("server.manage_club_points_in_db")

    response = client.post('/purchasePlaces', data={
        **MockData.purchase_place_data,
        'places': "18"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Sorry, your club doesn&#39;t have enough points." in response.data


def test_not_purchase_places_if_places_required_are_grater_than_number_of_competition_available_places(client, mocker):
    """Test that we cannot book places if the number of
    places required is greater than the number of available places."""
    mocker.patch("server.clubs", copy.deepcopy(MockData.mock_clubs))
    mocker.patch("server.competitions", copy.deepcopy(MockData.mock_competitions))
    mocker.patch("server.manage_competition_places_in_db")
    mocker.patch("server.manage_club_points_in_db")

    response = client.post('/purchasePlaces', data={
        **MockData.purchase_place_data,
        'places': "16"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Sorry, you cannot reserve more places than are available." in response.data


def test_clubs_cannot_purchase_more_than_twelve_places_per_competition(client, mocker):
    """clubs should not be able to purchase more than 12 places per competition"""
    mocker.patch("server.clubs", copy.deepcopy(MockData.mock_clubs))
    mocker.patch("server.competitions", copy.deepcopy(MockData.mock_competitions))
    mocker.patch("server.manage_competition_places_in_db")
    mocker.patch("server.manage_club_points_in_db")

    response = client.post('/purchasePlaces', data={
        **MockData.purchase_place_data,
        'places': "13"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Sorry, the maximum number of places per club per competition is : 12." in response.data


def test_should_display_showSummary_with_over_competition(client, mocker):
    """Test that the showSummary page is displayed an over competition"""
    mocker.patch("server.clubs", copy.deepcopy(MockData.mock_clubs))
    mocker.patch("server.competitions", [copy.deepcopy(MockData.mock_competitions[2])])
    mocker.patch("server.manage_competition_places_in_db")
    mocker.patch("server.manage_club_points_in_db")

    response = client.post('/showSummary', data={'email': 'club1@example.com'})

    # Check find an over competition
    assert response.status_code == 200
    assert b"Competition 3" in response.data
    assert b"Date: 2000-01-01 13:00:00" in response.data
    assert b"This competition is now over" in response.data


def test_should_display_showSummary_with_no_place_in_competition(client, mocker):
    """test that the showSummary page is displayed with a competition with no place"""
    mocker.patch("server.clubs", copy.deepcopy(MockData.mock_clubs))
    mocker.patch("server.competitions", [copy.deepcopy(MockData.mock_competitions[3])])
    mocker.patch("server.manage_competition_places_in_db")
    mocker.patch("server.manage_club_points_in_db")

    response = client.post('/showSummary', data={'email': 'club1@example.com'})

    # Check find a competition with no place
    assert response.status_code == 200
    assert b"Competition 4" in response.data
    assert b"Date: 2030-01-01 13:00:00" in response.data
    assert b"Number of Places: 0" in response.data
    assert b"Sorry, there are no more places available in this competition" in response.data
