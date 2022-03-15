import io
import sys
from functools import partial
from unittest import TestCase, mock

from card import Card
from game import Game


class GameTestCase(TestCase):
    @classmethod
    def setUp(cls):
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

    def assert_console_output(self, method_to_run, expected_output):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        method_to_run()
        sys.stdout = sys.__stdout__
        self.assertEqual(expected_output, captured_output.getvalue())

    def test_game_print_game(self):
        player_hand = [Card(2, 1), Card(2, 2)]
        dealer_hand = [Card(3, 1), Card(3, 2)]
        self.game.human_player.hand = player_hand
        self.game.dealer.hand = dealer_hand
        expected_string = f'Player: 4 {player_hand}\n' f'Dealer: 6 {dealer_hand}\n'
        self.assert_console_output(partial(self.game.print_game, True), expected_string)
        expected_string = (
            f'Player: 4 {player_hand}\n' f'Dealer: ?? [{dealer_hand[0]}, ??]\n'
        )
        self.assert_console_output(
            partial(self.game.print_game, False), expected_string
        )

    def test_game_decide_winner(self):
        self.game.human_player.hand = [Card(10, 1), Card(11, 2)]
        self.game.dealer.hand = [Card(10, 2), Card(8, 1)]
        self.assertTrue(self.game.decide_winner())
        self.game.dealer.hand = [Card(10, 1), Card(11, 2), Card(12, 3)]
        self.assertTrue(self.game.decide_winner())
        self.game.dealer.hand = [Card(10, 0), Card(12, 2)]
        self.assertTrue(not self.game.decide_winner())
        self.assertEqual(self.game.score, 1)

    def test_game_print_score(self):
        self.game.human_player.hand = [Card(10, 1), Card(10, 0)]
        self.game.dealer.hand = [Card(10, 2), Card(9, 0)]
        expected_string = '*** You Win ***\n Score: 1\n'
        self.assert_console_output(self.game.print_score, expected_string)
        self.game.dealer.hand = [Card(11, 1), Card(12, 0)]
        expected_string = '*** You Lose ***\n Score: 0\n'
        self.assert_console_output(self.game.print_score, expected_string)

    def test_game_shuffle(self):
        self.game.deck.cards.pop(0)
        self.game.shuffle_if_needed()
        self.assertEqual(len(self.game.deck.cards), 51)
        del self.game.deck.cards[:40]
        self.game.shuffle_if_needed()
        self.assertEqual(len(self.game.deck.cards), 52)

    # @mock.patch('player.human_player.HumanPlayer.choose_to_stay', return_value=True)
    # @mock.patch('game.Game.print_game', return_value=None)
    # @mock.patch('game.Game.deal_card')
    # def test_game_turn_player(self, mock1, mock2, mock3):
    #     self.game.human_player.hand = [Card(11, 1), Card(10, 0), Card(13, 3)]
    #     self.assertEqual(self.game.turn_player(), 30)
    #     mock1.return_value.get = False
    #     mock3.wraps = self.game.human_player.hand.append(Card(3, 1))
    #     self.assertEqual(self.game.turn_player(), 33)
    #     mock1.return_value.get = False
    #     self.game.human_player.hand = [Card(2, 0), Card(3, 3)]
    #     mock3.wraps = self.game.human_player.hand.append(Card(2, 1))
    #     self.assertEqual(self.game.turn_player(), 25)
