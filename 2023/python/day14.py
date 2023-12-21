
"""
Day 14 - Parabolic Reflector Dish
"""

from enum import Enum, auto
from typing import Final

import numpy as np


EMPTY: Final[int] = 0
CUBE_ROCK: Final[int] = 1
ROUNDED_ROCK: Final[int] = 2

TOTAL_CYCLES: Final[int] = 1_000_000_000

def cell_to_int(cell: str) -> int:
    match cell:
        case '.':
            return EMPTY
        case '#':
            return CUBE_ROCK
        case 'O':
            return ROUNDED_ROCK
        case _:
            raise ValueError

def parse_input() -> np.ndarray:
    with open('data/day14.txt', encoding='utf8') as f:
        grid = [[cell_to_int(cell) for cell in line] for line in f.read().splitlines()]

    return np.array(grid)


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    WEST = auto()
    EAST = auto()

def move_rocks(grid: np.ndarray, direction: Direction) -> np.ndarray:
    vertical = direction in (Direction.NORTH, Direction.SOUTH)

    main_axis_size = grid.shape[int(vertical)]
    cross_axis_size = grid.shape[int(not vertical)]

    rocks_along_line = [[] for _ in range(main_axis_size)]

    match direction:
        case Direction.NORTH:
            grid_transformed = grid.transpose()
        case Direction.SOUTH:
            grid_transformed = np.flipud(grid).transpose()
        case Direction.WEST:
            grid_transformed = grid
        case Direction.EAST:
            grid_transformed = np.fliplr(grid)
        case _:
            assert False, 'Unreachable'

    for line_idx, line in enumerate(grid_transformed):
        current_cross = 0
        num_rocks = 0

        for cross_idx, cell in enumerate(line):
            if cell == CUBE_ROCK:
                rocks_along_line[line_idx].append((current_cross, num_rocks))
                current_cross = cross_idx + 1
                num_rocks = 0
            elif cell == ROUNDED_ROCK:
                num_rocks += 1

        if num_rocks or current_cross > 0:
            rocks_along_line[line_idx].append((current_cross, num_rocks))

    new_grid = [[] for _ in range(main_axis_size)]
    for new_line, rock_positions in zip(new_grid, rocks_along_line):
        for rock_idx, num_rocks in rock_positions:
            if rock_idx > 0:
                num_empty_cells = rock_idx - len(new_line) - 1
                new_line.extend([EMPTY] * num_empty_cells)
                new_line.append(CUBE_ROCK)

            new_line.extend([ROUNDED_ROCK] * num_rocks)

        num_empty_cells = cross_axis_size - len(new_line)
        new_line.extend([EMPTY] * num_empty_cells)

    match direction:
        case Direction.NORTH:
            return np.transpose(new_grid)
        case Direction.SOUTH:
            return np.flipud(np.transpose(new_grid))
        case Direction.WEST:
            return np.array(new_grid)
        case Direction.EAST:
            return np.fliplr(new_grid)
        case _:
            assert False, 'Unreachable'

def calculate_load(grid: np.ndarray) -> int:
    load = 0
    num_rows = grid.shape[0]

    for i, row in enumerate(grid):
        load += (num_rows - i) * np.count_nonzero(row == ROUNDED_ROCK)

    return load

def part_1(grid: np.ndarray) -> int:
    return calculate_load(move_rocks(grid, Direction.NORTH))

def perform_cycle(grid: np.ndarray) -> np.ndarray:
    grid = move_rocks(grid, Direction.NORTH)
    grid = move_rocks(grid, Direction.WEST)
    grid = move_rocks(grid, Direction.SOUTH)
    grid = move_rocks(grid, Direction.EAST)

    return grid

def part_2(grid: np.ndarray, use_tortoise_hare: bool = False) -> int:
    if use_tortoise_hare:
        # Slower in practice but uses O(1) memory
        tortoise, hare = grid.copy(), grid.copy()

        tortoise = perform_cycle(tortoise)
        hare = perform_cycle(perform_cycle(hare))
        while not np.array_equal(tortoise, hare):
            tortoise = perform_cycle(tortoise)
            hare = perform_cycle(perform_cycle(hare))

        cycle_start = 0
        tortoise = grid
        while not np.array_equal(tortoise, hare):
            tortoise = perform_cycle(tortoise)
            hare = perform_cycle(hare)
            cycle_start += 1

        cycle_length = 1
        hare = perform_cycle(tortoise)
        while not np.array_equal(tortoise, hare):
            hare = perform_cycle(hare)
            cycle_length += 1

        new_grid = hare
    else:
        grids_seen = {}
        cycle_length = 0

        new_grid = grid
        while True:
            cycle_length += 1
            new_grid = perform_cycle(new_grid)
            flat = tuple(new_grid.flat)

            if flat in grids_seen:
                cycle_start = grids_seen[flat]
                cycle_length = cycle_length - cycle_start
                break
            else:
                grids_seen[flat] = cycle_length

    remaining_cycles = (1_000_000_000 - cycle_start) % cycle_length
    for i in range(remaining_cycles):
        new_grid = perform_cycle(new_grid)

    return calculate_load(new_grid)


def main():
    grid = parse_input()
    print(part_1(grid))
    print(part_2(grid))


if __name__ == '__main__':
    main()
