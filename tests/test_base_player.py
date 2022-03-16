from unittest import TestCase

from player import Player


class PlayerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.player = Player()

    def test_player_choose_to_stay(self):
        with self.assertRaises(NotImplementedError):
            self.player.choose_to_stay()
