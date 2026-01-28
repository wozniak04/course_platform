class Course:
    def __init__(self, id, title, price, materials_count, is_published=True):
        self.id = id
        self.title = title
        self.price = price
        self.materials_count = materials_count
        self.is_published = is_published