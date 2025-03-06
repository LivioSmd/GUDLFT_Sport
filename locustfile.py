from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 2)  # Simulates a waiting time between each request (1 to 2 seconds)

    @task
    def test_home_page(self):
        response = self.client.get("")  # GET : Test the home page
        assert response.status_code == 200, f"Error: {response.text}"
        assert response.elapsed.total_seconds() <= 5, f"Response time too long: {response.elapsed.total_seconds()}s"

    @task
    def test_display_clubs_list_page(self):
        response = self.client.get("displayClubsList")
        assert response.status_code == 200, f"Error: {response.text}"
        assert response.elapsed.total_seconds() <= 5, f"Response time too long: {response.elapsed.total_seconds()}s"

    @task
    def test_display_summary_page(self):
        data = {"email": "admin@test.com"}

        response = self.client.post("showSummary", data=data)  # POST : Test the showSummary page with datas

        assert response.status_code == 200, f"Error: {response.text}"
        assert response.elapsed.total_seconds() <= 2, f"POST too long: {response.elapsed.total_seconds()}s"

    @task
    def test_display_book_page(self):
        response = self.client.get("book/Competition%205/Test%20Club")

        assert response.status_code == 200, f"Error: {response.text}"
        assert response.elapsed.total_seconds() <= 5, f"Response time too long: {response.elapsed.total_seconds()}s"

    @task
    def test_display_purchase_places(self):
        data = {
            "club": "Test Club",
            "competition": "Competition 5",
            "places": "1"
        }

        response = self.client.post("purchasePlaces", data=data)

        assert response.status_code == 200, f"Error: {response.text}"
        assert response.elapsed.total_seconds() <= 2, f"POST too long: {response.elapsed.total_seconds()}s"

    @task
    def test_logout(self):
        response = self.client.get("logout")

        assert response.status_code == 302, f"Error: {response.text}"
        assert response.elapsed.total_seconds() <= 5, f"Response time too long: {response.elapsed.total_seconds()}s"
