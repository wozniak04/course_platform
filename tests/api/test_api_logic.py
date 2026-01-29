import pytest
import requests

class TestLogicAPI:
    URL = "http://127.0.0.1:5000"

    @pytest.fixture(autouse=True)
    def setup(self):
        requests.delete(f"{self.URL}/clear")
        
        requests.post(f"{self.URL}/users", json={"email": "u@t.pl", "age": 20, "region": "US"}) # Region US (brak zniżki -10)
        requests.post(f"{self.URL}/courses", json={"title": "C++", "price": 100, "materials_count": 5, "owner": "B", "published": True})
        requests.post(f"{self.URL}/courses", json={"title": "Draft", "price": 50, "materials_count": 1, "owner": "B", "published": False})

    def test_enrollment_edge_cases(self):
        # 1.Zapis na nieopublikowany kurs (400)
        r = requests.post(f"{self.URL}/enroll", json={"email": "u@t.pl", "title": "Draft"})
        assert r.status_code == 400
        assert "not published" in r.json()["error"]

        # 2. Poprawny zapis
        r = requests.post(f"{self.URL}/enroll", json={"email": "u@t.pl", "title": "C++"})
        assert r.status_code == 200

        # 3.Zapis ponowny na to samo (400)
        r = requests.post(f"{self.URL}/enroll", json={"email": "u@t.pl", "title": "C++"})
        assert r.status_code == 400
        assert "already enrolled" in r.json()["error"]

    def test_pricing_logic(self):
        # US Region, no premium: 100.0
        r = requests.post(f"{self.URL}/price", json={"email": "u@t.pl", "title": "C++"})
        assert r.json()["final_price"] == 100.0

        # Zmiana na PL: 100 - 10 = 90
        requests.delete(f"{self.URL}/clear")
        requests.post(f"{self.URL}/users", json={"email": "pl@t.pl", "age": 20, "region": "PL"})
        requests.post(f"{self.URL}/courses", json={"title": "C++", "price": 100, "materials_count": 5, "owner": "B", "published": True})
        r = requests.post(f"{self.URL}/price", json={"email": "pl@t.pl", "title": "C++"})
        assert r.json()["final_price"] == 90.0

    def test_review_edge_cases(self):
        # 1. Recenzja bez zakupu (400)
        r = requests.post(f"{self.URL}/review", json={"email": "u@t.pl", "title": "C++", "rating": 5, "comment": "X"})
        assert r.status_code == 400
        
        #  Zła ocena (0 lub 6)
        requests.post(f"{self.URL}/enroll", json={"email": "u@t.pl", "title": "C++"})
        r = requests.post(f"{self.URL}/review", json={"email": "u@t.pl", "title": "C++", "rating": 6, "comment": "X"})
        assert r.status_code == 400
        assert "1-5" in r.json()["error"]

        # 3. Poprawna recenzja
        r = requests.post(f"{self.URL}/review", json={"email": "u@t.pl", "title": "C++", "rating": 4, "comment": "Ok"})
        assert r.status_code == 201