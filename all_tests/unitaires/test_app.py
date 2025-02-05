from .fixtures import client

""""
def test_should_start_app(client):

    response = client.get('/')
    assert response.status_code == 200


def test_should_redirect_to_index_if_invalid_email(client, mocker):


    # Données mockées pour remplacer le contenu de `clubs`
    mock_clubs = [
        {"name": "Club 1", "email": "club1@example.com"},
        {"name": "Club 2", "email": "club2@example.com"}
    ]

    # Mock de la fonction loadClubs
    mocker.patch("server.loadClubs", return_value=mock_clubs)

    # Simule une requête POST avec un email invalide
    response = client.post('/showSummary', data={'email': 'invalid@example.com'})

    print(response.headers)
    assert response.status_code == 302  # Vérifie la redirection
    assert response.headers['Location'] == '/'  # Vérifie la redirection vers la page d'accueil
"""""


def test_should_valid_email(client, mocker):
    """
    Test que l'application redirige vers la page welcome si l'email est valide.
    """

    # Données mockées pour remplacer le contenu de `clubs`
    mock_clubs = [
        {"name": "Club 1", "email": "club1@example.com"},
        {"name": "Club 2", "email": "club2@example.com"}
    ]

    # Mock de la fonction loadClubs
    mocker.patch("server.loadClubs", return_value=mock_clubs)

    # Simule une requête POST avec un email invalide
    response = client.post('/showSummary', data={'email': 'club1@example.com'})
    # response = client.post("/showSummary", data={"email": "admin@irontemple.com"})

    print('headers : ', response.headers)
    print('response : ', response)

    assert response.status_code == 200
    assert b"Welcome" in response.data
