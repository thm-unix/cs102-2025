import multiprocessing
import pathlib
import sys
import typing as tp
from itertools import product
from math import sqrt
from random import choice, shuffle

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "")
                for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    grouped = []
    i = 0
    current_list = []
    for elem in values:
        current_list.append(elem)
        i += 1
        if i == n:
            grouped.append(current_list.copy())
            current_list = []
            i = 0
    return grouped


def get_row(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    transposed_grid = [row for row in zip(*grid)]
    return list(transposed_grid[pos[1]])


def get_block(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    square_size = int(sqrt(len(grid)))
    vertical_square_index = pos[0] // square_size
    horizontal_square_index = pos[1] // square_size

    v_start_index = vertical_square_index * square_size
    v_end_index = v_start_index + square_size
    v_part = grid[v_start_index:v_end_index]

    h_start_index = horizontal_square_index * square_size
    h_end_index = h_start_index + square_size

    result = []
    for item in v_part:
        result += item[h_start_index:h_end_index]

    return result


def find_empty_positions(
    grid: tp.List[tp.List[str]],
) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i, row in enumerate(grid):
        for j, column in enumerate(row):
            if column == ".":
                return (i, j)
    return None


def find_possible_values(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    possible_values = set([str(x) for x in range(1, 10)])
    current_block = set(get_block(grid, pos))
    row_values = set(get_row(grid, pos))
    column_values = set(get_col(grid, pos))
    return possible_values - current_block - row_values - column_values


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение пазла, заданного в grid"""
    """ Как решать Судоку?
	    1. Найти свободную позицию
	    2. Найти все возможные значения, которые могут находиться на этой позиции
	    3. Для каждого возможного значения:
	        3.1. Поместить это значение на эту позицию
	        3.2. Продолжить решать оставшуюся часть пазла
	>>> grid = read_sudoku('puzzle1.txt')
	>>> solve(grid)
	[['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
	"""
    position = find_empty_positions(grid)
    if position is None:
        return grid

    values = list(find_possible_values(grid, position))
    shuffle(values)
    for value in values:
        grid[position[0]][position[1]] = value
        if solve(grid):
            return grid
        grid[position[0]][position[1]] = "."
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    # TODO: Add doctests with bad puzzles
    for i, row in enumerate(solution):
        for j, column in enumerate(row):
            block = get_block(solution, (i, j))
            if len(block) != len(set(block)) or "." in block:
                return False

            grid_row = get_row(solution, (i, j))
            if len(grid_row) != len(set(grid_row)) or "." in grid_row:
                return False

            grid_column = get_col(solution, (i, j))
            if len(grid_column) != len(set(grid_column)) or "." in grid_column:
                return False
    return True


def generate_sudoku(N: int) -> tp.Optional[tp.List[tp.List[str]]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    SQUARE_SIZE_SQ = 9
    if N > SQUARE_SIZE_SQ**2:
        print("N is bigger than amount of cells in the grid.", file=sys.stderr)
        return []

    my_grid = []
    for _ in range(SQUARE_SIZE_SQ):
        my_grid.append(["."] * SQUARE_SIZE_SQ)
    solution = solve(my_grid)
    if solution is None:
        return None

    indexes = [value for value in product(range(SQUARE_SIZE_SQ), repeat=2)]
    for _ in range(SQUARE_SIZE_SQ**2 - N):
        cell = choice(indexes)
        solution[cell[0]][cell[1]] = "."
        indexes.remove(cell)
    return solution


def run_solve(filename):
    grid = read_sudoku(fname)
    solution = solve(grid)
    if not solution:
        print(f"Puzzle {fname} can't be solved")
    else:
        display(solution)


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        p = multiprocessing.Process(target=run_solve, args=(fname,))
        p.start()
