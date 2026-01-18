import tkinter
from typing import Callable

from sprout.widget import Container, Widget


class Dropdown(Widget):
    """Same as tkinter.OptionMenu."""

    def __init__(self, parent: Container, options: list[str]):
        super().__init__(parent)
        assert len(options) > 0
        self._variable = tkinter.StringVar(self.base)
        self._variable.set(options[0])
        self._variable.trace_add("write", self._on_write)
        self.options = options
        self._dropdown = tkinter.OptionMenu(self.base, self._variable, *options)
        self._dropdown.pack()
        self.on_write: Callable[[Widget], None] | None = None

    def _on_write(self, *args):
        if self.on_write is None:
            return
        self.on_write(self)

    @property
    def value(self):
        return self._variable.get()

    # font does not seem to behave well on macOS
