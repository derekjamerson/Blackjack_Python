from deck import Deck
from player import DealerPlayer, HumanPlayer


class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = HumanPlayer()
        self.dealer = DealerPlayer()
        self.score = 0

    def deal_card(self, receiver):
        receiver.hand.append(self.deck.cards.pop(0))

    def deal_game(self):
        self.deal_card(self.player)
        self.deal_card(self.dealer)
        self.deal_card(self.player)
        self.deal_card(self.dealer)

    def print_game(self):
        print(f'Player: {self.player.hand}')
        print(f'Dealer: [{self.dealer.hand[0]}, ??]')

    def decide_winner(self):
        p_score = self.player.score
        d_score = self.dealer.score
        if d_score < p_score <= 21 or p_score <= 21 < d_score:
            self.score += 1
            return True
        self.score -= 1
        return False

    def print_game_over(self, you_win):
        if you_win:
            final_string = '*** YOU WIN ***'
        else:
            final_string = '*** YOU LOSE ***'
        print(
            f'Player: {self.player.score} {self.player.hand}\n'
            f'Dealer: {self.dealer.score} {self.dealer.hand}\n'
            f'{final_string}\n'
            f'Score: {self.score}'
        )

    def shuffle_if_needed(self):
        if len(self.deck.cards) < 26:
            self.deck = Deck()

    def discard_hands(self):
        self.player.hand.clear()
        self.dealer.hand.clear()

    def play_game(self):
        while True:
            response = HumanPlayer.get_input_from_user(
                "Enter 'Q' to quit. 'P' to play:", ['q', 'p']
            )
            if response == 'q':
                break
            self.shuffle_if_needed()
            self.deal_game()
            if self.turn_player() <= 21:
                self.turn_dealer()
            you_win = self.decide_winner()
            self.print_game_over(you_win)
            self.discard_hands()

    def turn_dealer(self):
        while True:
            if self.dealer.choose_to_stay():
                break
            self.deal_card(self.dealer)

    def turn_player(self):
        while True:
            self.print_game()
            if self.player.choose_to_stay():
                return self.player.score
            else:
                self.deal_card(self.player)
                if self.player.score > 21:
                    return self.player.score
