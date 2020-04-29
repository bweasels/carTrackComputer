"""
Module storing the implementation of a circular progress bar in kivy.
.. note::
    Refer to the in-code documentation of the class and its methods to learn about the tool. Includes a usage example.
Authorship: Kacper Florianski
"""
from kivy.core.text import Label
from kivy.graphics import Rectangle, Color, Ellipse
from oldScripts.dials import CircularProgressBar

# This constant enforces the cap argument to be one of the caps accepted by the kivy.graphics.Line class
_ACCEPTED_BAR_CAPS = {"round", "none", "square"}

# Declare the defaults for the modifiable values
_DEFAULT_THICKNESS = 10
_DEFAULT_CAP_STYLE = 'round'
_DEFAULT_PRECISION = 10
_DEFAULT_PROGRESS_COLOUR = (1, 0, 0, 1)
_DEFAULT_BACKGROUND_COLOUR = (0.26, 0.26, 0.26, 1)
_DEFAULT_MAX_PROGRESS = 100
_DEFAULT_MIN_PROGRESS = 0
_DEFAULT_WIDGET_SIZE = 200
_DEFAULT_TEXT_LABEL = Label(text="{}", font_size=40)

# Declare the defaults for the normalisation function, these are used in the textual representation (multiplied by 100)
_NORMALISED_MAX = 0
_NORMALISED_MIN = -1
_DEFAULT_SIZE_MULTIPLIER = 1
_DEFAULT_START_ANGLE = 270
_DEFAULT_END_ANGLE = 90
_DEFAULT_FLIP = False


class AVCSProgressBar(CircularProgressBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._size_multiplier = _DEFAULT_SIZE_MULTIPLIER
        self._start_angle = _DEFAULT_START_ANGLE
        self._end_angle = _DEFAULT_END_ANGLE
        self._flip = _DEFAULT_FLIP

    @property
    def flip(self):
        return self._flip

    @flip.setter
    def flip(self, value: bool):
        if type(value) != bool:
            raise TypeError('Flip value must be a boolean, not {}!'.format(type(value)))
        self._flip = value

    def _refresh_text(self):
        """
         Function used to refresh the text of the progress label.
         Additionally updates the variable tracking the label's texture size
         """
        # Set the range of the numbers to the range of the AVCS system & ensure there are 2 decimal places
        value = round(self.get_normalised_progress() * 10 - 5, 2)
        value = format(value, '.2f')
        self._text_label.text = self._default_label_text.format(str(value))
        self._text_label.refresh()
        self._label_size = self._text_label.texture.size

    def _refresh_progress_color(self):
        """
        Function used to calculate the blue to red gradient
        """
        # get_normalised_progress ranges from 0 - 1, so scale
        bval = 1 - self.get_normalised_progress()
        rval = self.get_normalised_progress()
        alpha = abs(-0.5 + self.get_normalised_progress()) + 0.5
        self._progress_colour = (rval, 0, bval, alpha)

    def _refresh_size_multiplier(self):
        """
        Sets the size multipler for the dial to notify when things get saucy
        """
        self._size_multiplier = 1 + 0.2 * (abs(self.get_normalised_progress() - 0.5) / 0.5)

    def _refresh_end_angle(self):
        """
        Sets the angle for the sweeping dial
        """
        if self._flip:
            self._end_angle = (-180 * self.get_normalised_progress() + 180) + 0.001
        else:
            self._end_angle = (180 * self.get_normalised_progress() + 180) + 0.001

    def _test_text(self):
        """
        Print out a text for testing
        """
        value = self._end_angle
        self._text_label.text = self._default_label_text.format(str(value))
        self._text_label.refresh()
        self._label_size = self._text_label.texture.size

    def _draw(self):
        """
        Function used to draw the progress bar onto the screen.
        The drawing process is as follows:
            1. Clear the canvas
            2. Draw the background progress line (360 degrees)
            3. Draw the actual progress line (N degrees where n is between 0 and 360)
            4. Draw the textual representation of progress in the middle of the circle
        """

        with self.canvas:
            self.canvas.clear()
            self._refresh_text()
            self._refresh_progress_color()
            self._refresh_size_multiplier()
            self._refresh_end_angle()
            # self._test_text()

            if self._flip:
                self._start_angle = 90

            # Draw the background progress line
            Color(*self.background_colour)
            # Ellipse(pos=(self.pos[0]-self._widget_size/2, self.pos[1]-self._widget_size/2),
            #        size=(self._widget_size, self._widget_size))

            # Draw the progress line
            Color(*self.progress_colour)
            size = self._widget_size * self._size_multiplier
            Ellipse(pos=(self.pos[0] - size / 2, self.pos[1] - size / 2),
                    angle_start=self._start_angle, angle_end=self._end_angle, size=(size, size))

            # Center and draw the progress text
            Color(0, 0, 0, 1)
            Rectangle(texture=self._text_label.texture, size=self._label_size,
                      pos=(self._widget_size / 2 - self._label_size[0] + self.pos[0],
                           self._widget_size / 2 - self._label_size[1]*1.75 + self.pos[1]))
