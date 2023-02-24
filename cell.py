from graphics import Line, Point

class Cell():
    def __init__(
        self,
        window=None,
    ):
        self._win = window
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        top_left = Point(x1, y1)
        top_right = Point(x2, y1)
        bottom_left = Point(x1, y2)
        bottom_right = Point(x2, y2)

        border_color, background_color = "black", "gray85"

        if self.has_left_wall:
            Line(top_left, bottom_left).draw(self._win.canvas, border_color)
        else:
            Line(top_left, bottom_left).draw(self._win.canvas, background_color)

        if self.has_right_wall:
            Line(top_right, bottom_right).draw(self._win.canvas, border_color)
        else:
            Line(top_right, bottom_right).draw(self._win.canvas, background_color)

        if self.has_top_wall:
            Line(top_left, top_right).draw(self._win.canvas, border_color)
        else:
            Line(top_left, top_right).draw(self._win.canvas, background_color)

        if self.has_bottom_wall:
            Line(bottom_left, bottom_right).draw(self._win.canvas, border_color)
        else:
            Line(bottom_left, bottom_right).draw(self._win.canvas, background_color)

    def _get_middle(self):
        return Point(round((self._x1 + self._x2)/2), round((self._y1 + self._y2)/2))
 
    def draw_move(self, to_cell, undo=False):
        if self._win == None:
            return
        color = "red"
        if undo:
            color = "blue"
        line = Line(self._get_middle(), to_cell._get_middle())
        line.draw(self._win.canvas, color)
