class User:
    def __init__(self, email, age, region="PL"):
        self.age = age
        self.region = region
        self.is_premium = False
        self.saved_courses = []

        if age < 18 or "@" not in email:
            self.email = "invalid"
        else:
            self.email = email

    def toggle_premium(self):
        self.is_premium = not self.is_premium