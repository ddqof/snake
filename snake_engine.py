#!/usr/bin/env python3

import tkinter as tk
import snake_components
import argparse
import random
from config import SNAKE_SPEED, BLOCK_SIZE, WIDTH, HEIGHT


class Master(tk.Canvas):
    def __init__(self, root, **kwargs):
        super(Master, self).__init__(root, kwargs)
        self.root = root
        self.blocks = [
            snake_components.Block(BLOCK_SIZE * 3, BLOCK_SIZE, self),
            snake_components.Block(BLOCK_SIZE * 2, BLOCK_SIZE, self),
            snake_components.Block(BLOCK_SIZE, BLOCK_SIZE, self)]
        self.snake = snake_components.Snake(self.blocks, self)
        self.food = 0
        self.create_food()
        self.score = 0
        self.high_score = 0
        self.label = tk.Label(text="Score: {0}\n"
                                   "High Score: {1}".format(self.score, self.high_score),
                              width=12, height=10)
        self.label.pack(side=tk.LEFT)
        self.bind("<KeyPress>", self.key_handle)
        self.in_game = True

    def play(self):
        self.snake.move()
        if self.in_game:
            self.root.after(int(1 / SNAKE_SPEED * 1000), self.play)

    def create_food(self):
        block_coords = {}
        food_x1 = BLOCK_SIZE * random.randint(
            1, BLOCK_SIZE * ((WIDTH / BLOCK_SIZE ** 2) - 1))
        food_y1 = BLOCK_SIZE * random.randint(
            1, (HEIGHT * BLOCK_SIZE) / (BLOCK_SIZE ** 2) - BLOCK_SIZE)
        food_x2 = food_x1 + BLOCK_SIZE
        food_y2 = food_y1 + BLOCK_SIZE
        food = (food_x1, food_y1, food_x2, food_y2)
        for index in range(len(self.blocks)):
            block_coords[index] = tuple(self.coords(self.blocks[index].image))
        if food not in block_coords.values():
            self.food = self.create_oval(food[0], food[1], food[2], food[3],
                                         fill="red")
        else:
            self.create_food()

    def finish_the_game(self):
        self.in_game = False
        self.create_text(
            WIDTH / 2, HEIGHT / 2,
            text="Game Over\nPress 'Enter' or 'Space' button to restart",
            justify=tk.CENTER, font="Verdana {}".format(
                int(WIDTH / BLOCK_SIZE / 2)),
            fill="cyan")

    def restart_the_game(self):
        self.delete("all")
        self.score = 0
        self.update_text()
        self.blocks = [
            snake_components.Block(BLOCK_SIZE * 3, BLOCK_SIZE, self),
            snake_components.Block(BLOCK_SIZE * 2, BLOCK_SIZE, self),
            snake_components.Block(BLOCK_SIZE, BLOCK_SIZE, self)]
        self.snake = snake_components.Snake(self.blocks, self)
        self.create_food()
        self.in_game = True
        self.play()

    def update_text(self):
        self.label.configure(text="Score: {0}\n"
                                  "High Score: {1}".format(self.score, self.high_score),
                             width=12, height=10)

    def update_score(self):
        self.score = self.score + 1
        if self.score > self.high_score:
            self.high_score = self.high_score + 1

    def key_handle(self, event):
        key = event.keysym
        if key == 's' or key == 'Down':
            if self.snake.vector.y == 0 and self.in_game:
                self.snake.vector = snake_components.Vector(0, 1)

        if key == 'w' or key == 'Up':
            if self.snake.vector.y == 0 and self.in_game:
                self.snake.vector = snake_components.Vector(0, -1)

        if key == 'd' or key == 'Right':
            if self.snake.vector.x == 0 and self.in_game:
                self.snake.vector = snake_components.Vector(1, 0)

        if key == 'a' or key == 'Left':
            if self.snake.vector.x == 0 and self.in_game:
                self.snake.vector = snake_components.Vector(-1, 0)

        if (key == 'space' or key == 'Return') and not self.in_game:
            self.restart_the_game()


def main():
    """Запуск игрового процесса"""

    parse_args()
    root = tk.Tk()
    root.title("Snake")
    game_engine = Master(root, width=WIDTH, height=HEIGHT, bg="black")
    game_engine.pack()
    game_engine.focus_set()
    game_engine.play()

    root.mainloop()


def parse_args():
    """Разбор аргуметов запуска"""

    parser = argparse.ArgumentParser(
        prog='snake_engine.py',
        description='''Snake game. Use W-A-S-D or Arrow keys to
        control the snake.''',
        epilog='''Author: Dmitry Podaruev <ddqof.vvv@gmail.com>'''
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
