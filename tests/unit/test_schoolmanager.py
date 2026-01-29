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

def test_register_and_get_user(manager):
    u = User("test@wp.pl", 25)
    manager.register_user(u)
    assert manager.number_of_users() == 1 
    assert manager.get_user_by_email("test@wp.pl") == u
    assert manager.get_user_by_email("not@exists.pl") is None

def test_add_course(manager):
    c = Course("Python", 100, 5, "Admin")
    manager.add_course(c)
    assert manager.number_of_courses()==1
    assert manager.courses[0].owner == "Admin"



def test_calculate_price_logic(manager):
    u = User("pl@wp.pl", 20, "PL")
    u.is_premium = True
    c = Course("Java", 100, 10, "Instructor")
    # (100 * 0.8) - 10 = 70
    assert manager.calculate_price(c, u) == 70.0

def test_get_course_by_title(manager):
    c = Course("Python", 100, 5, "Admin")
    manager.add_course(c)

    res=manager.get_course_by_title("Python")
    assert res.title == "Python"
    res2=manager.get_course_by_title("qsdfgasdf")
    assert res2 is None

def test_enroll_flow(manager):
    u = User("student@edu.pl", 20)
    c = Course("Git", 50, 2, "Boss")
    c.publishCourse()
    
    assert manager.enroll(u, c) is True
    assert "Git" in u.saved_courses
    
    assert manager.enroll(u, c) == "User already enrolled"
    
    c2 = Course("Secret", 10, 1, "Boss")
    c2.publishCourse()
    c2.hideCourse()
    
    assert manager.enroll(u, c2) == "Course not published"

def test_enroll_invalid_user(manager):
    u = User("zly_mail", 10)
    c = Course("Git", 50, 2, "Boss")
    assert manager.enroll(u, c) == "User data is invalid"

def test_add_review_success(manager):
    u = User("fan@wp.pl", 25)
    u.saved_courses.append("Python")
    c = Course("Python", 100, 5, "Admin")
    manager.add_course(c)

    wynik = manager.add_review(u, "Python", 5, "Super!")
    
    assert isinstance(wynik, dict)
    assert wynik["rating"] == 5
    assert len(c.reviews) == 1

def test_add_review_invalid_rating(manager):
    u = User("fan@wp.pl", 25)
    res = manager.add_review(u, "Python", 0, "Zle")
    assert res == "Rating must be 1-5"
    res = manager.add_review(u, "Python", 6, "Zle")
    assert res == "Rating must be 1-5"

def test_add_review_not_enrolled(manager):
    u = User("fan@wp.pl", 25) 
    res = manager.add_review(u, "Python", 5, "Super!")
    assert res == "User must buy course first"

def test_add_review_course_not_exists(manager):
    u = User("fan@wp.pl", 25)
    u.saved_courses.append("Java") 
    res = manager.add_review(u, "Java", 5, "Super!")
    assert res == "Course does not exist"

def test_delete_user(manager):
    u = User("fan@wp.pl", 25)
    manager.register_user(u)

    assert manager.users[0].email == "fan@wp.pl"

    assert manager.delete_user("fan@wp.pl") == True
    assert manager.number_of_users() == 0

    assert manager.delete_user("asfsafd@s") == False # no user with that email

def test_delete_course(manager):
    c = Course("Python", 100, 5, "Admin")
    manager.add_course(c)
    assert manager.courses[0].title == "Python"
    assert manager.delete_course("Python") == True
    assert manager.number_of_courses() == 0

    assert manager.delete_course("ssdfasfd") == False # no course with that title
    