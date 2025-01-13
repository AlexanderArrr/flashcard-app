from flashcard import Flashcard as fc

class Flashcards():
    def __init__(self, name, cards_list):
        self.cards_id = name.lower()
        self.cards_name = name
        self.cards_amount = len(cards_list)
        self.cards_list = self.cards_list_to_fc_objects(cards_list)

    def get_fcs(self):
        cards_list = self.fc_objects_to_cards_list(self.cards_list)
        fcs_dict = {
            "cards_id": self.cards_id,
            "cards_name": self.cards_name,
            "cards_amount": self.cards_amount,
            "cards_list": cards_list
        }
        return fcs_dict
    
    def get_fcs_element(self, element):
        match element:
            case "id":
                return self.cards_id
            case "name":
                return self.cards_name
            case "amount":
                return self.cards_amount
            case "list":
                return self.cards_list
            case _:
                return None

    def cards_list_to_fc_objects(self, cards_list):
        if cards_list is not None:
            new_list = []
            for card in cards_list:
                fc_obj = fc(card["index"],
                            card["front"],
                            card["back"],
                            card["front_has_lines"],
                            card["front_lines"],
                            card["back_has_lines"],
                            card["back_lines"])
                new_list.append(fc_obj)
            return new_list
    
    def fc_objects_to_cards_list(self, fc_objects_list):
        new_list = []
        for card in fc_objects_list:
            new_list.append(card.get_fc())
        return new_list

    def get_fc_by_index(self, index):
        if self.cards_list is not None:
            for card in self.cards_list:
                if card.index == index:
                    return card


