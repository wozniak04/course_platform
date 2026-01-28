import pytest
from unittest.mock import Mock
from src.schoolmanager import SchoolManager
from src.user import User
from src.course import Course

@pytest.fixture
def manager():
    man = SchoolManager()
    man.email_client = Mock()
    return man

def test_calculate_price_standard(manager):
    u = User(1, "a@a.com", 20, "US")
    c = Course(1, "C++", 100, 5)
    assert manager.calculate_price(c, u) == 100

def test_calculate_price_premium(manager):
    u = User(1, "a@a.com", 20, "US")
    u.toggle_premium()
    c = Course(1, "C++", 100, 5)
    # 100 * 0.8 = 80
    assert manager.calculate_price(c, u) == 80

def test_calculate_price_region_pl(manager):
    u = User(1, "a@a.com", 20, "PL")
    c = Course(1, "C++", 100, 5)
    # 100 - 10 = 90
    assert manager.calculate_price(c, u) == 90

def test_calculate_price_premium_and_pl(manager):
    u = User(1, "a@a.com", 20, "PL")
    u.toggle_premium()
    c = Course(1, "C++", 100, 5)
    # (100 * 0.8) - 10 = 80 - 10 = 70
    assert manager.calculate_price(c, u) == 70

def test_calculate_price_not_negative(manager):
    u = User(1, "a@a.com", 20, "PL")
    c = Course(1, "C++", 5, 5)
    # 5 - 10 = -5 -> ma zwrócić 0
    assert manager.calculate_price(c, u) == 0.0

def test_enroll_success(manager):
    u = User(1, "a@a.com", 20)
    c = Course(1, "Python", 50, 5)
    
    assert manager.enroll(u, c) is True
    assert 1 in u.saved_courses
    manager.email_client.send.assert_called()

def test_enroll_invalid_user(manager):
    u = User(1, "bad", 10) # email bedzie "invalid"
    c = Course(1, "Python", 50, 5)
    assert manager.enroll(u, c) == "User data is invalid"

def test_enroll_already_exists(manager):
    u = User(1, "a@a.com", 20)
    c = Course(1, "Python", 50, 5)
    u.saved_courses.append(1)
    
    assert manager.enroll(u, c) == "User already enrolled"

def test_enroll_not_published(manager):
    u = User(1, "a@a.com", 20)
    c = Course(1, "Python", 50, 5, is_published=False)
    assert manager.enroll(u, c) == "Course not published"

def test_add_review_success(manager):
    u = User(1, "a@a.com", 20)
    u.saved_courses.append(10)
    
    res = manager.add_review(u, 10, 5, "Good")
    assert res["rating"] == 5
    assert res["course"] == 10

def test_add_review_bad_rating(manager):
    u = User(1, "a@a.com", 20)
    assert manager.add_review(u, 10, 6, "Good") == "Rating must be 1-5"
    assert manager.add_review(u, 10, 0, "Good") == "Rating must be 1-5"

def test_add_review_not_enrolled(manager):
    u = User(1, "a@a.com", 20)
    # Lista kursów pusta
    assert manager.add_review(u, 10, 5, "Good") == "User must buy course first"