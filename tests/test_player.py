from unittest import TestCase

from card import Card
from player import Player


class PlayerTestCase(TestCase):
    player = None

    @classmethod
    def setUpClass(cls):
        cls.player = Player()

    def test_player_hand_2_2(self):
        first_value = 2
        second_value = 2
        self.player.hand = [Card(first_value, 1), Card(second_value, 2)]
        self.assertEqual(self.player.score, 4)

    def test_player_hand_10_10(self):
        first_value = 10
        second_value = 10
        self.player.hand = [Card(first_value, 1), Card(second_value, 2)]
        self.assertEqual(self.player.score, 20)

    def test_player_hand_10_a(self):
        first_value = 10
        second_value = 1
        self.player.hand = [Card(first_value, 1), Card(second_value, 2)]
        self.assertEqual(self.player.score, 21)

    def test_player_hand_k_k(self):
        first_value = 13
        second_value = 13
        self.player.hand = [Card(first_value, 1), Card(second_value, 2)]
        self.assertEqual(self.player.score, 20)

    def test_player_hand_a_a(self):
        first_value = 1
        second_value = 1
        self.player.hand = [Card(first_value, 1), Card(second_value, 2)]
        self.assertEqual(self.player.score, 12)

    def test_player_hand_j_q_k(self):
        first_value = 12
        second_value = 12
        third_value = 13
        self.player.hand = [
            Card(first_value, 1),
            Card(second_value, 2),
            Card(third_value, 3),
        ]
        self.assertEqual(self.player.score, 30)

    def test_player_hand_21_aces(self):
        self.player.hand = []
        for num in range(21):
            self.player.hand.append(Card(1, 3))
        self.assertEqual(self.player.score, 21)

    def test_player_hand_one_of_each(self):
        self.player.hand = []
        for num in range(13):
            self.player.hand.append(Card(num, 1))
        self.assertEqual(self.player.score, sum(range(13)) - 3)
