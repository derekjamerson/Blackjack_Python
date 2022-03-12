from player import Player


class HumanPlayer(Player):
    def choose_to_stay(self):
        response = input('Enter \'S\' to stay, \'H\' to hit: ').lower()
        while True:
            if response == 's':
                return True
            elif response == 'h':
                return False
            response = input(
                'INVALID OPTION\n' 'Enter \'S\' to stay, \'H\' to hit: '.lower()
            )
