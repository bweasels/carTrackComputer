"""
A generic module to plot out barplots
Authorship: Ben Wesley
"""

from kivy.core.text import Label
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.widget import Widget

_DEFAULT_TEXT_LABEL = Label(text="{}", font_size=32, halign='middle', valign='middle')
_DEFAULT_NAME = Label(text="{}", font_size=50)
_DEFAULT_PLOT_SIZE = (10, 100)
_DEFAULT_MAX_PROGRESS = 15.0
_DEFAULT_MIN_PROGRESS = -15.0
_DEFAULT_POS = 100, 100
_DEFAULT_BORDER_THICKNESS = 2
_DEFAULT_BORDER_HEIGHT = 250
_DEFAULT_BORDER_WIDTH = 100
_DEFAULT_BAR_COLOR = (0, 0, 1, 1)


class GenericBar(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set the min and max values calculate the bar size
        self._plot_size = _DEFAULT_PLOT_SIZE
        self._max_progress = _DEFAULT_MAX_PROGRESS
        self._min_progress = _DEFAULT_MIN_PROGRESS
        self._value = _DEFAULT_MIN_PROGRESS

        # Set the border rectangle dimensions
        self._pos = _DEFAULT_POS
        self._border_thickness = _DEFAULT_BORDER_THICKNESS
        self._border_width = _DEFAULT_BORDER_WIDTH
        self._border_height = _DEFAULT_BORDER_HEIGHT

        # Set the bar center relative to the bar dimensions
        self._bar_x = self._pos[0] + self._border_thickness
        self._bar_y = self._pos[1] + self._border_thickness
        self._bar_width = self._border_width - 2 * self._border_thickness
        self._bar_max_height = self._pos[1] + self._border_height - self._border_thickness
        self._bar_min_height = self._pos[1] + self._border_thickness

        # Set the bar color, text, and name
        self._bar_color = _DEFAULT_BAR_COLOR
        self._text_label = _DEFAULT_TEXT_LABEL
        self._default_label_text = _DEFAULT_TEXT_LABEL.text
        self._label_size = (90, 40)
        self._name_size = (0, 0)
        self._name = _DEFAULT_NAME
        self._name_text = _DEFAULT_NAME.text

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
            self._bar_y = self._pos[1] + self._border_thickness

    @property
    def max(self):
        return self._max_progress

    @max.setter
    def max(self, value: float):
        if type(value) != float:
            raise TypeError("Maximum progress only accepts an float value, not {}!".format(type(value)))
        elif value <= self._min_progress:
            raise ValueError("Maximum progress - {} - must be greater than minimum progress ({})!"
                             .format(value, self._min_progress))
        else:
            self._max_progress = value

    @property
    def min(self):
        return self._min_progress

    @min.setter
    def min(self, value: float):
        if type(value) != float:
            raise TypeError("Minimum progress only accepts an float value, not {}!".format(type(value)))
        elif value > self._max_progress:
            raise ValueError("Minimum progress - {} - must be smaller than maximum progress ({})!"
                             .format(value, self._max_progress))
        else:
            self._min_progress = value
#            self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
         if type(value) != float:
            raise TypeError("Progress must be an float value, not {}!".format(type(value)))
         elif self._min_progress > value or value > self._max_progress:
            raise ValueError("Progress must be between minimum ({}) and maximum ({}), not {}!"
                             .format(self._min_progress, self._max_progress, value))
         if value != self._value:
            self._value = value
            self._draw()

    @property
    def label(self):
        return self._text_label

    @label.setter
    def label(self, value: Label):
        if not isinstance(value, Label):
            raise TypeError("Label must a kivy.graphics.Label, not {}!".format(type(value)))
        else:

            self._text_label = value
            self._default_label_text = value.text

    @property
    def bar_name(self):
        return self._name

    @bar_name.setter
    def bar_name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Label must a string, not {}!".format(type(value)))
        else:
            value = Label(text=value, halign='middle', valign='middle', font_size=20)
            self._name = value
            self._name_text = value.text
            self._name.refresh()
            self._name_size = value.texture.size

    def _refresh_text(self):
        """
        Function used to refresh the text of the progress label.
        Additionally updates the variable tracking the label's texture size
        """
        value = format(self._value, '.2f')
        self._text_label.text = self._default_label_text.format(str(value))
        self._text_label.refresh()
        self._label_size = self._text_label.texture.size

    def _get_bar_height(self, value: int) -> int:
        """
        Function used to convert the progress range into pixels for the bar
        """
        range = self._bar_max_height - self._bar_min_height
        quanta = range / (self._max_progress - self._min_progress)
        return int(quanta * value)

    def _draw(self):
        """
        Function used to draw the progress bar onto the screen.
        The drawing process is as follows:
            1. Clear the canvas & get new values
            2. Draw the bounding box around the progress line
            3. Draw the actual progress line (N degrees where n is between 0 and 360)
            4. Draw the number value in the middle of the plot and the label on top
        """
        with self.canvas:
            self.canvas.clear()
            self._refresh_text()

            # Draw the background progress line
            Color(1, 1, 1, 1)
            Line(rectangle=(self._pos[0], self._pos[1], self._border_width, self._border_height),
                 width=self._border_thickness)

            Color(0.5, 0.5, 0.5, 1)
            Rectangle(pos=(self._bar_x, self._bar_y),
                      size=(self._bar_width, self._get_bar_height(self._value)))

            Color(1, 1, 1, 1)
            Rectangle(texture=self._text_label.texture, size=self._label_size,
                      pos=(self._pos[0] + (self._border_width - self._label_size[0])/2,
                           self._pos[1] + self._border_height * 0.42))
            Color(1, 1, 1, 1)
            Rectangle(texture=self._name.texture, size=self._name_size,
                      pos=(self._pos[0] + self._border_thickness * 2,
                           self._pos[1] + self._border_height))
