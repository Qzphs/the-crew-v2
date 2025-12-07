import random

from game.card import Card
from game.rank import Rank
from game.suit import Suit


class Deck:

    def __init__(self):
        self.cards: list[Card] = []
        self.reset()

    def reset(self):
        self.cards.clear()
        self.cards.extend(
            Card(rank, suit) for rank in Rank for suit in Suit if suit != Suit.SPECIAL
        )
        random.shuffle(self.cards)

    def pop(self):
        if not self.cards:
            return Card.special()
        return self.cards.pop()
