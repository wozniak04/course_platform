from .emailclient import EmailClient
from .user import User
from .course import Course

class SchoolManager:
    def __init__(self):
        self.email_client = EmailClient()
        self.users = []
        self.courses = []

    def register_user(self, user):
        self.users.append(user)
        return user

    def add_course(self, course):
        self.courses.append(course)
        return course

    def get_user_by_email(self, email):
        for u in self.users:
            if u.email == email:
                return u
        return None
    
    def get_course_by_title(self,title):
        for c in self.courses:
            if c.title == title:
                return c
        return None

    def number_of_users(self):
        return len(self.users)
    
    def number_of_courses(self):
        return len(self.courses)
    
    def calculate_price(self, course: Course, user: User):
        price = course.price
        if user.is_premium:
            price = price * 0.8
        if user.region == "PL":
            price = price - 10
        return max(0.0, float(price))

    def enroll(self, user: User, course: Course):
        if user.email == "invalid":
            return "User data is invalid"
        if course.title in user.saved_courses:
            return "User already enrolled"
        if not course.is_published:
            return "Course not published"
        
        user.saved_courses.append(course.title)
        self.email_client.send(user.email, f"Welcome to {course.title}")
        return True

    def add_review(self, user: User, course_title, rating, comment):
        if rating < 1 or rating > 5:
            return "Rating must be 1-5"
        if course_title not in user.saved_courses:
            return "User must buy course first"
        
        course = next((c for c in self.courses if c.title == course_title), None)
        
        if course is None:
            return "Course does not exist"
        
        review = {
            "user": user.email, 
            "course": course_title, 
            "rating": rating, 
            "comment": comment
        }
        course.add_review(review)
        return review
    
    def delete_user(self, email):
        user = self.get_user_by_email(email)
        if user:
            self.users.remove(user)
            return True
        return False

    def delete_course(self, title):
        course = self.get_course_by_title(title)
        if course:
            self.courses.remove(course)
            return True
        return False