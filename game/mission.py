from game.card import Card
from game.deck import Deck
from game.player import Player
from game.players import BLANK_PLAYER
from game.task import Task


class Mission:

    def __init__(self):
        self.players: list[Player] = [BLANK_PLAYER]
        self.deck = Deck()
        self.tasks: list[Task] = []
        self.reset()

    def reset(self):
        self.deck.reset()
        self.tasks.clear()

    def add_task(self, n_cards: int):
        self.tasks.append(Task([self.deck.pop() for _ in range(n_cards)]))

    def add_special_task(self):
        self.tasks.append(Task([Card.special()]))
