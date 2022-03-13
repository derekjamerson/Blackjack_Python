from player import Player


class DealerPlayer(Player):
    def choose_to_stay(self):
        if self.score > 16:
            return True
        return False
