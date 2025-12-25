import tkinter

from game.card import Card
from game.mission import Mission
from game.task import Task
import sprout


class MissionScreen(sprout.Screen):

    def __init__(self, parent: sprout.Application, mission: Mission):
        super().__init__(parent)
        self.mission = mission

        self.rearrange_mode = False
        self.selected_task: Task | None = None

        self.reset_button = sprout.TextLabel(self, "(reset)")
        self.reset_button.command = self.reset
        self.reset_button.font = sprout.Font("Sans Serif", 15)
        self.reset_button.place(30, 30)

        self.add_single_button = sprout.TextLabel(self, "(add single)")
        self.add_single_button.command = self.add_single
        self.add_single_button.font = sprout.Font("Sans Serif", 15)
        self.add_single_button.place(180, 30)

        self.add_double_button = sprout.TextLabel(self, "(add double)")
        self.add_double_button.command = self.add_double
        self.add_double_button.font = sprout.Font("Sans Serif", 15)
        self.add_double_button.place(330, 30)

        self.add_special_button = sprout.TextLabel(self, "(add special)")
        self.add_special_button.command = self.add_special
        self.add_special_button.font = sprout.Font("Sans Serif", 15)
        self.add_special_button.place(480, 30)

        self.rearrange_tasks_button = sprout.TextLabel(self, "(rearrange tasks)")
        self.rearrange_tasks_button.command = self.rearrange_tasks
        self.rearrange_tasks_button.font = sprout.Font("Sans Serif", 15)
        self.rearrange_tasks_button.place(630, 30)

        self.change_players_button = sprout.TextLabel(self, "(change players)")
        # Command to be set by application
        self.change_players_button.font = sprout.Font("Sans Serif", 15)
        self.change_players_button.place(1230, 30, anchor=sprout.NE)

        self.task_widgets: list[TaskWidget] = []

    def update(self):
        for task_widget in self.task_widgets:
            task_widget.destroy()
        self.task_widgets.clear()
        self.task_widgets.extend(TaskWidget(self, task) for task in self.mission.tasks)

        self._update_task_borders()
        self._update_task_commands()
        for i, task_widget in enumerate(self.task_widgets):
            row = i // 3
            column = i % 3
            task_widget.place(x=30 + column * 400, y=90 + row * 135)

    def _update_task_borders(self):
        if self.rearrange_mode:
            self.rearrange_tasks_button.colour = "#f18519"
            for widget in self.task_widgets:
                if widget.task == self.selected_task:
                    widget.mark_selected()
                else:
                    widget.mark_available()
        else:
            self.rearrange_tasks_button.colour = "#ffffff"
            for widget in self.task_widgets:
                widget.hide_border()

    def _update_task_commands(self):
        if self.rearrange_mode:
            for widget in self.task_widgets:
                widget.assignee_icon.command = self.select_task
                for card_widget in widget.card_widgets:
                    card_widget.command = self.select_task
        else:
            for widget in self.task_widgets:
                widget.assignee_icon.command = self.cycle_assignee
                for card_widget in widget.card_widgets:
                    card_widget.command = card_widget.toggle_card

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

    def rearrange_tasks(self, widget: sprout.TextLabel):
        self.rearrange_mode = not self.rearrange_mode
        self.selected_task = None
        self._update_task_borders()
        self._update_task_commands()

    def select_task(self, widget: "TaskWidget | AssigneeWidget | CardWidget"):
        """
        Select a task to swap.

        If no task has been selected yet, mark this task as selected.
        Otherwise, swap the previously selected task with this one and
        clear selections.
        """
        while widget.parent != self:
            widget = widget.parent
        assert isinstance(widget, TaskWidget)

        if self.selected_task is None:
            self.selected_task = widget.task
        else:
            self.mission.swap_tasks(self.selected_task, widget.task)
            self.selected_task = None
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
        self.base.config(bd=5)

        # So that border displays correctly
        self.content = sprout.Frame(self, 0, 0)
        self.content.base.pack()

        self.assignee_icon = AssigneeWidget(self.content, task)
        self.assignee_icon.base.pack(side=tkinter.LEFT)

        self.card_widgets = [CardWidget(self.content, card) for card in task.cards]
        for card_widget in self.card_widgets:
            card_widget.base.pack(side=tkinter.LEFT)

    def mark_available(self):
        self.base.config(bg="#d1d1d1")

    def mark_selected(self):
        self.base.config(bg="#f18519")

    def hide_border(self):
        self.base.config(bg=self.parent.base.cget("bg"))


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
