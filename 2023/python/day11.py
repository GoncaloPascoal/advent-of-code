
"""
Day 11 - Cosmic Expansion
"""

import itertools


def parse_input() -> list[str]:
    with open('data/day11.txt', encoding='utf8') as f:
        return [line.strip() for line in f.readlines()]


def empty_row_indices(universe: list[str]) -> set[int]:
    return set(i for i, row in enumerate(universe) if '#' not in row)

def empty_col_indices(universe: list[str]) -> set[int]:
    return set(j for j in range(len(universe[0])) if all(line[j] == '.' for line in universe))

def calculate_sum_distances(universe: list[str], expansion_factor: int) -> int:
    sum_distances = 0
    galaxy_positions = set()

    for i, line in enumerate(universe):
        for j, character in enumerate(line):
            if character == '#':
                galaxy_positions.add((i, j))

    empty_rows, empty_cols = empty_row_indices(universe), empty_col_indices(universe)

    # Use Manhattan distance
    for g1, g2 in itertools.combinations(galaxy_positions, 2):
        distance = 0

        min_row, max_row = (g1[0], g2[0]) if g1[0] < g2[0] else (g2[0], g1[0])
        rows = set(range(min_row, max_row))
        num_empty = len(empty_rows & rows)
        distance += expansion_factor * num_empty + len(rows) - num_empty

        min_col, max_col = (g1[1], g2[1]) if g1[1] < g2[1] else (g2[1], g1[1])
        cols = set(range(min_col, max_col))
        num_empty = len(empty_cols & cols)
        distance += expansion_factor * num_empty + len(cols) - num_empty

        sum_distances += distance

    return sum_distances

def part_1(universe: list[str]) -> int:
    return calculate_sum_distances(universe, 2)

def part_2(universe: list[str]) -> int:
    return calculate_sum_distances(universe, 1_000_000)


def main():
    # TODO: use a NumPy array for optimization
    universe = parse_input()
    print(part_1(universe))
    print(part_2(universe))


if __name__ == '__main__':
    main()
