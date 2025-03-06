from selenium import webdriver
from selenium.webdriver.common.by import By
from .fixtures import Utils


class TestPurchase:
    """Test of purchase places."""

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

    def test_should_purchase_places(self):
        """Test of booking places"""
        email_input = self.browser.find_element(By.NAME, "email")
        login_submit_button = self.browser.find_element(By.TAG_NAME, "button")
        email_input.send_keys("admin@test.com")
        login_submit_button.click()
        Utils.sleep()

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
        """Test should not book less than one place"""
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
        """Test should not book more places than you own"""
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
        """Test should not book more places than are available"""
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
        assert li_element.text == "Sorry, you cannot reserve more places than are available.", \
            "Error in element retrieval"

    def test_should_not_book_more_than_twelve_places_per_competition(self):
        """Test should not book more than twelve places per competition"""
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
        assert li_element.text == "Sorry, the maximum number of places per club per competition is : 12.", \
            "Error in element retrieval"
