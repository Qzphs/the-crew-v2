from game.card import Card
from game.players import BLANK_PLAYER


class Task:

    def __init__(self, cards: list[Card]):
        self.cards = sorted(cards)
        self.assignee = BLANK_PLAYER
