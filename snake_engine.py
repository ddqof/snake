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
        self.blocks = [snake_components.Block(BLOCK_SIZE * 3, BLOCK_SIZE, self),
                       snake_components.Block(BLOCK_SIZE * 2, BLOCK_SIZE, self),
                       snake_components.Block(BLOCK_SIZE, BLOCK_SIZE, self)]
        self.snake = snake_components.Snake(self.blocks, self)
        self.eat = 0
        self.create_eat()
        self.bind("<KeyPress>", self.snake.key_handle)
        self.IN_GAME = True

    def play(self):
        self.snake.move()
        if self.IN_GAME:
            self.root.after(int(1 / SNAKE_SPEED * 1000), self.play)

    def create_eat(self):  # тест несколько раз еда может попасть на змейку
        block_coords = {}
        eat_x1 = BLOCK_SIZE * random.randint(1, BLOCK_SIZE * ((WIDTH / BLOCK_SIZE ** 2) - 1))
        eat_y1 = BLOCK_SIZE * random.randint(1, (HEIGHT * BLOCK_SIZE) / (BLOCK_SIZE ** 2) - BLOCK_SIZE)
        eat_x2 = eat_x1 + BLOCK_SIZE
        eat_y2 = eat_y1 + BLOCK_SIZE
        eat = (eat_x1, eat_y1, eat_x2, eat_y2)
        for index in range(len(self.blocks)):
            block_coords[index] = tuple(self.coords(self.blocks[index].image))
        if eat not in block_coords.values():
            self.eat = self.create_oval(eat[0], eat[1], eat[2], eat[3], fill="red")
        else:
            self.create_eat()
        return eat

    def finish_the_game(self):
        self.IN_GAME = False
        self.create_text(WIDTH / 2, HEIGHT / 2, text="Game Over",
                         justify=tk.CENTER, font="Verdana 18",
                         fill="white")


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