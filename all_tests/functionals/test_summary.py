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
        assert comp_no_place_element.text == "Sorry, there are no more places available in this competition", \
            "Error in element retrieval"
