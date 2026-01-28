from src.course import Course

def test_create_published_course():
    c = Course(1, "Python", 100, 10)
    assert c.title == "Python"
    assert c.price == 100
    assert c.is_published is True

def test_create_unpublished_course():
    c = Course(2, "Java", 200, 20, is_published=False)
    assert c.title == "Java"
    assert c.is_published is False