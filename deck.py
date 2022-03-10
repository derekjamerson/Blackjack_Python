from random import shuffle

from card import Card


class Deck:
    suits = ['Clubs', 'Hearts', 'Spades', 'Diamonds']

    values = [
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '10',
        'Jack',
        'Queen',
        'King',
        'Ace',
    ]

    def __init__(self):
        self.cards = []
        for suit in '♣♥♠♦':
            for value in range(1, 14):
                self.cards.append(Card(value, suit))
        shuffle(self.cards)
