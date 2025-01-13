import json
from pathlib import Path
from flashcards import Flashcards as fcs
from flashcard import Flashcard as fc

class File_Management():
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.resolve()
        self.flashcards_path = self.base_path.joinpath('flashcards').resolve()
        self.default_flashcard_path = self.flashcards_path.joinpath('default.json')
            
    def create_flashcards_folder(self):
        if not self.flashcards_path.exists():
            self.flashcards_path.mkdir()

    def create_default_flashcard(self):
        if not self.default_flashcard_path.exists():
            default_cards = self.__create_default_cards()
            json_content = self.__create_json_from_dict(default_cards.get_fcs())
            self.create_json_file(self.default_flashcard_path, json_content)

    def create_json_file(self, path, json_content):
        if not path.exists():
            f = open(path, 'w')
            f.write(json_content)
            f.close()
    
    def read_json_file(self, path):
        if path.exists():
            f = open(path, 'r')
            dict_json = json.load(f)
            f.close()
            return dict_json

    def list_flashcards_folder(self):
        flashcards_list = []
        if self.flashcards_path.exists():
            for child in self.flashcards_path.iterdir():
                if child.suffix == '.json':
                    flashcards_list.append(self.get_flashcards_name(child))
        return flashcards_list

    def get_flashcards_name(self, path):
        if path.exists():
            dict = self.read_json_file(path)
            return dict["cards_name"]
    
    def get_flashcards(self, name):
        path = self.flashcards_path.joinpath(name.lower() + ".json")
        if path.exists():
            dict_json = self.read_json_file(path)
            flashcards = fcs(dict_json["cards_name"], dict_json["cards_list"])
            return flashcards
        else:
            print("The specified path does not exist!")

    def __create_default_cards(self):
        json_dict = {
            "index": 0,
            "front": "A default text showing the front.",
            "back": "A default text showing the back.",
            "front_has_lines": False,
            "front_lines": None,
            "back_has_lines": False,
            "back_lines": None
        }
        dict_list = [json_dict]
        default_cards = fcs("Default", dict_list)
        return default_cards

    def __create_json_from_dict(self, card_dict):
        return json.dumps(card_dict, indent=4)
    
    


    
