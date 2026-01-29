class Course:
    def __init__(self,  title, price, materials_count,owner):
        self.title = title
        self.price = price
        self.materials_count = materials_count
        self.is_published = False
        self.owner=owner
        self.reviews=[]

    def publishCourse(self):
        self.is_published=True

    def hideCourse(self):
        self.is_published=False
    def add_review(self,review):
        self.reviews.append(review)
    def update_data(self, title=None, price=None, materials_count=None):
        if title:
            self.title = title
        if price is not None:
            self.price = price
        if materials_count is not None:
            self.materials_count = materials_count