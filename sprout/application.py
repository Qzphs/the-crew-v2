import tkinter

from sprout.constants import OFFSCREEN
from sprout.widget import Container, Widget


class Application:
    """
    Main class for GUIs using Sprout.

    Single-screen GUIs can use the default screen (self.screen)
    directly. Multi-screen GUIs can create their own screens and
    show/hide them using self.change_screen().
    """

    def __init__(self, title: str, width: int, height: int):
        self.tk = tkinter.Tk()
        self.tk.title(title)
        self.tk.geometry(f"{width}x{height}+{0}+{0}")
        self.width = width
        self.height = height
        self.screen = Screen(self)
        self.screen.place(x=0, y=0)

    def change_screen(self, screen: "Screen"):
        self.screen.place(x=OFFSCREEN, y=0)
        self.screen = screen
        self.screen.place(x=0, y=0)

    def start(self):
        self.tk.mainloop()


class Screen(Container):

    def __init__(self, parent: Application):
        self.parent = parent
        self.base = tkinter.Frame(
            parent.tk,
            width=parent.width,
            height=parent.height,
        )
        self.frame = self.base
        self.children: list[Widget] = []

    @property
    def background_colour(self):
        return self.base.cget("bg")

    @background_colour.setter
    def background_colour(self, background_colour: str | None):
        if background_colour is None:
            self.base.config(bg=self.parent.tk.cget("bg"))
        else:
            self.base.config(bg=background_colour)
