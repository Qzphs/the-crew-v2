from game.mission import Mission
from game.player import Player
from game.players import PLAYERS

import sprout as s


class PlayersScreen(s.Screen):

    def __init__(self, parent: s.Application, mission: Mission):
        super().__init__(parent)
        self.mission = mission

        self.select_players_label = s.TextLabel(self, "select players:")
        self.select_players_label.font = s.Font("Sans Serif", 15)
        self.select_players_label.place(x=640, y=50, anchor=s.N)

        self.player_widgets = [PlayerWidget(self, player) for player in PLAYERS]
        for i, player_widget in enumerate(self.player_widgets):
            # TODO: make player screen scrollable to support more players
            row = i // 6
            column = i % 6
            player_widget.place(
                x=190 + column * 180,
                y=200 + row * 180,
                anchor=s.CENTRE,
            )

        self.continue_button = s.TextLabel(self, "(continue)")
        self.continue_button.font = s.Font("Sans Serif", 15)
        self.continue_button.place(x=640, y=720, anchor=s.S)

        for player_widget in self.player_widgets:
            player_widget.on_click = self.select_player

    def select_player(self, source: "PlayerWidget"):
        player = source.player
        if player in self.mission.players:
            self.mission.players.remove(player)
            source.hide_border()
        else:
            player.index = len(self.mission.players)
            self.mission.players.append(player)
            source.show_border()


class PlayerWidget(s.ImageLabel):

    def __init__(self, parent: s.Container, player: Player):
        super().__init__(parent, s.Image.from_file(player.name))
        self.player = player
        self.border_width = 5

    def show_border(self):
        self.border_colour = "#f18519"

    def hide_border(self):
        self.border_colour = None
