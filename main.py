from random import shuffle


class Card:
    def __init__(self, v, s):
        self.value = v
        self.suit = s

    def __repr__(self):
        return self.value + " of " + self.suit


class Deck:
    suits = ["Clubs", "Hearts", "Spades", "Diamonds"]

    values = [None, None, "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self):
        self.cards = []
        for i in range(2, 15):
            for j in range(4):
                self.cards.append(Card(self.values[i], self.suits[j]))
        shuffle(self.cards)


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
        print("Player: %s" % self.player.hand)
        print("Dealer: [%s, HIDDEN]" % self.dealer.hand[0])

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

    def clean_up(self):
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
            self.clean_up()


if __name__ == '__main__':
    game = Game()
    game.play_game()
