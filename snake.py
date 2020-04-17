#!/usr/bin/env python3

import tkinter as tk

WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 20
SNAKE_SPEED = 20


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Block:
    def __init__(self, x, y, canvas):
        self.image = canvas.create_rectangle(x, y,
                                             x + BLOCK_SIZE, y + BLOCK_SIZE,
                                             fill='white')


class Snake:
    def __init__(self, blocks, canvas):
        self.blocks = blocks
        self.canvas = canvas
        self.vector = Vector(1, 0)
        self.IN_GAME = True

    def move(self):
        for index in reversed(range(1, len(self.blocks))):
            block = self.blocks[index].image
            x1, y1, x2, y2 = self.canvas.coords(self.blocks[index - 1].image)
            self.canvas.coords(block, x1, y1, x2, y2)

        x1, y1, x2, y2 = self.canvas.coords(self.blocks[1].image)

        self.canvas.coords(self.blocks[0].image,
                           x1 + self.vector.x * BLOCK_SIZE,
                           y1 + self.vector.y * BLOCK_SIZE,
                           x2 + self.vector.x * BLOCK_SIZE,
                           y2 + self.vector.y * BLOCK_SIZE)

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
            if self.vector.y != -1:
                self.vector = Vector(0, 1)

        if event.keycode == 87 or event.keycode == 38:
            if self.vector.y != 1:
                self.vector = Vector(0, -1)

        if event.keycode == 68 or event.keycode == 39:
            if self.vector.x != -1:
                self.vector = Vector(1, 0)

        if event.keycode == 65 or event.keycode == 37:
            if self.vector.x != 1:
                self.vector = Vector(-1, 0)


class Engine:
    def __init__(self, root, snake):
        self.root = root
        self.snake = snake

    def start_game(self):
        self.snake.move()
        if self.snake.IN_GAME:
            self.root.after(int(1/SNAKE_SPEED *  1000), self.start_game)


def main():
    root = tk.Tk()
    root.title("Snake")
    c = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#3F888F")
    c.pack()
    c.focus_set()
    # tk.Label(text="Score: {0}\n"
    #                    "High Score: {1}".format(SCORE, HIGH_SCORE),
    #               width=20, height=3).pack()
    blocks = [Block(BLOCK_SIZE * 3, BLOCK_SIZE, c),
              Block(BLOCK_SIZE * 2, BLOCK_SIZE, c),
              Block(BLOCK_SIZE, BLOCK_SIZE, c)]
    snake = Snake(blocks, c)
    c.bind("<KeyPress>", snake.key_handle)
    game_engine = Engine(root, snake)
    game_engine.start_game()

    root.mainloop()


if __name__ == '__main__':
    main()
