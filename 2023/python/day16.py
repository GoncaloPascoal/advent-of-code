
"""
Day 16 - The Floor Will Be Lava
"""

from dataclasses import dataclass
from typing import Self, NamedTuple

import numpy as np


def parse_input() -> np.ndarray:
    with open('data/day16.txt', encoding='utf8') as f:
        return np.array([list(line) for line in f.read().splitlines()])

class Vector2D(NamedTuple):
    row: int
    col: int

    def __add__(self, other: Self) -> Self:
        return Vector2D(self.row + other.row, self.col + other.col)

    def rotate_left(self) -> Self:
        return Vector2D(-self.col, self.row)

    def rotate_right(self) -> Self:
        return Vector2D(self.col, -self.row)


Vector2D.ZERO = Vector2D(0, 0)

Vector2D.UP = Vector2D(-1, 0)
Vector2D.DOWN = Vector2D(1, 0)
Vector2D.LEFT = Vector2D(0, -1)
Vector2D.RIGHT = Vector2D(0, 1)

@dataclass
class Beam:
    position: Vector2D
    velocity: Vector2D

    def move(self):
        self.position += self.velocity

    def rotate_left(self):
        self.velocity = self.velocity.rotate_left()

    def rotate_right(self):
        self.velocity = self.velocity.rotate_right()

    @property
    def horizontal(self) -> bool:
        return self.velocity.row == 0

    @property
    def vertical(self) -> bool:
        return self.velocity.col == 0

def is_inside_grid(grid: np.ndarray, position: Vector2D) -> bool:
    return 0 <= position.row < grid.shape[0] and 0 <= position.col < grid.shape[1]

def calculate_energized_tiles(grid: np.ndarray, start_beam: Beam) -> int:
    beams = [start_beam]
    energized = set()
    used_splitters = set()

    while beams:
        new_beams = []

        for beam in beams:
            if is_inside_grid(grid, beam.position):
                energized.add(beam.position)
                cell = grid[*beam.position]

                match cell:
                    case '/':
                        if beam.horizontal:
                            beam.rotate_left()
                        else:
                            beam.rotate_right()

                        beam.move()
                        new_beams.append(beam)
                    case '\\':
                        if beam.horizontal:
                            beam.rotate_right()
                        else:
                            beam.rotate_left()

                        beam.move()
                        new_beams.append(beam)
                    case '-' if beam.vertical:
                        if beam.position not in used_splitters:
                            beam_left = Beam(beam.position, Vector2D.LEFT)
                            beam_right = Beam(beam.position, Vector2D.RIGHT)

                            beam_left.move()
                            beam_right.move()

                            new_beams.append(beam_left)
                            new_beams.append(beam_right)

                            used_splitters.add(beam.position)
                    case '|' if beam.horizontal:
                        if beam.position not in used_splitters:
                            beam_up = Beam(beam.position, Vector2D.UP)
                            beam_down = Beam(beam.position, Vector2D.DOWN)

                            beam_up.move()
                            beam_down.move()

                            new_beams.append(beam_up)
                            new_beams.append(beam_down)

                            used_splitters.add(beam.position)
                    case _:
                        beam.move()
                        new_beams.append(beam)

        beams = new_beams

    return len(energized)


def part_1(grid: np.ndarray) -> int:
    return calculate_energized_tiles(grid, Beam(Vector2D.ZERO, Vector2D.RIGHT))

def part_2(grid: np.ndarray) -> int:
    max_energized_tiles = 0
    num_rows, num_cols = grid.shape

    for i in range(num_rows):
        max_energized_tiles = max(
            max_energized_tiles,
            calculate_energized_tiles(grid, Beam(Vector2D(i, 0), Vector2D.RIGHT)),
            calculate_energized_tiles(grid, Beam(Vector2D(i, num_cols - 1), Vector2D.LEFT))
        )

    for j in range(num_cols):
        max_energized_tiles = max(
            max_energized_tiles,
            calculate_energized_tiles(grid, Beam(Vector2D(0, j), Vector2D.DOWN)),
            calculate_energized_tiles(grid, Beam(Vector2D(num_rows - 1, j), Vector2D.UP))
        )

    return max_energized_tiles


def main():
    grid = parse_input()
    print(part_1(grid))
    print(part_2(grid))


if __name__ == '__main__':
    main()
