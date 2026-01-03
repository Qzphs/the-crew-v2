from game.mission import Mission
from game.players import BLANK_PLAYER
import sprout
from ui.mission_screen import MissionScreen
from ui.players_screen import PlayersScreen


class Application(sprout.Application):

    def __init__(self):
        super().__init__("the crew v2", 1280, 800)
        self.mission = Mission()

        self.players_screen = PlayersScreen(self, self.mission)
        self.mission_screen = MissionScreen(self, self.mission)

        self.players_screen.continue_button.command = self.start_mission

        self.mission_screen.change_players_button.command = self.change_players

        self.change_screen(self.players_screen)

    def start_mission(self, source: sprout.TextLabel):
        for i, player in enumerate(self.mission.players):
            player.index = i
        BLANK_PLAYER.index = 99
        self.mission_screen.reset()
        self.change_screen(self.mission_screen)

    def change_players(self, source: sprout.TextLabel):
        self.change_screen(self.players_screen)
