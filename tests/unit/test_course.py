from src.course import Course

def test_create_published_course():
    c = Course("Python", 100, 10,5)
    c.publishCourse()
    assert c.title == "Python"
    assert c.price == 100
    assert c.is_published is True

def test_create_unpublished_course():
    c = Course("Java", 200, 20,2)
    assert c.title == "Java"
    assert c.is_published is False
def test_update_course():
    
    c1 = Course("Java", 200, 20, "Marek")
    c2 = Course("Python", 100, 10, "Ania")

   
    c1.update_data(title="Java Pro", price=250, materials_count=30)
    assert c1.title == "Java Pro"
    assert c1.price == 250
    assert c1.materials_count == 30

    
    c2.update_data(price=120)
    assert c2.title == "Python"  
    assert c2.price == 120       
    assert c2.materials_count == 10 

    
    c2.update_data(title=None, price=None, materials_count=None)
    assert c2.title == "Python"
    assert c2.price == 120