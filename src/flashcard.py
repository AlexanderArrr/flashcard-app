class Flashcard():
    def __init__(self, index, front, back, front_has_lines = False, front_lines = None, back_has_lines = False, back_lines = None):
        self.index = index
        self.front = front
        self.back = back
        self.front_has_lines = front_has_lines
        self.front_lines = front_lines
        self.back_has_lines = back_has_lines
        self.back_lines = back_lines

    def get_fc(self):
        fc_dict = {
            "index": self.index,
            "front": self.front,
            "back": self.back,
            "front_has_lines": self.front_has_lines,
            "front_lines": self.front_lines,
            "back_has_lines": self.back_has_lines,
            "back_lines": self.back_lines
        }
        return fc_dict

    def get_fc_element(self, element):
        match element:
            case "index":
                return self.index
            case "front":
                return self.front
            case "back":
                return self.back
            case "front_has_lines":
                return self.front_has_lines
            case "front_lines":
                return self.front_lines
            case "back_has_lines":
                return self.back_has_lines
            case "back_lines":
                return self.back_lines
            case _:
                return None