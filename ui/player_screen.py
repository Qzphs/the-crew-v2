import tkinter

from game.mission import Mission
from game.player import Player
from game.players import PLAYERS
import sprout


class PlayerScreen(sprout.Screen):

    def __init__(self, parent: sprout.Application, mission: Mission):
        super().__init__(parent)
        self.mission = mission

        self.select_players_label = sprout.TextLabel(self, "select players:")
        self.select_players_label.font = sprout.Font("Sans Serif", 15)
        self.select_players_label.place(x=600, y=50, anchor=tkinter.N)

        self.player_widgets = [PlayerWidget(self, player) for player in PLAYERS]
        for i, player_widget in enumerate(self.player_widgets):
            # TODO: make player screen scrollable to support 10+ players
            row = i // 5
            column = i % 5
            player_widget.place(
                x=200 + column * 200, y=200 + row * 200, anchor=tkinter.CENTER
            )

        self.continue_button = sprout.TextLabel(self, "(continue)")
        self.continue_button.font = sprout.Font("Sans Serif", 15)
        self.continue_button.place(x=600, y=620, anchor=tkinter.S)

        for player_widget in self.player_widgets:
            player_widget.command = self.select_player

    def select_player(self, player_widget: "PlayerWidget"):
        player = player_widget.player
        if player in self.mission.players:
            self.mission.players.remove(player)
            player_widget.hide_border()
        else:
            player.index = len(self.mission.players)
            self.mission.players.append(player)
            player_widget.show_border()


class PlayerWidget(sprout.ImageLabel):

    def __init__(self, parent: sprout.Container, player: Player):
        super().__init__(parent, tkinter.PhotoImage(file=player.name))
        self.player = player

        self.base.config(bd=5)

    def parameters(self):
        return [self]

    def show_border(self):
        self.base.config(bg="#f18519")

    def hide_border(self):
        self.base.config(bg=self.parent.base.cget("bg"))
