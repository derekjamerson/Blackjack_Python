class Card:
    def __init__(self, v, s):
        self.value = v
        self.suit = s

    def __repr__(self):
        return f'{self.get_value_name()}{self.suit}'

    def get_value_name(self):
        match self.value:
            case 1:
                return 'A'
            case 11:
                return 'J'
            case 12:
                return 'Q'
            case 13:
                return 'K'
            case _:
                return str(self.value)
