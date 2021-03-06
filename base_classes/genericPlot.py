"""
Module storing the implementation of line graphs
Authorship: Ben Wesley
"""

from kivy.uix.widget import Widget
from kivy.graphics import Line, Color

_DEFAULT_PLOT_AREA = (100, 100)
_DEFAULT_POSITION = (100, 100)
_DEFAULT_MIN_VALUE = 0
_DEFAULT_MAX_VALUE = 10
_DEFAULT_NUM_POINTS = 100
_DEFAULT_GRID_COLOR = (1, 1, 1, 1)
_DEFAULT_TICK_RATIO = 0.02


class GenericLinePlot(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # plot Dimensions and location
        self._plot_area = _DEFAULT_PLOT_AREA
        self._position = _DEFAULT_POSITION
        self._x_values = []
        self._y_values = []
        self._min_value = _DEFAULT_MIN_VALUE
        self._max_value = _DEFAULT_MAX_VALUE
        self._num_points = _DEFAULT_NUM_POINTS

        # define plot grid properties for the x y axis
        self._grid_color = _DEFAULT_GRID_COLOR
        self._y_axis_points = [int(self._position[0] + 0.1 * self._plot_area[0]),
                               int(self._position[1] + 0.1 * self._plot_area[1]),
                               int(self._position[0] + 0.1 * self._plot_area[0]),
                               int(self._position[1] + self._plot_area[1])]
        self._x_axis_points = [int(self._position[0] + 0.1 * self._plot_area[0]),
                               int(self._position[1] + 0.1 * self._plot_area[1]),
                               int(self._position[0] + 0.1 * self._plot_area[0]),
                               int(self._position[1] + self._plot_area[1])]
        self._tick_length = int(self._plot_area[1] * _DEFAULT_TICK_RATIO)
        self._tick_gap = int((self._x_axis_points[2] - self._x_axis_points[0]) / self._num_points)

    @property
    def max(self):
        return self._max_value

    @max.setter
    def max(self, value: float):
        if type(value) != float:
            raise TypeError("Maximum progress only accepts an float value, not {}!".format(type(value)))
        elif value <= self._min_value:
            raise ValueError("Maximum progress - {} - must be greater than minimum progress ({})!"
                             .format(value, self._min_value))
        else:
            self._max_value = value

    @property
    def min(self):
        return self._min_value

    @min.setter
    def min(self, value: float):
        if type(value) != float:
            raise TypeError("Minimum progress only accepts an float value, not {}!".format(type(value)))
        elif value > self._max_value:
            raise ValueError("Minimum progress - {} - must be smaller than maximum progress ({})!"
                             .format(value, self._max_value))
        else:
            self._min_value = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: tuple):
        if type(value) != tuple:
            raise TypeError('position only accepts a tuple, not {}!'.format(type(value)))
        else:
            self._position = value
            self._draw_axes()

    @property
    def plot_area(self):
        return self._plot_area

    @plot_area.setter
    def plot_area(self, value: tuple):
        if type(value) != tuple:
            raise TypeError('plot_area only accepts a tuple, not {}!'.format(type(value)))
        else:
            self._plot_area = value
            self._draw_axes()

    @property
    def values(self):
        return self._x_values, self._y_values

    @values.setter
    def values(self, values: tuple):
        if type(values) != tuple:
            raise TypeError("Values must be a tuple value, not {}!".format(type(values)))
        elif len(values[0]) > self._num_points:
            raise ValueError("X Values must not be longer than {}!".format(len(values[0])))
        elif len(values[1]) > self._num_points:
            raise ValueError("Y Values must not be longer than {}!".format(len(values[1])))

        # use the inputted lists as the buffer starter
        self._x_values = values[0]
        self._y_values = values[1]

        # take the inputted list and get min and max values from it
        self._min_value = min(self._y_values)
        self._max_value = max(self._y_values)
        self._draw()

    def add_value(self, value: tuple):
        if type(value) != tuple:
            raise TypeError("New Value must be a tuple, not {}!".format(type(value)))
        elif type(value[0]) != float:
            raise TypeError("X Value must be float, not {}!".format(type(value[0])))
        elif type(value[1]) != float:
            raise TypeError("Y Value must be float, not {}!".format(type(value[1])))

        # if the buffer is full, dump the first point and tack the newest values on front
        if len(self._x_values) == self._num_points:
            del self._x_values[0]
            del self._y_values[0]
            self._x_values.append(value[0])
            self._y_values.append(value[1])
        # if buffer is not full, just append it and redraw
        else:
            self._x_values.append(value[0])
            self._y_values.append(value[1])

        # if there is only one element in the data, use defaults
        # otherwise calculate the min/max values
        if len(self._x_values) <= 1:
            self._min_value = _DEFAULT_MIN_VALUE
            self._max_value = _DEFAULT_MAX_VALUE
        else:
            self._min_value = min(self._y_values)
            self._max_value = max(self._y_values)
        self._draw()

    def _draw_axes(self):
        self._y_axis_points = [int(self._position[0] + 0.1 * self._plot_area[0]),
                               int(self._position[1] + 0.1 * self._plot_area[1]),
                               int(self._position[0] + 0.1 * self._plot_area[0]),
                               int(self._position[1] + self._plot_area[1])]
        self._x_axis_points = [int(self._position[0] + 0.1 * self._plot_area[0]),
                               int(self._position[1] + 0.1 * self._plot_area[1]),
                               int(self._position[0] + self._plot_area[0]),
                               int(self._position[1] + 0.1 * self._plot_area[1])]
        self._tick_length = int(self._plot_area[1] * _DEFAULT_TICK_RATIO)
        self._tick_gap = (self._x_axis_points[2] - self._x_axis_points[0]) / self._num_points

        # draw the axes
        Line(points=self._y_axis_points, width=2)
        Line(points=self._x_axis_points, width=2)

        # go through and plot out tick marks in a for loop :/
        for i in range(self._num_points):
            Line(points=[self._x_axis_points[0] + self._tick_gap * (i + 1),
                         self._x_axis_points[1] - self._tick_length,
                         self._x_axis_points[0] + self._tick_gap * (i + 1),
                         self._x_axis_points[1]], width=2)

    def _draw_points(self):
        y_steps = self._y_axis_points[3] - self._y_axis_points[1]
        y_steps = y_steps / (self._max_value - self._min_value)
        y_coord = [value - self._min_value for value in self._y_values]
        y_coord = [(value * y_steps) + self._y_axis_points[1] for value in y_coord]

        x_coord = [i * self._tick_gap + self._x_axis_points[0] for i in range(len(self._x_values))]

        for i in range(len(y_coord))[1:]:
            Line(points=[x_coord[i-1], y_coord[i-1], x_coord[i], y_coord[i]])

    def _draw(self):
        """
        Function used to draw the plot on the screen.
        The drawing process is as follows:
            1. Clear canvas
            2. Draw the axes and time marks
            3. Draw the current value on the y axis
            4. Draw the lines between the points
        """
        with self.canvas:
            self.canvas.clear()

            # plot the axes and tick marks
            Color(self._grid_color)
            self._draw_axes()

            self._draw_points()
