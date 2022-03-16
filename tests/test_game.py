import io
import sys
from contextlib import contextmanager
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

    def assert_dealer_turn(self, d_cards, should_hit):
        self.game.dealer.hand = self.num_list_to_cards(d_cards)
        self.game.turn_dealer()
        if should_hit:
            self.assertGreater(len(self.game.dealer.hand), len(d_cards))
        else:
            self.assertEqual(len(self.game.dealer.hand), len(d_cards))

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

    @contextmanager
    def capture_console_output(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        yield captured_output
        sys.stdout = sys.__stdout__

    def assert_printed_game(self, p_cards, d_cards, game_over):
        self.game.human_player.hand = self.num_list_to_cards(p_cards)
        self.game.dealer.hand = self.num_list_to_cards(d_cards)
        if game_over:
            expected_string = (
                f'Player: 4 {self.game.human_player.hand}\n'
                f'Dealer: 6 {self.game.dealer.hand}\n'
            )
        else:
            expected_string = (
                f'Player: 4 {self.game.human_player.hand}\n'
                f'Dealer: ?? [{self.game.dealer.hand[0]}, ??]\n'
            )
        with self.capture_console_output() as captured_output:
            self.game.print_game(game_over)
        self.assertEqual(captured_output.getvalue(), expected_string)

    def test_game_print_game(self):
        self.assert_printed_game([2, 2], [3, 3], False)
        self.assert_printed_game([2, 2], [3, 3], True)

    def assert_decided_winner(self, p_cards, d_cards, player_win):
        old_score = self.game.score
        self.game.human_player.hand = self.num_list_to_cards(p_cards)
        self.game.dealer.hand = self.num_list_to_cards(d_cards)
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

    def assert_printed_score(self, p_cards, d_cards, player_win):
        self.game.human_player.hand = self.num_list_to_cards(p_cards)
        self.game.dealer.hand = self.num_list_to_cards(d_cards)
        if player_win:
            expected_string = '*** You Win ***\n Score: 1\n'
        else:
            expected_string = '*** You Lose ***\n Score: 0\n'
        with self.capture_console_output() as captured_output:
            self.game.print_score()
        self.assertEqual(captured_output.getvalue(), expected_string)

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

    @mock.patch('game.Game._turn_player', side_effect=[None, 1])
    def test_game_turn_player_loop(self, *args):
        self.assertEqual(self.game.turn_player(), 1)

    @mock.patch('game.Game.deal_card')
    @mock.patch('player.human_player.HumanPlayer.choose_to_stay')
    @mock.patch('game.Game.print_game', return_value=None)
    def assert_player_score(
        self,
        mock_deal,
        mock_stay,
        args,
        *,
        p_cards,
        deal_card=None,
        choose_stay,
        expected,
    ):
        self.game.human_player.hand = self.num_list_to_cards(p_cards)
        if deal_card is not None:
            mock_deal.return_value = self.game.human_player.hand.append(
                Card(deal_card, 1)
            )
        mock_stay.return_value = choose_stay
        self.assertEqual(self.game._turn_player(), expected)

    def test_game_player_turn(self):
        self.assert_player_score(p_cards=[10, 2], choose_stay=True, expected=12)
        self.assert_player_score(
            p_cards=[10, 11], deal_card=12, choose_stay=False, expected=30
        )
        self.assert_player_score(
            p_cards=[2, 3, 4], deal_card=5, choose_stay=False, expected=None
        )

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

    @mock.patch('game.Game.turn_player', side_effect=[22, 21])
    @mock.patch('game.Game.turn_dealer')
    def test_game_base_game_no_dealer_turn(self, mock_dealer, *args):
        self.game.base_game()
        mock_dealer.assert_not_called()
        self.game.base_game()
        mock_dealer.assert_called()

    @mock.patch('game.Game.base_game', return_value=None)
    @mock.patch('game.Game.post_game', return_value=None)
    @mock.patch('game.Game.quit_game', side_effect=[True, False])
    def test_game_play_again(self, *args):
        self.assertFalse(self.game.play_again())
        self.assertTrue(self.game.play_again())

    @mock.patch('game.Game.play_again', side_effect=[True, False])
    def test_game_play_game(self, *args):
        self.assertIsNone(self.game.play_game())
