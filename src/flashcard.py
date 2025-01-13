from file_management import File_Management

class Flashcard():
    def __init__(self, id, front, back, front_has_lines = False, front_lines = None, back_has_lines = False, back_lines = None):
        self.card_id = id
        self.front = front
        self.back = back
        self.front_has_lines = front_has_lines
        self.front_lines = front_lines
        self.back_has_lines = back_has_lines
        self.back_lines = back_lines