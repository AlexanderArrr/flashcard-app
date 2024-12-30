import json
from pathlib import Path

class File_Management():
    def __init__(self):
        self.base_path = Path(__file__).parent.resolve()
        if not self.base_path.joinpath('flashcards').exists():
            self.base_path.mkdir('flashcards')
        self.flashcards_path = self.base_path.joinpath('flashcards').resolve()

        if not self.flashcards_path.joinpath('default_card.json').exists():
            self.__create_default()

    def __create_default(self):
        default_dict = {
            "cards_name" : "Default",
            "cards_id" : "default",
            "cards_amount" : 0,
            "cards_list" : [],
        }
        
        json_string = self.__create_json_from_dict(default_dict)

    def __create_json_from_dict(self, card_dict):
        return json.dumps(card_dict)