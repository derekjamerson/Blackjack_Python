class Card:
    def __init__(self, v, s):
        self.value = v
        self.suit = s

    def __repr__(self):
        return f'{self.value} of {self.suit}'

