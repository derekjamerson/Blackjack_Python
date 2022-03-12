from dealer import Dealer
from deck import Deck
from player import Player


class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Dealer()
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

    def game_over(self):
        p_score = self.player.score
        d_score = self.dealer.score
        if d_score < p_score <= 21 or p_score <= 21 < d_score:
            you_win = True
            self.score += 1
        else:
            you_win = False
            self.score -= 1
        if you_win:
            final_string = '*** YOU WIN ***'
        else:
            final_string = '*** YOU LOSE ***'
        print(final_string)
        print(f'Player: {p_score} {self.player.hand}')
        print(f'Dealer: {d_score} {self.dealer.hand}')
        print(final_string)
        print(f'Score: {self.score}')

    def discard_hands(self):
        self.player.hand.clear()
        self.dealer.hand.clear()

    def play_game(self):
        cards = self.deck.cards
        print('BlackJack')
        while True:
            response = input('Enter \'Q\' to quit. Enter any key to play:').lower()
            if response == 'q':
                break
            if len(cards) < 26:
                print('Shuffling...')
                self.deck = Deck()
                cards = self.deck.cards
            self.deal_game()
            if self.turn_player() <= 21:
                self.turn_dealer()
            self.game_over()
            self.discard_hands()

    def turn_dealer(self):
        while True:
            if self.dealer.choose_to_stay():
                break
            self.deal_card(self.dealer)

    def turn_player(self):
        while True:
            self.print_game()
            response = input('Enter \'S\' to stay, \'H\' to hit: ').lower()
            if response == 's':
                return self.player.score
            elif response == 'h':
                self.deal_card(self.player)
                if self.player.score > 21:
                    return self.player.score
            else:
                print('Invalid option.')
