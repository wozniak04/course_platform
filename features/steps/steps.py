from behave import *
import requests

URL = "http://127.0.0.1:5000"



@step('School system is empty')
def clear_system(context):
    r = requests.delete(f"{URL}/clear")
    assert r.status_code == 200

@step('I register a user with email: "{email}", age: "{age}", region: "{region}"')
def register_user(context, email, age, region):
    payload = {"email": email, "age": int(age), "region": region}
    r = requests.post(f"{URL}/users", json=payload)
    assert r.status_code == 201

@step('I create a course titled: "{title}" with price: "{price}", materials: "{count}", owner: "{owner}"')
def create_course(context, title, price, count, owner):
    payload = {"title": title, "price": float(price), "materials_count": int(count), "owner": owner}
    r = requests.post(f"{URL}/courses", json=payload)
    assert r.status_code == 201
    
@step('Course "{title}" is published')
def publish_course_step(context, title):
    r = requests.post(f"{URL}/courses/{title}/publish")
    assert r.status_code == 200




@when('I delete course with title: "{title}"')
def delete_course(context, title):
    r = requests.delete(f"{URL}/courses/{title}")
    assert r.status_code == 200

@when('I update "{field}" of course "{title}" to "{value}"')
def update_course(context, field, title, value):
    
    if field == "price":
        val = float(value)
    elif field == "materials_count":
        val = int(value)
    else:
        val = value
        
    payload = {field: val}
    r = requests.patch(f"{URL}/courses/{title}", json=payload)
    assert r.status_code == 200

@when('I enroll user "{email}" to course "{title}"')
def enroll_user(context, email, title):
    r = requests.post(f"{URL}/enroll", json={"email": email, "title": title})
    assert r.status_code == 200

@when('I add review for course "{title}" from "{email}" with rating: "{rating}" and comment: "{comment}"')
def add_review(context, title, email, rating, comment):
    payload = {"email": email, "title": title, "rating": int(rating), "comment": comment}
    r = requests.post(f"{URL}/review", json=payload)
    assert r.status_code == 201



@then('Number of users in system equals: "{count}"')
def check_users_count(context, count):
    r = requests.get(f"{URL}/users/count")
    assert r.json()["count"] == int(count)

@then('Number of courses in system equals: "{count}"')
def check_courses_count(context, count):
    r = requests.get(f"{URL}/courses/count")
    assert r.json()["count"] == int(count)

@then('User with email "{email}" exists in system')
def user_exists(context, email):
    r = requests.get(f"{URL}/users/{email}")
    assert r.status_code == 200

@then('Course "{title}" exists in system')
def course_exists(context, title):
    r = requests.get(f"{URL}/courses/{title}")
    assert r.status_code == 200

@then('Course "{title}" does not exist in system')
def course_not_exists(context, title):
    r = requests.get(f"{URL}/courses/{title}")
    assert r.status_code == 404

@then('Course "{title}" has "{field}" equal to "{value}"')
def check_course_field(context, title, field, value):
    r = requests.get(f"{URL}/courses/{title}")
    data = r.json()
    
    
    actual_val = data[field]
    if field in ["price", "materials_count"]:
        assert float(actual_val) == float(value)
    else:
        assert str(actual_val) == str(value)


@then('Course "{title}" has "{count}" reviews')
def check_reviews_count(context, title, count):
    r = requests.get(f"{URL}/courses/{title}")
    assert len(r.json()["reviews"]) == int(count)