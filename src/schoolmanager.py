from .emailclient import EmailClient
from .user import User
from .course import Course
class SchoolManager:
    def __init__(self):
        self.email_client = EmailClient()

    def calculate_price(self, course:Course, user : User):
        price = course.price
        if user.is_premium:
            price = price * 0.8
        if user.region == "PL":
            price = price - 10
        if price < 0:
            return 0.0
        return price

    def enroll(self, user:User, course:Course):
        if user.email == "invalid":
            return "User data is invalid"
        if course.id in user.saved_courses:
            return "User already enrolled"
        if not course.is_published:
            return "Course not published"
        
        user.saved_courses.append(course.id)
        self.email_client.send(user.email, f"Welcome to {course.title}")
        return True

    def add_review(self, user:User, course_id, rating, comment):
        if rating < 1 or rating > 5:
            return "Rating must be 1-5"
        if course_id not in user.saved_courses:
            return "User must buy course first"
        
        return {"user": user.id, "course": course_id, "rating": rating, "comment": comment}