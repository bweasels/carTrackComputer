"""
Module storing the implementation of the vertical barplots for AVCS
Authorship: Ben Wesley
"""

from kivy.graphics import Rectangle, Color, Line
from base_classes.GenericBars import GenericBar

_DEFAULT_BORDER_HEIGHT = 250

class AVCSProgressBar(GenericBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set the border rectangle dimensions
        self._border_height = _DEFAULT_BORDER_HEIGHT

        # Set the progress bar to be centered on the plot center b/c AVCS is pos and neg
        self._bar_y = self._pos[1] + self._border_height / 2

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, value: tuple):
        if type(value) != tuple:
            raise TypeError("pos only accepts a tuple, not {}!".format(type(value)))
        else:
            self._pos = value
            self._bar_x = self._pos[0] + self._border_thickness
            self._bar_y = self._pos[1] + self._border_height / 2

    def _refresh_progress_color(self):
        """
        Function to range progress color by spread
        """

        # normalize the progress from 0 - 1
        progress_range = self._max_progress - self._min_progress
        progress_value = self._value - self._min_progress
        progress = progress_value / progress_range

        # set the color values
        bval = 1 - progress**2
        rval = progress**2
        alpha = abs(-0.5 + progress) + 0.5
        gval = abs(alpha - 1)

        self._bar_color = (rval, gval, bval, alpha)

    def _draw(self):
        """
        Function used to draw an AVCS specific progress bar onto the screen.
        Changes from GenericBars.py
            1. Bar starts centered
            2. Bar becomes bluer as timing is retarded (neg AVCS), red for advance (pos AVCS)
        """
        with self.canvas:
            self.canvas.clear()
            self._refresh_progress_color()
            self._refresh_text()

            # Draw the background progress line
            Color(1, 1, 1, 1)
            Line(rectangle=(self._pos[0], self._pos[1], self._border_width, self._border_height),
                 width=self._border_thickness)

            Color(*self._bar_color)
            Rectangle(pos=(self._bar_x, self._bar_y),
                      size=(self._bar_width, self._get_bar_height(self._value)))

            Color(1, 1, 1, 1)
            Rectangle(texture=self._text_label.texture, size=self._label_size,
                      pos=(self._pos[0] + (self._border_width - self._label_size[0]) / 2,
                           self._pos[1] + self._border_height * 0.42))
            Color(1, 1, 1, 1)
            Rectangle(texture=self._name.texture, size=self._name_size,
                      pos=(self._pos[0] + self._border_thickness * 2,
                           self._pos[1] + self._border_height))
