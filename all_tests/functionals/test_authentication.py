from selenium import webdriver
from selenium.webdriver.common.by import By
from .fixtures import Utils


class TestAuthentication:
    """Test of authentication."""

    def setup_method(self):  # setup_method is a pytest method performed before each test
        """Initialization of tests, before each test."""
        # Create a Chrome browser
        self.browser = webdriver.Chrome()

        # Home page loading
        self.browser.get("http://127.0.0.1:5000")

        # Pause for 2 second, to let the page load
        Utils.sleep()

    def teardown_method(self):  # teardown_method is a pytest method performed after each test
        """Closing the browser after each test."""
        self.browser.quit()  # Ferme proprement le navigateur

    def test_open_chrome_window(self):
        """Test of opening the Chrome window."""
        # H1 title retrieval
        h1_element = self.browser.find_element(By.TAG_NAME, "h1")

        # Verification of the title
        assert h1_element.text == "Welcome to the GUDLFT Registration Portal!", "Error in element retrieval"

    def test_connexion_invalid_email(self):
        """Test authentication with an invalid email."""
        email_input = self.browser.find_element(By.NAME, "email")
        submit_button = self.browser.find_element(By.TAG_NAME, "button")

        email_input.clear()  # clear the input field

        # email entry
        email_input.send_keys("invalid@example.com")

        # click on the submit button
        submit_button.click()
        Utils.sleep()

        # retrieval of the "h1" title and the error message in "li"
        h1_element = self.browser.find_element(By.TAG_NAME, "h1")
        li_element = self.browser.find_element(By.TAG_NAME, "li")

        # Verification of the title and the error message
        assert h1_element.text == "Welcome to the GUDLFT Registration Portal!", "Error in element retrieval"
        assert li_element.text == "Sorry, we couldn't find that email.", "Error in element retrieval"

    def test_connexion_valid_email(self):
        """Test authentication with a valid email."""
        email_input = self.browser.find_element(By.NAME, "email")
        submit_button = self.browser.find_element(By.TAG_NAME, "button")

        email_input.send_keys("admin@test.com")
        submit_button.click()
        Utils.sleep()

        h2_element = self.browser.find_element(By.TAG_NAME, "h2")

        assert h2_element.text == "Welcome, admin@test.com", "Error in element retrieval"
