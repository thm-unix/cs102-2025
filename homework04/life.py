import pathlib
import random
import typing as tp
import copy

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0] * self.cols for _ in range(self.rows)]
        if randomize:
            for i, row in enumerate(grid):
                for j, column in enumerate(row):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbors = []
        if cell[0] > 0:
            neighbors.append((cell[0] - 1, cell[1]))
        if cell[1] > 0:
            neighbors.append((cell[0], cell[1] - 1))
        if cell[0] > 0 and cell[1] > 0:
            neighbors.append((cell[0] - 1, cell[1] - 1))

        if cell[0] < self.rows - 1:
            neighbors.append((cell[0] + 1, cell[1]))
        if cell[0] < self.rows - 1 and cell[1] > 0:
            neighbors.append((cell[0] + 1, cell[1] - 1))

        if cell[1] < self.cols - 1:
            neighbors.append((cell[0], cell[1] + 1))
        if cell[1] < self.cols - 1 and cell[0] > 0:
            neighbors.append((cell[0] - 1, cell[1] + 1))
        if cell[1] < self.cols - 1 and cell[0] < self.rows - 1:
            neighbors.append((cell[0] + 1, cell[1] + 1))

        final = [self.curr_generation[row][column] for row, column in neighbors]
        return final

    def get_next_generation(self) -> Grid:
        next_grid = []
        for row in range(self.rows):
            next_row = []
            for column in range(self.cols):
                cell = self.curr_generation[row][column]
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

    def step(self) -> None:
        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if not self.max_generations:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        with open(filename, "r") as file:
            lines = [line.strip() for line in file.readlines()]
        rows = len(lines)
        cols = len(lines[0]) if rows > 0 else 0
        game = GameOfLife((rows, cols), randomize=False, max_generations=None)
        for i, line in enumerate(lines):
            for j, symbol in enumerate(line):
                game.curr_generation[i][j] = int(symbol == "1")
        return game

    def save(self, filename: pathlib.Path) -> None:
        with open(filename, "w") as file:
            for row in self.curr_generation:
                line = "".join(str(col) for col in row)
                file.write(f"{line}\n")
