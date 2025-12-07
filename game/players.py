import os

from game.player import Player


PLAYERS = [
    Player(f"players/{filename}")
    for filename in os.listdir("players")
    if filename.endswith(".png")
]
PLAYERS.sort(key=lambda player: player.name)

BLANK_PLAYER = Player("assets/blank.png")
