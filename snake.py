#!/usr/bin/env python3

import argparse
import snake_engine
import tkinter as tk
import snake_components
from config import BLOCK_SIZE, WIDTH, HEIGHT


class Canvas(tk.Canvas):
    """Компонент «игрвоое поле»"""

    def __init__(self, driver, root, **kwargs):
        super(Canvas, self).__init__(root, kwargs)
        self.root = root
        self.driver = driver
        self.label = tk.Label(text="Score: {0}\nHigh Score: {1}"
                              .format(self.driver.score, self.driver.high_score),
                              width=12, height=10)
        self.label.pack(side=tk.LEFT)
        self.bind("<KeyPress>", self.key_handle)
        self.last_handled_vector = snake_components.Vector(1, 0)

    def update_canvas(self):
        self.delete('all')
        for y in range(len(self.driver.map)):
            for x in range(len(self.driver.map[y])):
                if self.driver.map[y][x] == 9:
                    self.create_rectangle(x * BLOCK_SIZE, y * BLOCK_SIZE, (x + 1) * BLOCK_SIZE,
                                          (y + 1) * BLOCK_SIZE, fill='gray')
                if self.driver.map[y][x] == 1:
                    self.create_rectangle(x * BLOCK_SIZE, y * BLOCK_SIZE, (x + 1) * BLOCK_SIZE,
                                          (y + 1) * BLOCK_SIZE, fill='white')
                if self.driver.map[y][x] == 5:
                    self.create_oval(x * BLOCK_SIZE, y * BLOCK_SIZE, (x + 1) * BLOCK_SIZE,
                                     (y + 1) * BLOCK_SIZE, fill=self.driver.food_types[5])
                if self.driver.map[y][x] == 6:
                    self.create_oval(x * BLOCK_SIZE, y * BLOCK_SIZE, (x + 1) * BLOCK_SIZE,
                                     (y + 1) * BLOCK_SIZE, fill=self.driver.food_types[6])
                if self.driver.map[y][x] == 7:
                    self.create_oval(x * BLOCK_SIZE, y * BLOCK_SIZE, (x + 1) * BLOCK_SIZE,
                                     (y + 1) * BLOCK_SIZE, fill=self.driver.food_types[7])
                if self.driver.map[y][x] == 8:
                    self.create_oval(x * BLOCK_SIZE, y * BLOCK_SIZE, (x + 1) * BLOCK_SIZE,
                                     (y + 1) * BLOCK_SIZE, fill=self.driver.food_types[8])

        self.label.configure(text="Score: {0}\nHigh Score: {1}"
                             .format(self.driver.score, self.driver.high_score),
                             width=12, height=10)
        if not self.driver.in_game:
            self.create_text(
                WIDTH / 2, HEIGHT / 2,
                text="Game Over\nPress 'Enter' or 'Space' button to restart",
                justify=tk.CENTER, font="Verdana {}".format(
                    int(WIDTH / BLOCK_SIZE / 2)),
                fill="cyan")

        # for row in self.driver.map:
        #     for x in row:
        #         print("{:4d}".format(x), end="")
        #     print()

        print('\n')

    def play(self):
        """Запуск игрового процесса"""

        self.driver.snake.move()
        self.driver.snake.check_obstacles()
        self.driver.check_boost_time()
        self.update_canvas()
        self.root.after(int(self.driver.current_update_freq), self.play)

    def key_handle(self, event):
        """Обработка нажатий на клавиши"""

        key = event.keysym
        if key == 's' or key == 'Down':
            if self.driver.snake.last_handled_vector.y == 0:
                self.driver.snake.vector = snake_components.Vector(0, 1)

        if key == 'w' or key == 'Up':
            if self.driver.snake.last_handled_vector.y == 0:
                self.driver.snake.vector = snake_components.Vector(0, -1)

        if key == 'd' or key == 'Right':
            if self.driver.snake.last_handled_vector.x == 0:
                self.driver.snake.vector = snake_components.Vector(1, 0)

        if key == 'a' or key == 'Left':
            if self.driver.snake.last_handled_vector.x == 0:
                self.driver.snake.vector = snake_components.Vector(-1, 0)

        if (key == 'space' or key == 'Return') and not self.driver.in_game:
            self.driver.restart_the_game()


def main():
    """Подготовка к запуску игрового процесса"""

    args = parse_args()
    root = tk.Tk()
    root.title("Snake")
    game_engine = snake_engine.Driver(3, args.v)
    game_gui = Canvas(game_engine, root, width=WIDTH, height=HEIGHT, bg="black")
    game_gui.pack()
    game_gui.focus_set()
    game_gui.play()

    root.mainloop()


def parse_args():
    """Разбор аргуметов запуска"""

    parser = argparse.ArgumentParser(
        prog='snake_engine.py',
        description='''Snake game. Use W-A-S-D or Arrow keys to
        control the snake.''',
        epilog='''Author: Dmitry Podaruev <ddqof.vvv@gmail.com>'''
    )
    parser.add_argument('-v',
                        help='launch vanilla version of game',
                        action='store_true')
    parser.add_argument('-lvl',
                        type=int,
                        help='select game level',
                        default=0)
    return parser.parse_args()


if __name__ == '__main__':
    main()
