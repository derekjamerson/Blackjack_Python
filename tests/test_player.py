from unittest import TestCase

from card import Card
from player import Player


class PlayerTestCase(TestCase):
    def test_all_possible_two_number_card_hand_combinations(self):
        player = Player()
        for first in range(2, 10):
            for second in range(first, 10):
                player.hand = [Card(first, 1), Card(second, 2)]
                self.assertEqual(
                    player.score,
                    first + second,
                    f'Error: [{first}, {second}] != {player.score}',
                )
