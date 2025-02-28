from .fixtures import client, MockData


def test_should_start_app(client):
    """Test que l'application démarre correctement."""

    # Simule une requête GET sur la page d'accueil
    response = client.get('/')

    # Verification de la réponse
    assert response.status_code == 200


def test_should_valid_email(client, mocker):
    """Test que l'application redirige vers la page welcome si l'email est valide."""

    # Mock de la fonction loadClubs
    mocker.patch("server.clubs", MockData.mock_clubs)

    # Simule une requête POST avec un email valide
    response = client.post('/showSummary', data={'email': 'club1@example.com'})

    # Verification de la redirection
    assert response.status_code == 200  # Vérifie le status code
    assert b"Welcome" in response.data  # Vérifie la présence du mot "Welcome" dans le contenu de la page


def test_should_redirect_to_index_if_invalid_email(client, mocker):
    """Test que l'application redirige vers la page welcome si l'email est valide."""

    # Mock de la fonction loadClubs
    mocker.patch("server.clubs", MockData.mock_clubs)

    # Simule une requête POST avec un email invalide
    response = client.post('/showSummary', data={'email': 'invalid@example.com'})

    # Verification de la redirection
    assert response.status_code == 302  # Vérifie le status code
    assert response.headers['Location'] == '/'  # Vérifie la redirection vers la page d'accueil


def test_should_valid_purchase_places(client, mocker):
    """Test que l'on puisse reserver des places dans une competition."""

    # Mock des fonctions
    mocker.patch("server.clubs", MockData.mock_clubs)
    mocker.patch("server.competitions", MockData.mock_competitions)

    # Simule une requête POST avec uniquement le nombre de place modifié
    response = client.post('/purchasePlaces', data={
        **MockData.purchase_place_data,
        'places': "10"
    }, follow_redirects=True)

    assert response.status_code == 200  # Vérifie le status code
    assert b"Great-booking complete!" in response.data  # Vérifie la présence du message dans le contenu de la page


def test_should_not_valid_purchase_places_if_places_required_is_empty(client, mocker):
    mocker.patch("server.clubs", MockData.mock_clubs)
    mocker.patch("server.competitions", MockData.mock_competitions)

    # Simule une requête POST avec uniquement le nombre de place modifié un nombre de places invalide
    response = client.post('/purchasePlaces', data={
        **MockData.purchase_place_data,
        'places': ""
    }, follow_redirects=True)
    assert response.status_code == 200  # Vérifie le status code
    assert b"Sorry, select a number of places greater than 0." in response.data


def test_should_not_valid_purchase_places_if_places_required_are_grater_than_number_of_club_points(client, mocker):
    mocker.patch("server.clubs", MockData.mock_clubs)
    mocker.patch("server.competitions", MockData.mock_competitions)
    response = client.post('/purchasePlaces', data={
        **MockData.purchase_place_data,
        'places': "35"
    }, follow_redirects=True)
    assert response.status_code == 200  # Vérifie le status code
    assert b"Sorry, your club doesn&#39;t have enough points." in response.data


def test_not_purchase_places_if_places_required_are_grater_than_number_of_competition_available_places(client, mocker):
    mocker.patch("server.clubs", MockData.mock_clubs)
    mocker.patch("server.competitions", MockData.mock_competitions)
    response = client.post('/purchasePlaces', data={
        **MockData.purchase_place_data,
        'places': "20"
    }, follow_redirects=True)
    assert response.status_code == 200  # Vérifie le status code
    assert b"Sorry, you cannot reserve more places than are available." in response.data


def test_clubs_cannot_purchase_more_than_twelve_places_per_competition(client, mocker):
    """clubs should not be able to purchase more than 12 places per competition"""

    mocker.patch("server.clubs", MockData.mock_clubs)
    mocker.patch("server.competitions", MockData.mock_competitions)
    response = client.post('/purchasePlaces', data={
        **MockData.purchase_place_data,
        'places': "13"
    }, follow_redirects=True)
    print(response.data)
    assert response.status_code == 200  # Vérifie le status code
    assert b"Sorry, the maximum number of places per club per competition is : 12." in response.data


def test_should_display_showSummary_with_valid_competition(client, mocker):
    """test that the showSummary page is displayed with valid competition"""

    mocker.patch("server.clubs", MockData.mock_clubs)
    mocker.patch("server.competitions", [MockData.mock_competitions[0]])

    response = client.post('/showSummary', data={'email': 'club1@example.com'})

    # Check find a valid competition
    assert response.status_code == 200
    assert b"Competition 1" in response.data
    assert b"Date: 2030-01-01 13:00:00" in response.data
    assert b"Number of Places: 25" in response.data
    assert b"Book Places" in response.data


def test_should_display_showSummary_with_over_competition(client, mocker):
    """test that the showSummary page is displayed with valid competition"""

    mocker.patch("server.clubs", MockData.mock_clubs)
    mocker.patch("server.competitions", [MockData.mock_competitions[2]])

    response = client.post('/showSummary', data={'email': 'club1@example.com'})

    # Check find an over competition
    assert response.status_code == 200
    assert b"Competition 3" in response.data
    assert b"Date: 2000-01-01 13:00:00" in response.data
    assert b"This competition is now over" in response.data


def test_should_display_showSummary_with_no_place_in_competition(client, mocker):
    """test that the showSummary page is displayed with valid competition"""

    mocker.patch("server.clubs", MockData.mock_clubs)
    mocker.patch("server.competitions", [MockData.mock_competitions[3]])

    response = client.post('/showSummary', data={'email': 'club1@example.com'})

    # Check find an over competition
    assert response.status_code == 200
    assert b"Competition 4" in response.data
    assert b"Date: 2030-01-01 13:00:00" in response.data
    assert b"Number of Places: 0" in response.data
    assert b"Sorry, there are no more places available in this competition" in response.data
