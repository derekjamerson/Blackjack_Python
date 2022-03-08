class Player:
    def __init__(self):
        self.hand = []

    def calculate_score(self):
        num_of_aces = 0
        calc_score = 0
        for c in self.hand:
            if c.value == 'Ace':
                num_of_aces += 1
                calc_score += 11
            elif c.value in ["Jack", "Queen", "King"]:
                calc_score += 10
            else:
                calc_score += int(c.value)
        while calc_score > 21:
            if num_of_aces > 0:
                calc_score -= 10
                num_of_aces -= 1
            else:
                break
        return calc_score
