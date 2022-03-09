class Card:
    face_value_mapping = {
        1: 'A',
        11: 'J',
        12: 'Q',
        13: 'K',
    }

    def __init__(self, v, s):
        self.suit = s
        self.value = v
        self.value_name = self.face_value_mapping.get(self.value, self.value)
        self.score = self.get_score()

    def __repr__(self):
        return f'{self.value_name}{self.suit}'

    def get_score(self):
        if self.value > 10:
            return 10
        elif self.value == 1:
            return 11
        else:
            return self.value


