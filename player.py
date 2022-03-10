class Player:
    def __init__(self):
        self.hand = []

    @property
    def score(self):
        return sum(sorted(self.hand, reverse=True))
