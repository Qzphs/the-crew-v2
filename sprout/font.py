import tkinter.font


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
