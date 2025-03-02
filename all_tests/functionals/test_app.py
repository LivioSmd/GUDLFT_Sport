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
        assert h1_element.text == "Welcome to the GUDLFT Registration Portal!", "Error in element retrieval"

    def test_connexion_invalid_email(self):
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
        assert h1_element.text == "Welcome to the GUDLFT Registration Portal!", "Error in element retrieval"
        assert li_element.text == "Sorry, we couldn't find that email.", "Error in element retrieval"

    def test_connexion_valid_email(self):
        """Test d'authentification avec un email invalide."""

        # Récupération du champ email
        email_input = self.browser.find_element(By.NAME, "email")

        # Récupération du champ submit
        submit_button = self.browser.find_element(By.TAG_NAME, "button")

        # Saisie de l'email
        email_input.send_keys("admin@test.com")

        # Appui sur le bouton submit
        submit_button.click()

        Utils.sleep()

        # Récupération du titre "H1"
        h2_element = self.browser.find_element(By.TAG_NAME, "h2")

        # Vérification du titre "h1"
        assert h2_element.text == "Welcome, admin@test.com", "Error in element retrieval"

    def test_should_purchase_places(self):
        """Test de reservation de places"""

        email_input = self.browser.find_element(By.NAME, "email")
        login_submit_button = self.browser.find_element(By.TAG_NAME, "button")
        email_input.send_keys("admin@test.com")
        login_submit_button.click()
        Utils.sleep()

        # récupération du bouton de réservation
        book_competition_button = self.browser.find_element(By.ID, "competition_4")
        book_competition_button.click()

        Utils.sleep()

        places_input = self.browser.find_element(By.NAME, "places")
        places_input.send_keys("1")
        places_submit_button = self.browser.find_element(By.TAG_NAME, "button")
        places_submit_button.click()

        Utils.sleep()

        li_element = self.browser.find_element(By.TAG_NAME, "li")
        assert li_element.text == "Great-booking complete!", "Error in element retrieval"

    def test_should_not_purchase_less_than_one_place(self):
        """Test de reservation de places"""

        email_input = self.browser.find_element(By.NAME, "email")
        login_submit_button = self.browser.find_element(By.TAG_NAME, "button")
        email_input.send_keys("admin@test.com")
        login_submit_button.click()
        Utils.sleep()
        book_competition_button = self.browser.find_element(By.ID, "competition_4")
        book_competition_button.click()
        Utils.sleep()
        places_input = self.browser.find_element(By.NAME, "places")
        places_input.send_keys("0")
        places_submit_button = self.browser.find_element(By.TAG_NAME, "button")
        places_submit_button.click()
        Utils.sleep()

        li_element = self.browser.find_element(By.TAG_NAME, "li")
        assert li_element.text == "Sorry, select a number of places greater than 0.", "Error in element retrieval"

    def test_should_not_book_more_places_than_you_own(self):
        """Test de reservation de places"""

        email_input = self.browser.find_element(By.NAME, "email")
        login_submit_button = self.browser.find_element(By.TAG_NAME, "button")
        email_input.send_keys("admin@test.com")
        login_submit_button.click()
        Utils.sleep()
        book_competition_button = self.browser.find_element(By.ID, "competition_4")
        book_competition_button.click()
        Utils.sleep()
        places_input = self.browser.find_element(By.NAME, "places")
        places_input.send_keys("101")
        places_submit_button = self.browser.find_element(By.TAG_NAME, "button")
        places_submit_button.click()
        Utils.sleep()

        li_element = self.browser.find_element(By.TAG_NAME, "li")
        assert li_element.text == "Sorry, your club doesn't have enough points.", "Error in element retrieval"

    def test_should_not_book_more_places_than_are_available(self):
        """Test de reservation de places"""

        email_input = self.browser.find_element(By.NAME, "email")
        login_submit_button = self.browser.find_element(By.TAG_NAME, "button")
        email_input.send_keys("admin@test.com")
        login_submit_button.click()
        Utils.sleep()
        book_competition_button = self.browser.find_element(By.ID, "competition_4")
        book_competition_button.click()
        Utils.sleep()
        places_input = self.browser.find_element(By.NAME, "places")
        places_input.send_keys("51")
        places_submit_button = self.browser.find_element(By.TAG_NAME, "button")
        places_submit_button.click()
        Utils.sleep()

        li_element = self.browser.find_element(By.TAG_NAME, "li")
        assert li_element.text == "Sorry, you cannot reserve more places than are available.", "Error in element retrieval"

    def test_should_not_book_more_than_twelve_places_per_competition(self):
        """Test de reservation de places"""

        email_input = self.browser.find_element(By.NAME, "email")
        login_submit_button = self.browser.find_element(By.TAG_NAME, "button")
        email_input.send_keys("admin@test.com")
        login_submit_button.click()
        Utils.sleep()
        book_competition_button = self.browser.find_element(By.ID, "competition_4")
        book_competition_button.click()
        Utils.sleep()
        places_input = self.browser.find_element(By.NAME, "places")
        places_input.send_keys("13")
        places_submit_button = self.browser.find_element(By.TAG_NAME, "button")
        places_submit_button.click()
        Utils.sleep()

        li_element = self.browser.find_element(By.TAG_NAME, "li")
        assert li_element.text == "Sorry, the maximum number of places per club per competition is : 12.", "Error in element retrieval"

    def test_should_should_display_showSummary_with_valid_competition(self):
        """Test showSummary page is displayed with valid competition"""

        email_input = self.browser.find_element(By.NAME, "email")
        login_submit_button = self.browser.find_element(By.TAG_NAME, "button")
        email_input.send_keys("admin@test.com")
        login_submit_button.click()
        Utils.sleep()

        book_place_element = self.browser.find_element(By.ID, "competition_4")
        assert book_place_element.text == "Book Places", "Error in element retrieval"

    def test_should_should_display_showSummary_with_not_available_competition(self):
        """Test showSummary page is displayed with not available competition"""

        email_input = self.browser.find_element(By.NAME, "email")
        login_submit_button = self.browser.find_element(By.TAG_NAME, "button")
        email_input.send_keys("admin@test.com")
        login_submit_button.click()
        Utils.sleep()

        comp_over_element = self.browser.find_element(By.ID, "comp_error_comp_over_2")
        comp_no_place_element = self.browser.find_element(By.ID, "comp_no_place_3")
        assert comp_over_element.text == "This competition is now over", "Error in element retrieval"
        assert comp_no_place_element.text == "Sorry, there are no more places available in this competition", "Error in element retrieval"
