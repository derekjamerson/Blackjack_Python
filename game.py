from deck import Deck
from player import DealerPlayer, HumanPlayer


class Game:
    def __init__(self):
        self.deck = Deck()
        self.human_player = HumanPlayer()
        self.dealer = DealerPlayer()
        self.score = 0

    def deal_card(self, receiver):
        receiver.hand.append(self.deck.cards.pop(0))

    def deal_game(self):
        self.deal_card(self.human_player)
        self.deal_card(self.dealer)
        self.deal_card(self.human_player)
        self.deal_card(self.dealer)

    def print_game(self, game_is_over):
        d_score, dealer_card = self.get_dealer_hand_info(game_is_over)
        print(
            f'Player: {self.human_player.score} {self.human_player.hand}\n'
            f'Dealer: {d_score} [{self.dealer.hand[0]}, {dealer_card}]'
        )

    def get_dealer_hand_info(self, game_is_over):
        if game_is_over:
            return self.dealer.score, self.dealer.hand[1]
        return '??', '??'

    def decide_winner(self):
        p_score = self.human_player.score
        d_score = self.dealer.score
        if d_score < p_score <= 21 or p_score <= 21 < d_score:
            self.score += 1
            return True
        self.score -= 1
        return False

    def print_score(self):
        if self.decide_winner():
            output = '*** You Win ***'
        else:
            output = '*** You Lose ***'
        print(f'{output}\n Score: {self.score}')

    def shuffle_if_needed(self):
        if len(self.deck.cards) < 26:
            self.deck = Deck()

    def discard_hands(self):
        self.human_player.hand.clear()
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
            self.print_game(True)
            self.print_score()
            self.discard_hands()

    def turn_dealer(self):
        while True:
            if self.dealer.choose_to_stay():
                break
            self.deal_card(self.dealer)

    def turn_player(self):
        while True:
            self.print_game(False)
            if self.human_player.choose_to_stay():
                return self.human_player.score
            else:
                self.deal_card(self.human_player)
                if self.human_player.score > 21:
                    return self.human_player.score
