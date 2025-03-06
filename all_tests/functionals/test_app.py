from selenium import webdriver
from selenium.webdriver.common.by import By
from .fixtures import Utils


class TestApp:
    """Test of app."""

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
