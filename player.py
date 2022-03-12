class Player:
    def __init__(self):
        self.hand = []

    @property
    def score(self):
        raw_score = sum(sorted(self.hand, reverse=True))
        ace_counter = 0
        num_of_aces = len([x for x in self.hand if x.value == 1])
        while raw_score > 21 and ace_counter < num_of_aces:
            ace_counter += 1
            raw_score -= 10
        return raw_score

    def choose_to_stay(self):
        raise Exception("Not Implemented")
