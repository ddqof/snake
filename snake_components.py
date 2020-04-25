#!/usr/bin/env python3
import tkinter as tk
from config import WIDTH, HEIGHT, BLOCK_SIZE


class Vector:
    """Компонент «вектор змейки»"""

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Block:
    """Компонент «блок змейки»"""

    def __init__(self, x, y, canvas):
        self.image = canvas.create_rectangle(x, y,
                                             x + BLOCK_SIZE, y + BLOCK_SIZE,
                                             fill='white')


class Snake:
    """Компонент «змейка»"""

    def __init__(self, blocks, canvas):
        self.blocks = blocks
        self.canvas = canvas
        self.vector = Vector(1, 0)
        self.IN_GAME = True

    def move(self):
        print(self.canvas.coords(self.canvas.eat))
        for index in reversed(range(1, len(self.blocks))):
            block = self.blocks[index].image
            x1, y1, x2, y2 = self.canvas.coords(self.blocks[index - 1].image)
            self.canvas.coords(block, x1, y1, x2, y2)

        x1, y1, x2, y2 = self.canvas.coords(self.blocks[0].image)
        self.canvas.coords(self.blocks[0].image,
                           x1 + self.vector.x * BLOCK_SIZE,
                           y1 + self.vector.y * BLOCK_SIZE,
                           x2 + self.vector.x * BLOCK_SIZE,
                           y2 + self.vector.y * BLOCK_SIZE)
        self.check_obstacles()

    def check_obstacles(self):
        self.check_eat()
        self.check_walls()

    def check_eat(self):
        if len(self.canvas.coords(self.canvas.eat)) != 0:
            if self.canvas.coords(self.blocks[0].image) == self.canvas.coords(self.canvas.eat):
                self.canvas.delete(self.canvas.eat)

    def check_walls(self):
        if (self.canvas.coords(self.blocks[0].image)[2] > WIDTH or
                self.canvas.coords(self.blocks[0].image)[0] < 0 or
                self.canvas.coords(self.blocks[0].image)[3] > HEIGHT or
                self.canvas.coords(self.blocks[0].image)[1] < 0):
            self.IN_GAME = False
            self.canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Game Over",
                                    justify=tk.CENTER, font="Verdana 18",
                                    fill="white")

    def key_handle(self, event):
        if event.keycode == 83 or event.keycode == 40:
            if self.vector.y == 0 and self.IN_GAME:
                self.vector = Vector(0, 1)
                self.move()

        if event.keycode == 87 or event.keycode == 38:
            if self.vector.y == 0 and self.IN_GAME:
                self.vector = Vector(0, -1)
                self.move()

        if event.keycode == 68 or event.keycode == 39:
            if self.vector.x == 0 and self.IN_GAME:
                self.vector = Vector(1, 0)
                self.move()

        if event.keycode == 65 or event.keycode == 37:
            if self.vector.x == 0 and self.IN_GAME:
                self.vector = Vector(-1, 0)
                self.move()
