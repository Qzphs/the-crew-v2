import tkinter
from typing import Callable

from sprout.widget import Container, Widget


class Frame(Container):
    """Same as tkinter.Frame."""

    def __init__(self, parent: Container, width: int, height: int):
        super().__init__(parent)
        self.base.config(width=width, height=height)
        self.base.bind("<Button-1>", self._on_click)
        self.on_click: Callable[[Widget], None] | None = None

    def _on_click(self, event: tkinter.Event):
        if self.on_click is None:
            return
        self.on_click(self)

    @property
    def background_colour(self):
        if self.base.cget("bg") == self.parent.base.cget("bg"):
            return None
        return self.base.cget("bg")

    @background_colour.setter
    def background_colour(self, background_colour: str | None):
        if background_colour is None:
            self.base.config(bg=self.parent.base.cget("bg"))
        else:
            self.base.config(bg=background_colour)

    @property
    def border_width(self):
        return self.base.cget("bd")

    @border_width.setter
    def border_width(self, border_width: int):
        self.base.config(bd=border_width)
