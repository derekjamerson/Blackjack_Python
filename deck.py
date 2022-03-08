from random import shuffle
from card import Card


class Deck:
    suits = ["Clubs", "Hearts", "Spades", "Diamonds"]

    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self):
        self.cards = []
        for suit in self.suits:
            for value in self.values:
                self.cards.append(Card(value, suit))
        shuffle(self.cards)
