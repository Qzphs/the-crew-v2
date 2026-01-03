# Sprout v0.2.1 https://github.com/Qzphs/sprout


import tkinter
from typing import Callable
import tkinter.font


NW = tkinter.NW
N = tkinter.N
NE = tkinter.NE
E = tkinter.E
SE = tkinter.SE
S = tkinter.S
SW = tkinter.SW
W = tkinter.W

CENTRE = tkinter.CENTER


class Font:
    """Same as tkinter.font.Font."""

    def __init__(
        self,
        family: str,
        size: int,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strikethrough: bool = False,
    ):
        self.family = family
        self.size = size
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.strikethrough = strikethrough

    def tkinter(self):
        return tkinter.font.Font(
            family=self.family,
            size=self.size,
            weight=tkinter.font.BOLD if self.bold else tkinter.font.NORMAL,
            slant=tkinter.font.ITALIC if self.italic else tkinter.font.ROMAN,
            underline=self.underline,
            overstrike=self.strikethrough,
        )


class Image:

    def __init__(self, base: tkinter.PhotoImage):
        self.base = base

    @classmethod
    def from_file(cls, filename: str):
        return Image(tkinter.PhotoImage(file=filename))

    def subsample(self, x: int, y: int | None = None):
        if y is None:
            y = x
        return Image(self.base.subsample(x=x, y=y))

    def zoom(self, x: int, y: int | None = None):
        if y is None:
            y = x
        return Image(self.base.zoom(x=x, y=y))



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
        self.screen.place(x=-self.width, y=0)
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



class Dropdown(Widget):
    """Same as tkinter.OptionMenu."""

    def __init__(self, parent: Container, options: list[str]):
        super().__init__(parent)
        assert len(options) > 0
        self._variable = tkinter.StringVar(self.base)
        self._variable.set(options[0])
        self.options = options
        self._dropdown = tkinter.OptionMenu(self.base, self._variable, *options)
        self._dropdown.pack()

    @property
    def value(self):
        return self._variable.get()



class Entry(Widget):
    """Same as tkinter.Entry."""

    def __init__(self, parent):
        super().__init__(parent)
        self._variable = tkinter.StringVar(self.base)
        self._entry = tkinter.Entry(self.base, textvariable=self._variable)
        self._entry.pack()

    @property
    def value(self):
        return self._entry.get()



class Frame(Container):
    """Same as tkinter.Frame."""

    def __init__(self, parent: Container, width: int, height: int):
        super().__init__(parent)
        self.base.config(width=width, height=height)
        self.base.bind("<Button-1>", self._on_click)
        self.command: Callable[[Widget], None] | None = None

    def _on_click(self, event: tkinter.Event):
        if self.command is None:
            return
        self.command(self)

    @property
    def border_colour(self):
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



class ImageLabel(Widget):
    """Same as tkinter.Label, but always has an image."""

    def __init__(self, parent: Container, image: Image):
        super().__init__(parent)
        self._label = tkinter.Label(self.base, image=image.base)
        self._image = image
        self._label.bind("<Button-1>", self._on_click)
        self._label.pack()
        self.command: Callable[[Widget], None] | None = None

    def _on_click(self, event: tkinter.Event):
        if self.command is None:
            return
        self.command(self)

    @property
    def border_colour(self):
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



class ScrollableFrame(Container):
    """Use tkinter.Canvas to create a scrollable frame."""

    def __init__(
        self,
        parent: Container,
        outer_width: int,
        outer_height: int,
        inner_width: int,
        inner_height: int,
    ):
        # TODO: only vertical scroll supported
        assert outer_width == inner_width
        assert outer_height < inner_height

        super().__init__(parent)

        self._scrollbar = tkinter.Scrollbar(
            self.base,
            orient=tkinter.VERTICAL,
        )
        self._scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self._canvas = tkinter.Canvas(
            self.base,
            bd=0,
            highlightthickness=0,
            width=outer_width,
            height=outer_height,
            scrollregion=(0, 0, inner_width, inner_height),
            yscrollcommand=self._scrollbar.set,
        )
        self._canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self._scrollbar.config(command=self._canvas.yview)

        self.frame = tkinter.Frame(
            self._canvas,
            width=inner_width,
            height=inner_height,
        )
        self.frame.pack(fill=tkinter.BOTH)
        self._canvas.create_window(
            0,
            0,
            anchor=NW,
            width=inner_width,
            height=inner_height,
            window=self.frame,
        )



class TextLabel(Widget):
    """Same as tkinter.Label, but always has text."""

    def __init__(self, parent: Container, text: str):
        super().__init__(parent)
        self._label = tkinter.Label(self.base, text=text)
        self._label.bind("<Button-1>", self._on_click)
        self._label.pack()
        self.command: Callable[[Widget], None] | None = None

    def _on_click(self, event: tkinter.Event):
        if self.command is None:
            return
        self.command(self)

    @property
    def text(self) -> str:
        return self._label.cget("text")

    @text.setter
    def text(self, text: str):
        self._label.config(text=text)

    @property
    def font(self):
        # TODO: return a sprout.Font instead of str
        return self._label.cget("font")

    @font.setter
    def font(self, font: Font):
        self._label.config(font=font.tkinter())

    @property
    def colour(self):
        return self._label.cget("fg")

    @colour.setter
    def colour(self, colour: str):
        self._label.config(fg=colour)
