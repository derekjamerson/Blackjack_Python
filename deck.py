from random import shuffle
from card import Card


class Deck:
    def __init__(self):
        self.cards = []
        for suit in '♣♥♠♦':
            for value in range(1, 14):
                self.cards.append(Card(value, suit))
        shuffle(self.cards)
