from game.card import Card
from game.mission import Mission
from game.task import Task

import sprout as s


class MissionScreen(s.Screen):

    def __init__(self, parent: s.Application, mission: Mission):
        super().__init__(parent)
        self.mission = mission

        self.rearrange_mode = False
        self.selected_task_widget: TaskWidget | None = None

        self.reset_button = s.TextLabel(self, "(reset)")
        self.reset_button.on_click = self.reset
        self.reset_button.place(30, 30)

        self.add_single_button = s.TextLabel(self, "(add single)")
        self.add_single_button.on_click = self.add_single
        self.add_single_button.place(180, 30)

        self.add_double_button = s.TextLabel(self, "(add double)")
        self.add_double_button.on_click = self.add_double
        self.add_double_button.place(330, 30)

        self.add_special_button = s.TextLabel(self, "(add special)")
        self.add_special_button.on_click = self.add_special
        self.add_special_button.place(480, 30)

        self.rearrange_tasks_button = s.TextLabel(self, "(rearrange tasks)")
        self.rearrange_tasks_button.on_click = self.rearrange_tasks
        self.rearrange_tasks_button.place(630, 30)

        self.change_players_button = s.TextLabel(self, "(change players)")
        # on_click to be set by application
        self.change_players_button.place(1230, 30, anchor=s.NE)

        MAX_TASK_COUNT = 15
        self.task_widgets = [TaskWidget(self) for _ in range(MAX_TASK_COUNT)]
        for i, task_widget in enumerate(self.task_widgets):
            row = i // 3
            column = i % 3
            task_widget.place(x=30 + column * 400, y=90 + row * 135)

        for widget in self.children:
            if not isinstance(widget, s.TextLabel):
                continue
            widget.font = s.Font("Sans Serif", 15)

    def _update(self):
        if self.rearrange_mode:
            self.rearrange_tasks_button.colour = "#f18519"
        else:
            self.rearrange_tasks_button.colour = "#ffffff"
        for task_widget in self.task_widgets:
            self._update_border(task_widget)
            self._update_commands(task_widget)

    def _update_border(self, task_widget: "TaskWidget"):
        if not self.rearrange_mode:
            task_widget.border_colour = None
        elif task_widget == self.selected_task_widget:
            task_widget.border_colour = "#f18519"
        else:
            task_widget.border_colour = "#d1d1d1"

    def _update_commands(self, task_widget: "TaskWidget"):
        if not self.rearrange_mode:
            task_widget.inner1.on_click = None
            task_widget.inner2.on_click = None
            if task_widget.assignee_icon is not None:
                task_widget.assignee_icon.on_click = self.cycle_assignee
            for card_widget in task_widget.card_widgets:
                card_widget.on_click = card_widget.toggle_card
        else:
            task_widget.inner1.on_click = self.select_task
            task_widget.inner2.on_click = self.select_task
            if task_widget.assignee_icon is not None:
                task_widget.assignee_icon.on_click = self.select_task
            for card_widget in task_widget.card_widgets:
                card_widget.on_click = self.select_task

    def reset(self, source: s.TextLabel | None = None):
        self.mission.reset()
        self.rearrange_mode = False
        self.selected_task_widget = None
        for task_widget in self.task_widgets:
            task_widget.task = None
        self._update()

    def add_single(self, source: s.TextLabel):
        task_widget = next(
            (widget for widget in self.task_widgets if widget.task is None), None
        )
        if task_widget is None:
            return
        self.mission.add_task(1)
        task_widget.task = self.mission.tasks[-1]
        self._update_border(task_widget)
        self._update_commands(task_widget)

    def add_double(self, source: s.TextLabel):
        task_widget = next(
            (widget for widget in self.task_widgets if widget.task is None), None
        )
        if task_widget is None:
            return
        self.mission.add_task(2)
        task_widget.task = self.mission.tasks[-1]
        self._update_border(task_widget)
        self._update_commands(task_widget)

    def add_special(self, source: s.TextLabel):
        task_widget = next(
            (widget for widget in self.task_widgets if widget.task is None), None
        )
        if task_widget is None:
            return
        self.mission.add_special_task()
        task_widget.task = self.mission.tasks[-1]
        self._update_border(task_widget)
        self._update_commands(task_widget)

    def rearrange_tasks(self, source: s.TextLabel):
        self.rearrange_mode = not self.rearrange_mode
        self.selected_task_widget = None
        self._update()

    def select_task(self, source: s.Widget):
        """
        Select a task to swap.

        If no task has been selected yet, mark this task as selected.
        Otherwise, swap the previously selected task with this one and
        clear selections.
        """
        while source.parent != self:
            source = source.parent
        assert isinstance(source, TaskWidget)

        if self.selected_task_widget is None:
            self.selected_task_widget = source
            self._update_border(source)
        else:
            widget1 = self.selected_task_widget
            widget2 = source
            task1 = widget1.task
            task2 = widget2.task
            widget1.task = task2
            widget2.task = task1
            self.selected_task_widget = None
            self._update_border(widget1)
            self._update_commands(widget1)
            self._update_border(widget2)
            self._update_commands(widget2)

    def cycle_assignee(self, source: "AssigneeWidget"):
        index = self.mission.players.index(source.task.assignee)
        index += 1
        index %= len(self.mission.players)
        source.task.assignee = self.mission.players[index]
        source.image = s.Image.from_file(source.task.assignee.name).subsample(2)


class TaskWidget(s.Frame):

    def __init__(self, parent: s.Container):
        super().__init__(parent, 360, 120)
        self._task: Task | None = None
        self.border_width = 5

        # So that border displays correctly
        self.inner1 = s.Frame(self, 350, 110)
        self.inner1.place(0, 0)

        self.inner2 = s.Frame(self.inner1, 0, 0)
        self.inner2.place(0, 0)

        self.assignee_icon: AssigneeWidget | None = None
        self.card_widgets: list[CardWidget] = []

    @property
    def task(self):
        return self._task

    @task.setter
    def task(self, task: Task | None):
        self._task = task
        for widget in list(self.inner2.children):
            widget.destroy()
        self.assignee_icon = None
        self.card_widgets.clear()
        if task is None:
            return
        self.assignee_icon = AssigneeWidget(self.inner2, task)
        self.assignee_icon.pack()
        self.card_widgets.extend(CardWidget(self.inner2, card) for card in task.cards)
        for card_widget in self.card_widgets:
            card_widget.pack()

    def mark_available(self):
        self.border_colour = "#d1d1d1"

    def mark_selected(self):
        self.border_colour = "#f18519"

    def hide_border(self):
        self.border_colour = None


class AssigneeWidget(s.ImageLabel):

    def __init__(self, parent: s.Container, task: Task):
        super().__init__(
            parent,
            s.Image.from_file(task.assignee.name).subsample(2),
        )
        self.task = task


class CardWidget(s.TextLabel):

    def __init__(self, parent: s.Container, card: Card):
        super().__init__(parent, str(card))
        self.card = card

        if self.card.done:
            self.colour = "#4f4f4f"
            self.font = s.Font("Sans Serif", 80, strikethrough=True)
        else:
            self.colour = self.card.suit.colour
            self.font = s.Font("Sans Serif", 80, strikethrough=False)

        self.on_click = self.toggle_card

    def toggle_card(self, source: "CardWidget"):
        self.card.done = not self.card.done
        if self.card.done:
            self.colour = "#4f4f4f"
            self.font = s.Font("Sans Serif", 80, strikethrough=True)
        else:
            self.colour = self.card.suit.colour
            self.font = s.Font("Sans Serif", 80, strikethrough=False)
