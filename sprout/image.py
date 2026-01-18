import tkinter


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
