from unittest import TestCase

from card import Card
from player import Player


class PlayerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.player = Player()

    def assert_hand_score(self, cards, score):
        self.player.hand = []
        for card in cards:
            self.player.hand.append(Card(card, 1))
        self.assertEqual(self.player.score, score)

    def test_player_hand_number_cards(self):
        self.assert_hand_score([2, 2], 4)
        self.assert_hand_score([2, 3, 4, 5, 6, 7, 8, 9], 44)
        self.assert_hand_score([10, 10], 20)
        self.assert_hand_score([10, 9], 19)

    def test_player_hand_faces(self):
        self.assert_hand_score([11, 11], 20)
        self.assert_hand_score([11, 12, 13], 30)

    def test_player_hand_aces(self):
        self.assert_hand_score([1, 1], 12)
        self.assert_hand_score([1, 10], 21)
        self.assert_hand_score([1, 1, 1, 1, 1], 15)
