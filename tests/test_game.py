import io
import sys
from functools import partial
from unittest import TestCase, mock

from card import Card
from game import Game


class GameTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.game = Game()

    @staticmethod
    def num_list_to_cards(num_list):
        hand = []
        for num in num_list:
            hand.append(Card(num, 1))
        return hand

    def assert_dealer_turn(self, cards, should_hit):
        self.game.dealer.hand = self.num_list_to_cards(cards)
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

    def assert_decided_winner(self, p_hand, d_hand, player_win):
        old_score = self.game.score
        self.game.human_player.hand = self.num_list_to_cards(p_hand)
        self.game.dealer.hand = self.num_list_to_cards(d_hand)
        self.assertEqual(self.game.decide_winner(), player_win)
        if player_win:
            self.assertEqual(self.game.score, old_score + 1)
        else:
            self.assertEqual(self.game.score, old_score - 1)

    def test_game_decide_winner(self):
        p_hand = [10, 11]
        self.assert_decided_winner(p_hand, [10, 8], True)
        self.assert_decided_winner(p_hand, [10, 11, 12], True)
        self.assert_decided_winner(p_hand, [10, 12], False)

    def assert_printed_score(self, p_hand, d_hand, player_win):
        self.game.human_player.hand = []
        self.game.dealer.hand = []
        for c in p_hand:
            self.game.human_player.hand.append(Card(c, 1))
        for c in d_hand:
            self.game.dealer.hand.append(Card(c, 1))
        if player_win:
            output = '*** You Win ***\n Score: 1\n'
        else:
            output = '*** You Lose ***\n Score: 0\n'
        self.assert_console_output(self.game.print_score, output)

    def test_game_print_score(self):
        p_hand = [10, 10]
        self.assert_printed_score(p_hand, [10, 9], True)
        self.assert_printed_score(p_hand, [11, 12], False)

    def assert_need_to_shuffle(self, should_be_shuffled):
        self.game.shuffle_if_needed()
        self.assertEqual(len(self.game.deck.cards) == 52, should_be_shuffled)

    def test_game_shuffle(self):
        self.game.deck.cards.pop(0)
        self.assert_need_to_shuffle(False)
        del self.game.deck.cards[:40]
        self.assert_need_to_shuffle(True)

    @mock.patch('game.Game.play_again', side_effect=[True, False])
    def test_game_play_again(self, *args):
        self.assertIsNone(self.game.play_game())

    @mock.patch('game.Game._turn_player', side_effect=[None, 1])
    def test_game_turn_player_loop(self, *args):
        self.assertEqual(self.game.turn_player(), 1)

    @mock.patch('game.Game.deal_card')
    @mock.patch(
        'player.human_player.HumanPlayer.choose_to_stay',
        side_effect=[True, False, False],
    )
    @mock.patch('game.Game.print_game', return_value=None)
    def test_game_player_turn(self, mock_deal, *args):
        self.game.human_player.hand = [Card(10, 2), Card(2, 0)]
        self.assertEqual(self.game._turn_player(), 12)
        self.game.human_player.hand = [Card(10, 2), Card(11, 0)]
        mock_deal.return_value = self.game.human_player.hand.append(Card(12, 3))
        self.assertEqual(self.game._turn_player(), 30)
        self.game.human_player.hand = [Card(2, 2), Card(3, 0), Card(12, 4)]
        self.assertIsNone(self.game._turn_player())

    @mock.patch(
        'player.human_player.HumanPlayer.get_input_from_user', side_effect=['q', 'f']
    )
    def test_game_quit_game(self, *args):
        self.assertFalse(self.game.quit_game())
        self.assertTrue(self.game.quit_game())

    @mock.patch('game.Game.print_game', return_value=None)
    @mock.patch('game.Game.print_score', return_value=None)
    def test_game_post_game(self, *args):
        self.game.post_game()
        self.assertEqual(len(self.game.human_player.hand), 0)
        self.assertEqual(len(self.game.dealer.hand), 0)

    # THIS IS 63-67
    # @mock.patch('game.Game.quit_game', side_effect=[True, False])
    # @mock.patch('game.Game.base_game', return_value=None)
    # @mock.patch('game.Game.post_game', return_value=None)
    # def test_game_play_again(self, *args):
    #     self.assertFalse(self.game.play_again())
    #     self.assertTrue(self.game.play_again())
    #
    # THIS IS 80-81
    # @mock.patch('game.Game.turn_player', return_value=22)
    # @mock.patch('game.Game.turn_dealer', return_value='dealer')
    # def test_game_base_game(self, *args):
    #     # self.assertIsNone(self.game.base_game())
    #     self.assertEqual(self.game.base_game(), 'dealer')
