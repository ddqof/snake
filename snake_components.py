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
        self.master = canvas
        self.vector = Vector(1, 0)

    def move(self):
        for index in reversed(range(1, len(self.blocks))):
            block = self.blocks[index].image
            x1, y1, x2, y2 = self.master.coords(self.blocks[index - 1].image)
            self.master.coords(block, x1, y1, x2, y2)

        x1, y1, x2, y2 = self.master.coords(self.blocks[0].image)
        self.master.coords(self.blocks[0].image,
                           x1 + self.vector.x * BLOCK_SIZE,
                           y1 + self.vector.y * BLOCK_SIZE,
                           x2 + self.vector.x * BLOCK_SIZE,
                           y2 + self.vector.y * BLOCK_SIZE)
        self.check_obstacles()
        # TODO: fix strange blocks adding and eat's spawn on snake

    def check_obstacles(self):
        self.check_self_eating()
        self.check_eat()
        self.check_walls()

    def check_self_eating(self):
        for i in range(len(self.blocks) - 1):
            for j in range(1, len(self.blocks)):
                if i != j and self.master.coords(self.blocks[i].image) == self.master.coords(self.blocks[j].image):
                    self.master.finish_the_game()

    def check_eat(self):
        if len(self.master.coords(self.master.eat)) != 0:
            if self.master.coords(self.blocks[0].image) == self.master.coords(self.master.eat):
                self.master.delete(self.master.eat)
                self.blocks.append(Block(self.master.coords(self.blocks[-1].image)[0] * self.vector.x,
                                         self.master.coords(self.blocks[-1].image)[1] * self.vector.y,
                                         self.master))
                self.master.eat = self.master.create_eat()

    def check_walls(self):
        if (self.master.coords(self.blocks[0].image)[2] > WIDTH or
                self.master.coords(self.blocks[0].image)[0] < 0 or
                self.master.coords(self.blocks[0].image)[3] > HEIGHT or
                self.master.coords(self.blocks[0].image)[1] < 0):
            self.master.finish_the_game()

    def key_handle(self, event):
        if event.keycode == 83 or event.keycode == 40:
            if self.vector.y == 0 and self.master.IN_GAME:
                self.vector = Vector(0, 1)
                self.move()

        if event.keycode == 87 or event.keycode == 38:
            if self.vector.y == 0 and self.master.IN_GAME:
                self.vector = Vector(0, -1)
                self.move()

        if event.keycode == 68 or event.keycode == 39:
            if self.vector.x == 0 and self.master.IN_GAME:
                self.vector = Vector(1, 0)
                self.move()

        if event.keycode == 65 or event.keycode == 37:
            if self.vector.x == 0 and self.master.IN_GAME:
                self.vector = Vector(-1, 0)
                self.move()
