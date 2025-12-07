from enum import Enum
import functools


@functools.total_ordering
class Rank(Enum):

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9

    def __eq__(self, other):
        if not isinstance(other, Rank):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, Rank):
            return NotImplemented
        return self.value < other.value
