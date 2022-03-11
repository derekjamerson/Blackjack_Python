from unittest import TestCase

from card import Card
from game import Game


class CardTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = Game()

    def test_game_deal_hands(self):
        self.game.deal_game()
        player_hand_count = len(self.game.player.hand)
        dealer_hand_count = len(self.game.dealer.hand)
        self.assertEqual(player_hand_count, 2)
        self.assertEqual(dealer_hand_count, 2)

    def test_game_discard_hands(self):
        self.game.discard_hands()
        player_hand_count = len(self.game.player.hand)
        dealer_hand_count = len(self.game.dealer.hand)
        self.assertEqual(player_hand_count, 0)
        self.assertEqual(dealer_hand_count, 0)

    def test_game_dealer_turn_5(self):
        self.game.dealer.hand = [Card(2, 1), Card(3, 2)]
        self.game.turn_dealer()
        self.assertGreater(self.game.dealer.calculate_score(), 5)

    def test_game_dealer_turn_16(self):
        self.game.dealer.hand = [Card(6, 1), Card(1, 2)]
        self.game.turn_dealer()
        self.assertGreater(self.game.dealer.calculate_score(), 16)

    def test_game_dealer_turn_17(self):
        self.game.dealer.hand = [Card(6, 1), Card(1, 2)]
        self.game.turn_dealer()
        self.assertEqual(self.game.dealer.calculate_score(), 17)

    def test_game_dealer_turn_25(self):
        self.game.dealer.hand = [Card(11, 1), Card(12, 2), Card(13, 3)]
        self.game.turn_dealer()
        self.assertEqual(self.game.dealer.calculate_score(), 30)
