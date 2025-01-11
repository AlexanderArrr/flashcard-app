from file_management import File_Management

class Flashcard():
    def __init__(self, id, front, back, front_has_image = False, front_image = "", back_has_image = False, back_image = ""):
        self.card_id = id
        self.front = front
        self.back = back
        self.front_has_image = front_has_image
        self.front_image = front_image
        self.back_has_image = back_has_image
        self.back_image = back_image