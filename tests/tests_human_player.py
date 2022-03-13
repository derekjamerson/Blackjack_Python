from unittest import TestCase
from unittest.mock import patch

from player import HumanPlayer


class HumanPlayerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.player = HumanPlayer()

    @patch('builtins.input', side_effect=['s', 'h'])
    def test_human_player_choose_to_stay(self, side_effects):
        self.assertEqual(self.player.choose_to_stay(), True)
        self.assertEqual(self.player.choose_to_stay(), False)
