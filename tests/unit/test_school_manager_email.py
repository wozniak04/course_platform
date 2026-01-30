import unittest
from unittest.mock import MagicMock
from src.schoolmanager import SchoolManager
from src.user import User

class TestSchoolManagerEmail(unittest.TestCase):
    def setUp(self):
        self.manager = SchoolManager()
        self.manager.email_client = MagicMock()

    def test_notify_users_sends_emails_to_all(self):
        u1 = User("student1@test.pl", 20)
        u2 = User("student2@test.pl", 22)
        self.manager.register_user(u1)
        self.manager.register_user(u2)
        
        message = "Zniżka 50% na kurs Pythona!"

        count = self.manager.notify_users_about_promotion(message)


        self.assertEqual(count, 2)

        self.assertEqual(self.manager.email_client.send.call_count, 2)
        

        self.manager.email_client.send.assert_any_call("student1@test.pl", message)
        self.manager.email_client.send.assert_any_call("student2@test.pl", message)

    def test_enroll_sends_welcome_email(self):
        from src.course import Course
        
        user = User("jan@kowalski.pl", 25)
        course = Course("Java", 100, 10, "Admin")
        course.publishCourse() 
        
        self.manager.enroll(user, course)

        self.manager.email_client.send.assert_called_once_with(
            "jan@kowalski.pl", 
            "Welcome to Java"
        )