from game.rank import Rank
from game.suit import Suit


class Card:

    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit
        self.done = False

    @classmethod
    def special(cls):
        return Card(Rank.NINE, Suit.SPECIAL)

    def __repr__(self):
        if self.suit == Suit.SPECIAL:
            return f"{self.suit.symbol}X"
        return f"{self.suit.symbol}{self.rank.value}"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return (self.suit, self.rank) == (other.suit, other.rank)

    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return (self.suit, self.rank) < (other.suit, other.rank)
