from .fixtures import client, MockData
from server import logout


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
