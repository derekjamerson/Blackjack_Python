class Card:
    def __init__(self, v, s):
        self.value = v
        self.suit = s
        self.score = self.get_score()

    def __repr__(self):
        return f'{self.get_value_name()}{self.suit}'

    def get_score(self):
        if self.value > 10:
            return 10
        elif self.value == 1:
            return 11
        else:
            return self.value

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
