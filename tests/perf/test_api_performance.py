import pytest
import requests

BASE_URL = "http://localhost:5000"

class TestApiPerformance:

    @pytest.fixture(autouse=True)
    def setup(self):
        
        requests.delete(f"{BASE_URL}/clear")

    def test_create_and_delete_user_speed(self):
        
        for i in range(100):
            email = f"perf_{i}@test.pl"
            payload = {
                "email": email,
                "age": 25,
                "region": "PL"
            }
            
            
            response = requests.post(f"{BASE_URL}/users", json=payload, timeout=0.5)
            assert response.status_code == 201
            
            
            del_response = requests.delete(f"{BASE_URL}/users/{email}", timeout=0.5)
            assert del_response.status_code == 200

    def test_multiple_enrollments_speed_and_consistency(self):
        
        test_email = "performance_student@test.pl"
        
        
        requests.post(f"{BASE_URL}/users", json={"email": test_email, "age": 20})
        
        for i in range(100):
            title = f"Course_{i}"
            
            requests.post(f"{BASE_URL}/courses", json={
                "title": title, "price": 10, "materials_count": 1, "owner": "Admin", "published": True
            })

            
            res = requests.post(
                f"{BASE_URL}/enroll",
                json={"email": test_email, "title": title},
                timeout=0.5
            )
            assert res.status_code == 200

        
        final_res = requests.get(f"{BASE_URL}/users/{test_email}")
        assert final_res.status_code == 200
        assert len(final_res.json()["courses"]) == 100

    def test_batch_course_creation_1000(self):
        
        for i in range(1000):
            title = f"Bulk_Course_{i}"
            res = requests.post(
                f"{BASE_URL}/courses", 
                json={"title": title, "price": 50, "materials_count": 1, "owner": "System"},
                timeout=0.5
            )
            assert res.status_code == 201

        
        count_res = requests.get(f"{BASE_URL}/courses/count")
        assert count_res.json()["count"] == 1000