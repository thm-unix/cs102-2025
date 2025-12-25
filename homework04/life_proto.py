import random
import typing as tp
from tkinter.ttk import Label

import pygame
from pygame.locals import *

# from turtledemo.sorting_animate import randomize


Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        self.grid: Grid = self.create_grid(True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.grid = self.create_grid(True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()
            # self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0] * self.cell_width for _ in range(self.cell_height)]
        if randomize:
            for i, row in enumerate(grid):
                for j, column in enumerate(row):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def draw_grid(self) -> None:
        for row in range(self.cell_height):
            for column in range(self.cell_width):
                rect = pygame.Rect(column * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)

                color_name = "green" if self.grid[row][column] else "white"
                color = pygame.Color(color_name)

                pygame.draw.rect(self.screen, color, rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbors = []
        if cell[0] > 0:
            neighbors.append((cell[0] - 1, cell[1]))
        if cell[1] > 0:
            neighbors.append((cell[0], cell[1] - 1))
        if cell[0] > 0 and cell[1] > 0:
            neighbors.append((cell[0] - 1, cell[1] - 1))

        if cell[0] < self.cell_height - 1:
            neighbors.append((cell[0] + 1, cell[1]))
        if cell[0] < self.cell_height - 1 and cell[1] > 0:
            neighbors.append((cell[0] + 1, cell[1] - 1))

        if cell[1] < self.cell_width - 1:
            neighbors.append((cell[0], cell[1] + 1))
        if cell[1] < self.cell_width - 1 and cell[0] > 0:
            neighbors.append((cell[0] - 1, cell[1] + 1))
        if cell[1] < self.cell_width - 1 and cell[0] < self.cell_height - 1:
            neighbors.append((cell[0] + 1, cell[1] + 1))

        final = [self.grid[row][column] for row, column in neighbors]
        return final

    def get_next_generation(self) -> Grid:
        next_grid = []
        for row in range(self.cell_height):
            next_row = []
            for column in range(self.cell_width):
                cell = self.grid[row][column]
                neighbors = self.get_neighbours((row, column))
                neighbor_sum = sum(neighbors)
                if cell:
                    value = 1 if neighbor_sum in (2, 3) else 0
                    next_row.append(value)
                else:
                    value = 1 if neighbor_sum == 3 else 0
                    next_row.append(value)
            next_grid.append(next_row)
        return next_grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
