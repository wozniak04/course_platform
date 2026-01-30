import pytest
import requests

class TestCourseAPI:
    URL = "http://127.0.0.1:5000"

    @pytest.fixture(autouse=True)
    def setup(self):
        requests.delete(f"{self.URL}/clear")

    def test_add_valid_course(self):
        payload = {"title": "Python", "price": 100, "materials_count": 5, "owner": "Marek"}
        r = requests.post(f"{self.URL}/courses", json=payload)
        assert r.status_code == 201
        assert r.json()["title"] == "Python"

    def test_error_duplicate_course_title(self):
        payload = {"title": "Python", "price": 100, "materials_count": 5, "owner": "Marek"}
        requests.post(f"{self.URL}/courses", json=payload)
        r = requests.post(f"{self.URL}/courses", json=payload)
        assert r.status_code == 409
        assert "already exists" in r.json()["message"]

    def test_get_course_details_success(self):
        requests.post(f"{self.URL}/courses", json={"title": "Java", "price": 200, "materials_count": 10, "owner": "Ania"})
        r = requests.get(f"{self.URL}/courses/Java")
        assert r.status_code == 200
        assert r.json()["owner"] == "Ania"

    def test_get_course_404_not_found(self):
        r = requests.get(f"{self.URL}/courses/C_sharp")
        assert r.status_code == 404

    def test_delete_course_success(self):
        requests.post(f"{self.URL}/courses", json={"title": "PHP", "price": 10, "materials_count": 1, "owner": "X"})
        r = requests.delete(f"{self.URL}/courses/PHP")
        assert r.status_code == 200
        
        r_check = requests.get(f"{self.URL}/courses/PHP")
        assert r_check.status_code == 404

    def test_delete_course_404_not_found(self):
        r = requests.delete(f"{self.URL}/courses/Brak")
        assert r.status_code == 404

    def test_courses_list_all(self):
        requests.post(f"{self.URL}/courses", json={"title": "C1", "price": 1, "materials_count": 1, "owner": "A"})
        requests.post(f"{self.URL}/courses", json={"title": "C2", "price": 2, "materials_count": 2, "owner": "B"})
        r = requests.get(f"{self.URL}/courses")
        rlen=requests.get(f"{self.URL}/courses/count")

        assert len(r.json()) == 2
        assert rlen.json()["count"] == 2
        
    def test_update_course_all_fields(self):

        requests.post(f"{self.URL}/courses", json={"title": "Old", "price": 10, "materials_count": 1, "owner": "A"})
        
        payload = {"title": "New", "price": 99, "materials_count": 9}
        r = requests.patch(f"{self.URL}/courses/Old", json=payload)
        
        assert r.status_code == 200

        r_get = requests.get(f"{self.URL}/courses/New")
        assert r_get.json()["price"] == 99

    def test_update_course_partial_fields(self):
        requests.post(f"{self.URL}/courses", json={"title": "Python", "price": 100, "materials_count": 5, "owner": "A"})
        

        r = requests.patch(f"{self.URL}/courses/Python", json={"price": 150})
        assert r.status_code == 200
        
        r_get = requests.get(f"{self.URL}/courses/Python")
        assert r_get.json()["price"] == 150
        assert r_get.json()["title"] == "Python" 

    def test_update_course_404_not_found(self):
        r = requests.patch(f"{self.URL}/courses/Nieistnieje", json={"price": 100})
        assert r.status_code == 404

    def test_update_course_conflict_title(self):

        requests.post(f"{self.URL}/courses", json={"title": "Java", "price": 10, "materials_count": 1, "owner": "A"})
        requests.post(f"{self.URL}/courses", json={"title": "Python", "price": 10, "materials_count": 1, "owner": "A"})
        

        r = requests.patch(f"{self.URL}/courses/Java", json={"title": "Python"})
        assert r.status_code == 409
        assert "already exists" in r.json()["message"]
    def test_publish_and_hide_course_flow(self):
        
        title = "Cloud_Computing"
        requests.post(f"{self.URL}/courses", json={
            "title": title, "price": 300, "materials_count": 20, "owner": "Admin"
        })

        
        r_pub = requests.post(f"{self.URL}/courses/{title}/publish")
        assert r_pub.status_code == 200
        assert f"Course '{title}' has been published" in r_pub.json()["message"]

        
        r_hide = requests.post(f"{self.URL}/courses/{title}/hide")
        assert r_hide.status_code == 200
        assert f"Course '{title}' is now hidden" in r_hide.json()["message"]

    def test_publish_course_404(self):
        
        r = requests.post(f"{self.URL}/courses/GhostCourse/publish")
        assert r.status_code == 404
        assert "Course not found" in r.json()["error"]