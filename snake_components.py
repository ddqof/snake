#!/usr/bin/env python3

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
        """Движение змейки"""

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

    def check_obstacles(self):
        """Проверка встречи всевозможных препятствий при движении"""

        self.check_self_eating()
        self.check_eat()
        self.check_walls()

    def check_self_eating(self):
        """Проверка столкновения какого-либо блока змейки с другим блоком"""

        for i in range(len(self.blocks) - 1):
            for j in range(1, len(self.blocks)):
                if (i != j and self.master.coords(self.blocks[i].image) ==
                        self.master.coords(self.blocks[j].image)):
                    self.master.finish_the_game()

    def check_eat(self):
        """Проверка содержание еды по координатам «головы» змейки"""

        if (self.master.coords(self.blocks[0].image) ==
                self.master.coords(self.master.food)):
            self.master.update_score()
            self.master.update_text()
            self.master.delete(self.master.food)
            self.blocks.append(
                Block(self.master.coords(self.blocks[-1].image)[0],
                      self.master.coords(self.blocks[-1].image)[1],
                      self.master))
            self.master.create_food()

    def check_walls(self):
        """Проверка на столкновение змейки со стеной"""

        if (self.master.coords(self.blocks[0].image)[2] > WIDTH or
                self.master.coords(self.blocks[0].image)[0] < 0 or
                self.master.coords(self.blocks[0].image)[3] > HEIGHT or
                self.master.coords(self.blocks[0].image)[1] < 0):
            self.master.finish_the_game()
