from random import shuffle
from card import Card


class Deck:
    suits = ["\u2663", "\u2665", "\u2660", "\u2666"]

    values = range(1, 14)

    def __init__(self):
        self.cards = []
        for suit in self.suits:
            for value in self.values:
                self.cards.append(Card(value, suit))
        shuffle(self.cards)
