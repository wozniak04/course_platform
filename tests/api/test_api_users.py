import pytest
import requests

class TestUserAPI:
    URL = "http://127.0.0.1:5000"

    @pytest.fixture(autouse=True)
    def setup(self):
        requests.delete(f"{self.URL}/clear")

    def test_register_valid_user(self):
        payload = {"email": "jan@test.pl", "age": 20, "region": "PL"}
        r = requests.post(f"{self.URL}/users", json=payload)
        assert r.status_code == 201
        assert r.json()["email"] == "jan@test.pl"

    def test_error_register_duplicate_email(self):
        payload = {"email": "jan@test.pl", "age": 20}
        requests.post(f"{self.URL}/users", json=payload)
        r = requests.post(f"{self.URL}/users", json=payload)
        assert r.status_code == 409
        assert "already registered" in r.json()["message"]

    def test_error_age_below_18(self):
        payload = {"email": "bobo@test.pl", "age": 17}
        r = requests.post(f"{self.URL}/users", json=payload)
        assert r.status_code == 400
        assert "zły email lub wiek" in r.json()["message"]

    def test_error_invalid_email_format(self):
        payload = {"email": "jan_at_test.pl", "age": 25} # brak @
        r = requests.post(f"{self.URL}/users", json=payload)
        assert r.status_code == 400

    def test_get_user_by_email_success(self):
        requests.post(f"{self.URL}/users", json={"email": "find@test.pl", "age": 30})
        r = requests.get(f"{self.URL}/users/find@test.pl")
        assert r.status_code == 200
        assert r.json()["email"] == "find@test.pl"

    def test_get_user_404_not_found(self):
        r = requests.get(f"{self.URL}/users/nieistnieje@test.pl")
        assert r.status_code == 404

    def test_delete_user_success(self):
        requests.post(f"{self.URL}/users", json={"email": "delete@test.pl", "age": 20})
        r = requests.delete(f"{self.URL}/users/delete@test.pl")
        assert r.status_code == 200
        
        # Potwierdzenie usunięcia
        r_check = requests.get(f"{self.URL}/users/delete@test.pl")
        assert r_check.status_code == 404

    def test_delete_user_404_not_found(self):
        r = requests.delete(f"{self.URL}/users/brak@test.pl")
        assert r.status_code == 404

    def test_users_count_increment(self):
        requests.post(f"{self.URL}/users", json={"email": "u1@t.pl", "age": 20})
        requests.post(f"{self.URL}/users", json={"email": "u2@t.pl", "age": 21})
        r = requests.get(f"{self.URL}/users/count")
        assert r.json()["count"] == 2