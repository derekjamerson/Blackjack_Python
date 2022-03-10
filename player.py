from operator import attrgetter


class Player:
    def __init__(self):
        self.hand = []

    def calculate_score(self):
        self.hand.sort(key=attrgetter('value'), reverse=True)
        hand_score = 0
        for c in self.hand:
            if c.score == 11 and hand_score > 10:
                hand_score += 1
            else:
                hand_score += c.score
        return hand_score
