import tkinter

from game.card import Card
from game.mission import Mission
from game.task import Task
import sprout


class MissionScreen(sprout.Screen):

    def __init__(self, parent: sprout.Application, mission: Mission):
        super().__init__(parent)
        self.mission = mission

        self.reset_button = sprout.TextLabel(self, "(reset)")
        self.reset_button.font = sprout.Font("Sans Serif", 15)
        self.reset_button.place(30, 30)

        self.add_single_button = sprout.TextLabel(self, "(add single)")
        self.add_single_button.font = sprout.Font("Sans Serif", 15)
        self.add_single_button.place(180, 30)

        self.add_double_button = sprout.TextLabel(self, "(add double)")
        self.add_double_button.font = sprout.Font("Sans Serif", 15)
        self.add_double_button.place(330, 30)

        self.add_special_button = sprout.TextLabel(self, "(add special)")
        self.add_special_button.font = sprout.Font("Sans Serif", 15)
        self.add_special_button.place(480, 30)

        self.sort_tasks_button = sprout.TextLabel(self, "(sort tasks)")
        self.sort_tasks_button.font = sprout.Font("Sans Serif", 15)
        self.sort_tasks_button.place(630, 30)

        self.change_players_button = sprout.TextLabel(self, "(change players)")
        self.change_players_button.font = sprout.Font("Sans Serif", 15)
        self.change_players_button.place(1230, 30, anchor=sprout.NE)

        self.task_widgets: list[TaskWidget] = []

        self.reset_button.command = self.reset
        self.add_single_button.command = self.add_single
        self.add_double_button.command = self.add_double
        self.add_special_button.command = self.add_special
        self.sort_tasks_button.command = self.sort_tasks

    def update(self):
        for task_widget in self.task_widgets:
            task_widget.destroy()
        self.task_widgets.clear()

        self.task_widgets.extend(TaskWidget(self, task) for task in self.mission.tasks)
        for i, task_widget in enumerate(self.task_widgets):
            task_widget.assignee_icon.command = self.cycle_assignee
            row = i // 3
            column = i % 3
            task_widget.place(x=30 + column * 400, y=90 + row * 135)

    def reset(self, widget: sprout.TextLabel | None = None):
        self.mission.reset()
        self.update()

    def add_single(self, widget: sprout.TextLabel):
        self.mission.add_task(1)
        self.update()

    def add_double(self, widget: sprout.TextLabel):
        self.mission.add_task(2)
        self.update()

    def add_special(self, widget: sprout.TextLabel):
        self.mission.add_special_task()
        self.update()

    def sort_tasks(self, widget: sprout.TextLabel):
        self.mission.tasks.sort()
        self.update()

    def cycle_assignee(self, widget: "AssigneeWidget"):
        index = self.mission.players.index(widget.task.assignee)
        index += 1
        index %= len(self.mission.players)
        widget.task.assignee = self.mission.players[index]
        widget.image = sprout.Image.from_file(widget.task.assignee.name).subsample(2)


class TaskWidget(sprout.Frame):

    def __init__(self, parent: sprout.Container, task: Task):
        super().__init__(parent, 0, 0)
        self.task = task

        self.assignee_icon = AssigneeWidget(self, task)
        self.assignee_icon.base.pack(side=tkinter.LEFT)

        self.card_widgets = [CardWidget(self, card) for card in task.cards]
        for card_widget in self.card_widgets:
            card_widget.base.pack(side=tkinter.LEFT)


class AssigneeWidget(sprout.ImageLabel):

    def __init__(self, parent: sprout.Container, task: Task):
        super().__init__(
            parent,
            sprout.Image.from_file(task.assignee.name).subsample(2),
        )
        self.task = task


class CardWidget(sprout.TextLabel):

    def __init__(self, parent: sprout.Container, card: Card):
        super().__init__(parent, str(card))
        self.card = card

        if self.card.done:
            self.colour = "#4f4f4f"
            self.font = sprout.Font("Sans Serif", 80, strikethrough=True)
        else:
            self.colour = self.card.suit.colour
            self.font = sprout.Font("Sans Serif", 80, strikethrough=False)

        self.command = self.toggle_card

    def toggle_card(self, widget: "CardWidget"):
        self.card.done = not self.card.done
        if self.card.done:
            self.colour = "#4f4f4f"
            self.font = sprout.Font("Sans Serif", 80, strikethrough=True)
        else:
            self.colour = self.card.suit.colour
            self.font = sprout.Font("Sans Serif", 80, strikethrough=False)
