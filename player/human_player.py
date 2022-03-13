from player import Player


class HumanPlayer(Player):
    @staticmethod
    def get_input_from_user(input_string, valid_options):
        error_string = f'Invalid Option\n {input_string}'
        while True:
            response = input(input_string).lower()
            if response in valid_options:
                return response
            input_string = error_string

    def choose_to_stay(self):
        input_string = "Enter 'S' to stay, 'H' to hit: "
        valid_options = ['s', 'h']
        return self.get_input_from_user(input_string, valid_options) == 's'
