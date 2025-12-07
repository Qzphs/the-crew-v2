# Sprout v0.1 https://github.com/Qzphs/sprout


import tkinter.font
from typing import Callable
import tkinter


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

    def place(self, x: int, y: int, anchor: str = tkinter.NW):
        self.base.place(x=x, y=y, anchor=anchor)


class Container(Widget):
    """Base class for Sprout widgets that contain other widgets."""

    def __init__(self, parent: "Container"):
        super().__init__(parent)
        self.frame = self.base
        """The tkinter frame other widgets connect to."""



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



class Dropdown(Widget):
    """Same as tkinter.OptionMenu."""

    def __init__(self, parent: Container, options: list[str]):
        super().__init__(parent)
        assert len(options) > 0
        self.variable = tkinter.StringVar(self.base)
        self.variable.set(options[0])
        self.options = options
        self.dropdown = tkinter.OptionMenu(self.base, self.variable, *options)
        self.dropdown.pack()

    @property
    def value(self):
        return self.variable.get()



class Entry(Widget):
    """Same as tkinter.Entry."""

    def __init__(self, parent):
        super().__init__(parent)
        self.variable = tkinter.StringVar(self.base)
        self.entry = tkinter.Entry(self.base, textvariable=self.variable)
        self.entry.pack()

    @property
    def value(self):
        return self.entry.get()


class Frame(Container):
    """Same as tkinter.Frame."""

    def __init__(self, parent: Container, width: int, height: int):
        super().__init__(parent)
        self.base.config(width=width, height=height)



class ImageLabel(Widget):
    """Same as tkinter.Label, but always has an image."""

    def __init__(self, parent: Container, image: tkinter.PhotoImage):
        super().__init__(parent)
        self.label = tkinter.Label(self.base, image=image)
        self._image = image
        self.label.bind("<Button-1>", self._on_click)
        self.label.pack()
        self.command: Callable | None = None

    def _on_click(self, event: tkinter.Event):
        if self.command is None:
            return
        self.command(*self.parameters())

    def parameters(self) -> list:
        """
        Return a list of parameters this widget should use.

        When the widget is clicked, this method is called to get a list of
        parameters, which are then passed into self.command().

        Subclasses should override this.
        """
        return []

    @property
    def image(self) -> tkinter.PhotoImage:
        return self._image

    @image.setter
    def image(self, image: tkinter.PhotoImage):
        self.label.config(image=image)
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

        self.scrollbar = tkinter.Scrollbar(
            self.base,
            orient=tkinter.VERTICAL,
        )
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.canvas = tkinter.Canvas(
            self.base,
            bd=0,
            highlightthickness=0,
            width=outer_width,
            height=outer_height,
            scrollregion=(0, 0, inner_width, inner_height),
            yscrollcommand=self.scrollbar.set,
        )
        self.canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.scrollbar.config(command=self.canvas.yview)

        self.frame = tkinter.Frame(
            self.canvas,
            width=inner_width,
            height=inner_height,
        )
        self.frame.pack(fill=tkinter.BOTH)
        self.canvas.create_window(
            0,
            0,
            anchor=tkinter.NW,
            width=inner_width,
            height=inner_height,
            window=self.frame,
        )



class TextLabel(Widget):
    """Same as tkinter.Label, but always has text."""

    def __init__(self, parent: Container, text: str):
        super().__init__(parent)
        self.label = tkinter.Label(self.base, text=text)
        self.label.bind("<Button-1>", self._on_click)
        self.label.pack()
        self.command: Callable | None = None

    def _on_click(self, event: tkinter.Event):
        if self.command is None:
            return
        self.command(*self.parameters())

    def parameters(self) -> list:
        """
        Return a list of parameters this widget should use.

        When the widget is clicked, this method is called to get a list of
        parameters, which are then passed into self.command().

        Subclasses should override this.
        """
        return []

    @property
    def text(self) -> str:
        return self.label.cget("text")

    @text.setter
    def text(self, text: str):
        self.label.config(text=text)

    @property
    def font(self):
        # TODO: return a sprout.Font instead of str
        return self.label.cget("font")

    @font.setter
    def font(self, font: Font):
        self.label.config(font=font.tkinter())
