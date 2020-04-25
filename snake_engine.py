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
        self.eat = self.create_eat()
        self.blocks = [snake_components.Block(BLOCK_SIZE * 3, BLOCK_SIZE, self),
                       snake_components.Block(BLOCK_SIZE * 2, BLOCK_SIZE, self),
                       snake_components.Block(BLOCK_SIZE, BLOCK_SIZE, self)]
        self.snake = snake_components.Snake(self.blocks, self)
        self.bind("<KeyPress>", self.snake.key_handle)

    def play_game(self):
        self.snake.move()
        if self.snake.IN_GAME:
            self.root.after(int(1 / SNAKE_SPEED * 1000), self.play_game)

    def create_eat(self):
        x1 = BLOCK_SIZE * random.randint(1, BLOCK_SIZE * ((WIDTH / BLOCK_SIZE ** 2) - 1))
        y1 = BLOCK_SIZE * random.randint(1, (HEIGHT * BLOCK_SIZE) / (BLOCK_SIZE ** 2) - BLOCK_SIZE)
        x2 = x1 + BLOCK_SIZE
        y2 = y1 + BLOCK_SIZE
        eat = self.create_oval(x1, y1, x2, y2, fill="red")
        return eat


def main():
    """Запуск игрового процесса"""

    parse_args()
    root = tk.Tk()
    root.title("Snake")
    game_engine = Master(root, width=WIDTH, height=HEIGHT, bg="black")
    game_engine.pack()
    game_engine.focus_set()
    game_engine.play_game()

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
