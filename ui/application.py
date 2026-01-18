from game.mission import Mission
from game.players import BLANK_PLAYER

import sprout as s

from ui.mission_screen import MissionScreen
from ui.players_screen import PlayersScreen


class Application(s.Application):

    def __init__(self):
        super().__init__("the crew v2", 1280, 800)
        self.mission = Mission()

        self.players_screen = PlayersScreen(self, self.mission)
        self.mission_screen = MissionScreen(self, self.mission)

        self.players_screen.continue_button.on_click = self.start_mission

        self.mission_screen.change_players_button.on_click = self.change_players

        self.change_screen(self.players_screen)

    def start_mission(self, source: s.TextLabel):
        for i, player in enumerate(self.mission.players):
            player.index = i
        BLANK_PLAYER.index = 99
        self.mission_screen.reset()
        self.change_screen(self.mission_screen)

    def change_players(self, source: s.TextLabel):
        self.change_screen(self.players_screen)
