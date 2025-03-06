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

    def test_should_should_display_list_of_clubs_and_their_points(self):
        """Test displayClubsList page is displayed with the list of clubs and their points"""
        clubs_list_button = self.browser.find_element(By.ID, "clubs_list_button")
        clubs_list_button.click()
        Utils.sleep()

        clubs_list_title = self.browser.find_element(By.TAG_NAME, "h2")
        go_back_button = self.browser.find_element(By.ID, "go_back_button")
        club_name = self.browser.find_element(By.ID, "club_name_Test_Club")
        club_point = self.browser.find_element(By.ID, "club_points_Test_Club")

        assert clubs_list_title.text == "Clubs List:", "Error in element retrieval"
        assert go_back_button is not None, "Error in element retrieval"
        assert club_name.text.startswith("Club: "), "Error in element retrieval"
        assert club_point.text.startswith("Points: "), "Error in element retrieval"
