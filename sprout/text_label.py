import tkinter
from typing import Callable

from sprout.font import Font
from sprout.widget import Container, Widget


class TextLabel(Widget):
    """Same as tkinter.Label, but always has text."""

    def __init__(self, parent: Container, text: str):
        super().__init__(parent)
        self._label = tkinter.Label(self.base, text=text)
        self._label.bind("<Button-1>", self._on_click)
        self._label.pack()
        self.on_click: Callable[[Widget], None] | None = None

    def _on_click(self, event: tkinter.Event):
        if self.on_click is None:
            return
        self.on_click(self)

    @property
    def colour(self):
        return self._label.cget("fg")

    @colour.setter
    def colour(self, colour: str):
        self._label.config(fg=colour)

    @property
    def font(self):
        # TODO: return a sprout.Font instead of str
        return self._label.cget("font")

    @font.setter
    def font(self, font: Font):
        self._label.config(font=font.tkinter())

    @property
    def text(self) -> str:
        return self._label.cget("text")

    @text.setter
    def text(self, text: str):
        self._label.config(text=text)
