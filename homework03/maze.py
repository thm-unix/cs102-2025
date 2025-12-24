from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union
from pandas import DataFrame
from enum import Enum

DELTAS = ((0, 1), (1, 0), (-1, 0), (0, -1))
MARKER = '■'

class Direction(Enum):
    UP = 1
    RIGHT = 2


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [[MARKER] * cols for _ in range(rows)]


def remove_wall(grid, coord):
    row, column = coord

    dr, dc = 0, 0
    direction = choice((Direction.UP, Direction.RIGHT))
    if direction == Direction.UP and row - 2 > 0:
        dr = -1
    else:
        if column + 2 < len(grid[0]):
            dc = 1
        elif row - 2 > 0:
            dr = -1
        else:
            return grid

    grid[row + dr][column + dc] = ' '
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for coordinate in empty_cells:
        remove_wall(grid, coordinate)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1
    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"
    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    exits = []
    for i, row in enumerate(grid):
        for j, column in enumerate(row):
            if column == 'X':
                exits.append((i, j))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    for i, row in enumerate(grid):
        for j, column in enumerate(row):
            if column == k:
                for dr, dc in DELTAS:
                    new_row, new_column = i + dr, j + dc
                    if new_row in range(len(grid)) and new_column in range(len(grid[0])):
                        if grid[new_row][new_column] == 0:
                            grid[i+dr][j+dc] = k + 1

    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    row, column = exit_coord
    cell = grid[row][column]
    if not cell or not isinstance(cell, int):
        return

    path = [(row, column)]
    while cell > 1:
        for dr, dc in DELTAS:
            new_row, new_column = row + dr, column + dc
            if new_row in range(len(grid)) and new_column in range(len(grid[0])):
                if grid[new_row][new_column] == cell - 1:
                    row, column = new_row, new_column
                    cell -= 1
                    path.append((row, column))
                    break
        else:
            return
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    row, column = coord
    row_count, column_count = len(grid), len(grid[0])
    if row not in (0, row_count - 1) and column not in (0, column_count - 1):
        return False

    for dr, dc in DELTAS:
        new_row, new_column = row + dr, column + dc
        if new_row in range(row_count) and new_column in range(column_count):
            if grid[new_row][new_column] != MARKER:
                return False
    return True


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    exits = get_exits(grid)
    if len(exits) == 1:
        return grid, exits[0]

    for maze_exit in exits:
        if encircled_exit(grid, maze_exit):
            return grid, None

    grid_cpy = deepcopy(grid)
    for i, row in enumerate(grid_cpy):
        for j, column in enumerate(row):
            if column in ('X', ' '):
                grid_cpy[i][j] = 0

    exit1, exit2 = exits
    grid_cpy[exit1[0]][exit1[1]] = 1

    k = 1
    while grid_cpy[exit2[0]][exit2[1]] == 0:
        previous_grid = deepcopy(grid_cpy)
        make_step(grid_cpy, k)
        if grid_cpy == previous_grid:
            break
        k += 1

    if not grid_cpy[exit2[0]][exit2[1]]:
        return grid_cpy, None

    return grid_cpy, shortest_path(grid_cpy, exit2)

def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(DataFrame(MAZE))
