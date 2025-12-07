from enum import Enum
import functools


_SUIT_SYMBOLS = "♠♥♣♦★"
_SUIT_COLOURS = ["#568fc1", "#995362", "#77ac70", "#bf90dc", "#ffeeb0"]


@functools.total_ordering
class Suit(Enum):

    SPADES = 0
    HEARTS = 1
    CLUBS = 2
    DIAMONDS = 3
    SPECIAL = 4

    @property
    def symbol(self):
        return _SUIT_SYMBOLS[self.value]

    @property
    def colour(self):
        return _SUIT_COLOURS[self.value]

    def __eq__(self, other):
        if not isinstance(other, Suit):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, Suit):
            return NotImplemented
        return self.value < other.value
