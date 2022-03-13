from unittest import TestCase

from card import Card
from player.dealer_player import DealerPlayer


class DealerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.dealer = DealerPlayer()

    def assert_dealer_choice(self, cards, *, choose_to_stay):
        self.dealer.hand = []
        for card in cards:
            self.dealer.hand.append(Card(card, 1))
        self.assertEqual(self.dealer.choose_to_stay(), choose_to_stay)

    def test_game_dealer_turn(self):
        self.assert_dealer_choice([2, 5], choose_to_stay=False)
        self.assert_dealer_choice([4, 4, 8], choose_to_stay=False)
        self.assert_dealer_choice([3, 3, 3, 3, 5], choose_to_stay=True)
        self.assert_dealer_choice([11, 12], choose_to_stay=True)
