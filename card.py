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

    @property
    def score(self):
        if self.value > 10:
            return 10
        elif self.value == 1:
            return 11
        return self.value

    @property
    def value_name(self):
        return self.face_value_mapping.get(self.value, self.value)

    def __repr__(self):
        return f'{self.value_name}{self.suit}'

    def __lt__(self, other):
        return self.value < other.value

    def __radd__(self, other):
        if self.score + other > 21:
            return self.score + other - 10
        return self.score + other
