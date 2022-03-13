from unittest import TestCase

from card import Card
from game import Game


class GameTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = Game()

    def assert_dealer_turn(self, cards, should_hit):
        self.game.dealer.hand = []
        for card in cards:
            self.game.dealer.hand.append(Card(card, 1))
        self.game.turn_dealer()
        if should_hit:
            self.assertGreater(len(self.game.dealer.hand), len(cards))
        else:
            self.assertEqual(len(self.game.dealer.hand), len(cards))

    def test_game_deal_hands(self):
        self.game.deal_game()
        self.assertEqual(len(self.game.human_player.hand), 2)
        self.assertEqual(len(self.game.dealer.hand), 2)

    def test_game_discard_hands(self):
        self.game.discard_hands()
        self.assertEqual(len(self.game.human_player.hand), 0)
        self.assertEqual(len(self.game.dealer.hand), 0)

    def test_game_dealer_turn(self):
        self.assert_dealer_turn([2, 5], True)
        self.assert_dealer_turn([4, 4, 8], True)
        self.assert_dealer_turn([3, 3, 3, 3, 5], False)
        self.assert_dealer_turn([11, 12], False)
