from cell import Cell
import random
import time

class Maze():
    def __init__(
        self,
        x,
        y,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self._cells = []
        self._x = x
        self._y = y
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        cells = []
        for i in range(self._num_cols):
            col = []
            for j in range(self._num_rows):
                cell = Cell(self._win)
                col.append(cell)
            cells.append(col)
        self._cells = cells

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win == None:
            return
        cell = self._cells[i][j]

        width = self._cell_size_x
        height = self._cell_size_y
        left = self._x + i * width
        top = self._y + j * height
        
        cell.draw(left, top, left + width, top + height)
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)

        last_col = self._num_cols - 1
        last_row = self._num_rows - 1
        self._cells[last_col][last_row].has_bottom_wall = False
        self._draw_cell(last_col, last_row)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_coords_list = []
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_coords_list.append((i - 1, j))
            # top
            if j > 0 and not self._cells[i][j - 1].visited:
                next_coords_list.append((i, j - 1))
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_coords_list.append((i + 1, j))
            # bottom
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_coords_list.append((i, j + 1))
            
            if not next_coords_list:
                self._draw_cell(i, j)
                return
            
            direction = random.randrange(len(next_coords_list))
            next_coords = next_coords_list[direction]

            # left
            if next_coords[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # top
            if next_coords[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            # right
            if next_coords[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # bottom
            if next_coords[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            
            self._break_walls_r(next_coords[0], next_coords[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        # left
        if (
            i > 0
            and not self._cells[i][j].has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            solved = self._solve_r(i - 1, j)
            if solved:
                return True
            self._cells[i][j].draw_move(self._cells[i - 1][j], True)
        # up
        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            solved = self._solve_r(i, j - 1)
            if solved:
                return True
            self._cells[i][j].draw_move(self._cells[i][j - 1], True)
        # right
        if (
            i < self._num_cols - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            solved = self._solve_r(i + 1, j)
            if solved:
                return True
            self._cells[i][j].draw_move(self._cells[i + 1][j], True)
        # down
        if (
            j < self._num_rows - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            solved = self._solve_r(i, j + 1)
            if solved:
                return True
            self._cells[i][j].draw_move(self._cells[i][j + 1], True)
        return False
