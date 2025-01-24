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
        
    def save_json_file(self, fcs_name, fcs_dict):
        path = self.flashcards_path.joinpath(fcs_name.lower() + ".json")
        if not path.exists():
            self.create_json_file(path, self.__create_json_from_dict(fcs_dict))
            return
        f = open(path, 'w')
        f.write(self.__create_json_from_dict(fcs_dict))
        f.close()

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
    
    def create_new_flashcards(self, name):
        fc_list = []
        new_fcs = fcs(name, fc_list)
        json_content = self.__create_json_from_dict(new_fcs.get_fcs())
        self.create_json_file(self.flashcards_path.joinpath(name.lower() + '.json'), json_content)

    def check_existing_json_file(self, name):
        path_to_check = self.flashcards_path.joinpath(name.lower() + '.json')
        if path_to_check.exists():
            return False
        return True

    def __create_default_cards(self):
        json_dict = {
            "index": 0,
            "front": "A default text showing the front.",
            "back": "A default text showing the back.",
            "front_has_lines": True,
            "front_lines": [{"coords": [586.0, 43.0, 586.0, 43.0, 586.0, 44.0, 587.0, 50.0, 588.0, 58.0, 590.0, 68.0, 591.0, 78.0, 593.0, 90.0, 594.0, 99.0, 596.0, 108.0, 597.0, 117.0, 597.0, 120.0], "color": "black", "width": 2}, {"coords": [631.0, 40.0, 631.0, 40.0, 631.0, 41.0, 631.0, 43.0, 631.0, 52.0, 632.0, 62.0, 633.0, 72.0, 634.0, 82.0, 635.0, 90.0, 636.0, 96.0, 637.0, 102.0, 637.0, 107.0, 638.0, 111.0, 638.0, 112.0], "color": "black", "width": 2}, {"coords": [562.0, 83.0, 562.0, 83.0, 567.0, 84.0, 572.0, 84.0, 582.0, 84.0, 596.0, 84.0, 612.0, 84.0, 628.0, 84.0, 645.0, 84.0, 661.0, 84.0, 676.0, 84.0, 686.0, 84.0, 688.0, 84.0], "color": "black", "width": 2}],
            "back_has_lines": False,
            "back_lines": None
        }
        dict_list = [json_dict]
        default_cards = fcs("Default", dict_list)
        return default_cards

    def __create_json_from_dict(self, card_dict):
        return json.dumps(card_dict, indent=4)
    
    


    
