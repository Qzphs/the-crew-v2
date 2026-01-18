import tkinter

from sprout.constants import NW


class Widget:
    """Base class for Sprout widgets."""

    def __init__(self, parent: "Container"):
        self.parent = parent
        self.base = tkinter.Frame(parent.frame)
        """
        The underlying tkinter widget.
        
        This can be accessed directly to hack in any changes not
        supported by Sprout.
        """
        self.parent.children.append(self)

    def pack(self, side: str = tkinter.LEFT):
        self.base.pack(side=side)

    def place(self, x: int, y: int, anchor: str = NW):
        self.base.place(x=x, y=y, anchor=anchor)

    def destroy(self):
        self.parent.children.remove(self)
        self.base.destroy()


class Container(Widget):
    """Base class for Sprout widgets that contain other widgets."""

    def __init__(self, parent: "Container"):
        super().__init__(parent)
        self.frame = self.base
        """The tkinter frame other widgets connect to."""
        self.children: list[Widget] = []
