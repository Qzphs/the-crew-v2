import functools

from game.card import Card
from game.players import BLANK_PLAYER


@functools.total_ordering
class Task:

    def __init__(self, cards: list[Card]):
        self.cards = sorted(cards)
        self.assignee = BLANK_PLAYER

    def __eq__(self, other):
        if not isinstance(other, Task):
            return NotImplemented
        return (self.assignee.index, self.cards) == (other.assignee.index, other.cards)

    def __lt__(self, other):
        if not isinstance(other, Task):
            return NotImplemented
        return (self.assignee.index, self.cards) < (other.assignee.index, other.cards)
