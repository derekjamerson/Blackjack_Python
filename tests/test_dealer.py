from unittest import TestCase

from card import Card
from player.dealer import Dealer


class PlayerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dealer = Dealer()

    def assert_dealer_choice(self, cards, choose_to_stay):
        self.dealer.hand = []
        for card in cards:
            self.dealer.hand.append(Card(card, 1))
        self.assertEqual(self.dealer.choose_to_stay(), choose_to_stay)

    def test_game_dealer_turn(self):
        self.assert_dealer_choice([2, 5], False)
        self.assert_dealer_choice([4, 4, 8], False)
        self.assert_dealer_choice([3, 3, 3, 3, 5], True)
        self.assert_dealer_choice([11, 12], True)
