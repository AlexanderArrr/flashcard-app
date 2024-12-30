from file_management import File_Management
from flashcard import Flashcard

class Flashcards():
    def __init__(self, name):
        self.cards_name = name
        self.cards_id = name.lower()
        self.cards_amount = 0
        self.cards_list = []


