import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from .fixtures import Utils

thisClub = {"name": "Club 1", "email": "club1@example.com"}


class TestAuthentification:
    """Test de l'authentification."""

    def setup_method(self):  # setup_method est une methode de pytest qui permet d'initialiser les tests
        """Initialisation des tests."""
        self.browser = webdriver.Chrome()  # Créer le navigateur

        # Chargement de la page d'accueil
        self.browser.get("http://127.0.0.1:5000")

        # Pause pour voir la fenêtre
        Utils.sleep()

    def teardown_method(self):  # teardown_method est une methode de pytest qui est appelée après chaque test
        """Fermeture du navigateur après chaque test."""
        self.browser.quit()  # Ferme proprement le navigateur

    def test_open_chrome_window(self):

        # Récupération du titre H1
        h1_element = self.browser.find_element(By.TAG_NAME, "h1")

        # Vérification du titre H1
        assert h1_element.text == "Welcome to the GUDLFT Registration Portal!", "Le titre H1 est incorrect"

    def test_connexion_invalid_email(self, mocker):

        # Récupération du champ email
        email_input = self.browser.find_element(By.NAME, "email")

        # Récupération du champ submit
        submit_button = self.browser.find_element(By.TAG_NAME, "button")

        email_input.clear()  # Nettoie le champ

        # Saisie de l'email
        email_input.send_keys("invalid@example.com")

        # Appui sur le bouton submit
        submit_button.click()

        Utils.sleep()

        # Récupération du titre "H1" et du "li" qui contient le message d'erreur
        h1_element = self.browser.find_element(By.TAG_NAME, "h1")
        li_element = self.browser.find_element(By.TAG_NAME, "li")

        # Vérification du titre "h1" et du message d'erreur
        assert h1_element.text == "Welcome to the GUDLFT Registration Portal!", "Le titre H1 est incorrect"
        assert li_element.text == "Sorry, we couldn't find that email.", "Le message d'erreur est incorrect"

    def test_connexion_valid_email(self, mocker):
        """Test d'authentification avec un email invalide."""

        # Récupération du champ email
        email_input = self.browser.find_element(By.NAME, "email")

        # Récupération du champ submit
        submit_button = self.browser.find_element(By.TAG_NAME, "button")

        # Saisie de l'email
        email_input.send_keys("admin@irontemple.com")

        # Appui sur le bouton submit
        submit_button.click()

        Utils.sleep()

        # Récupération du titre "H1"
        h2_element = self.browser.find_element(By.TAG_NAME, "h2")

        # Vérification du titre "h1"
        assert h2_element.text == "Welcome, admin@irontemple.com", "Impossible de trouver le message d'après connexion"
