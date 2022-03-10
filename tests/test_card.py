from unittest import TestCase
from card import Card


class CardTestCase(TestCase):
    def test_str_method_returns_text_for_card(self):
        card = Card(v=1, s="Spades")
        self.assertEqual(repr(card), "1 of Spades")
