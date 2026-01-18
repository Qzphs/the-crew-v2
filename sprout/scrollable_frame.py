import tkinter

from sprout.constants import NW
from sprout.widget import Container


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
