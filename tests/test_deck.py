from unittest import TestCase

from deck import Deck


class DeckTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deck = Deck()

    def test_deck_for_number_of_cards(self):
        self.assertEqual(len(self.deck.cards), 52)

    def test_deck_for_duplicates(self):
        no_dupes = set(self.deck.cards)
        self.assertEqual(len(self.deck.cards), len(no_dupes))
