import tkinter
from typing import Callable

from sprout.image import Image
from sprout.widget import Container, Widget


class ImageLabel(Widget):
    """Same as tkinter.Label, but always has an image."""

    def __init__(self, parent: Container, image: Image):
        super().__init__(parent)
        self._label = tkinter.Label(self.base, image=image.base)
        self._image = image
        self._label.bind("<Button-1>", self._on_click)
        self._label.pack()
        self.on_click: Callable[[Widget], None] | None = None

    def _on_click(self, event: tkinter.Event):
        if self.on_click is None:
            return
        self.on_click(self)

    @property
    def border_colour(self):
        if self.base.cget("bg") == self.parent.base.cget("bg"):
            return None
        return self.base.cget("bg")

    @border_colour.setter
    def border_colour(self, border_colour: str | None):
        if border_colour is None:
            self.base.config(bg=self.parent.base.cget("bg"))
        else:
            self.base.config(bg=border_colour)

    @property
    def border_width(self):
        return self.base.cget("bd")

    @border_width.setter
    def border_width(self, border_width: int):
        self.base.config(bd=border_width)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image: Image):
        self._label.config(image=image.base)
        self._image = image
