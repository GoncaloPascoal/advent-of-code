
"""
Day 6 - Wait For It
"""

from typing import TypeAlias
from numbers import Real
from math import ceil, floor, prod, sqrt

PuzzleInput: TypeAlias = tuple[list[int], list[int]]

def parse_input() -> PuzzleInput:
    with open('data/day06.txt', encoding='utf8') as f:
        time_str, distance_str = f.readlines()

    times = [int(x) for x in time_str.removeprefix('Time:').strip().split()]
    distances = [int(x) for x in distance_str.removeprefix('Distance:').strip().split()]

    return times, distances


def solve_quadratic(a: Real, b: Real, c: Real) -> tuple[float, float]:
    discriminant = sqrt(b ** 2 - 4 * a * c)
    return (-b - discriminant) / (2 * a), (-b + discriminant) / (2 * a) 

def winning_combinations(time: int, distance: int) -> int:
    solutions = solve_quadratic(-1, time, -distance)
    low, high = min(solutions), max(solutions)

    return ceil(high - 1) - floor(low + 1) + 1

def part_1(data: PuzzleInput) -> int:
    return prod(winning_combinations(time, distance) for time, distance in zip(*data))

def part_2(data: PuzzleInput) -> int:
    time, distance = (int(''.join(str(x) for x in l)) for l in data)
    return winning_combinations(time, distance)


def main():
    data = parse_input()
    print(part_1(data))
    print(part_2(data))


if __name__ == '__main__':
    main()
