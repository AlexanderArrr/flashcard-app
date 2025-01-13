import json
from pathlib import Path

class File_Management():
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.resolve()
        self.flashcards_path = self.base_path.joinpath('flashcards').resolve()
        self.default_flashcard_path = self.flashcards_path.joinpath('default_card.json')
            
    def create_flashcards_folder(self):
        if not self.flashcards_path.exists():
            self.flashcards_path.mkdir()

    def create_default_flashcard(self):
        if not self.default_flashcard_path.exists():
            default_cards_dict = self.__create_default_cards()
            json_content = self.__create_json_from_dict(default_cards_dict)
            self.create_json_file(self.default_flashcard_path, json_content)

    def create_json_file(self, path, json_content):
        if not path.exists():
            f = open(path, 'w')
            f.write(json_content)
            f.close()

    def __create_default_cards(self):
        default_cards_dict = {
            "cards_name": "Default", 
            "cards_id": "zzzdefault", 
            "cards_amount": 0, 
            "cards_list": [], 
        }
        return default_cards_dict

    def __create_json_from_dict(self, card_dict):
        return json.dumps(card_dict, indent=4)