from operator import attrgetter

from deck import Deck
from player import Player


class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Player()
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
        p_score = self.player.calculate_score()
        d_score = self.dealer.calculate_score()
        you_win = False
        if d_score < p_score <= 21 or p_score <= 21 < d_score:
            you_win = True
            self.score += 1
        else:
            you_win = False
            self.score -= 1
        final_string = ""
        if you_win:
            final_string = "*** YOU WIN ***"
        else:
            final_string = "*** YOU LOSE ***"
        print(final_string)
        print("Player: %s %s" % (p_score, self.player.hand))
        print("Dealer: %s %s" % (d_score, self.dealer.hand))
        print(final_string)
        print("Score: %s" % self.score)

    def discard_hands(self):
        self.player.hand.clear()
        self.dealer.hand.clear()

    def play_game(self):
        cards = self.deck.cards
        print("BlackJack")
        while True:
            player_did_not_bust = True
            response = input("Enter 'Q' to quit. Enter any key to play:").lower()
            if response == 'q':
                break
            if len(cards) < 26:
                print("Shuffling...")
                self.deck = Deck()
                cards = self.deck.cards
            self.deal_game()
            while True:
                self.print_game()
                response = input("Enter 'S' to stay, 'H' to hit: ").lower()
                match response:
                    case "s":
                        break
                    case "h":
                        self.deal_card(self.player)
                    case _:
                        print("Invalid option.")
                player_score = self.player.calculate_score()
                if player_score > 21:
                    self.game_over()
                    player_did_not_bust = False
                    break
            while player_did_not_bust:
                dealer_score = self.dealer.calculate_score()
                if dealer_score > 16:
                    break
                else:
                    self.deal_card(self.dealer)
            self.game_over()
            self.discard_hands()
