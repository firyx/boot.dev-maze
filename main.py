from graphics import Window
from maze import Maze

def main():
    win = Window(800, 600)
    maze = Maze(100, 100, 40, 30, 20, 10, win)
    solved = maze.solve()
    if solved:
        print("maze was solved")
    else:
        print("maze is not solvable")
    win.wait_for_close()

main()