
"""
Day 2 - Cube Conundrum
"""

import re
from math import prod
from typing import TypeAlias

Draw: TypeAlias = tuple[int, int, int]  # Red, Green, Blue
Game: TypeAlias = list[Draw]

def parse_input() -> list[Game]:
    with open('data/day02.txt', encoding='utf8') as f:
        lines = f.readlines()

    games = []
    for line in lines:
        game = []
        line = line.split(':')[1].strip()

        for draw_str in line.split(';'):
            draw = tuple(
                int(match.group(1))
                if (match := re.search(f'(\\d+) {color}', draw_str)) is not None else 0
                for color in ['red', 'green', 'blue']
            )
            game.append(draw)

        games.append(game)

    return games


def part_1(games: list[Game]) -> int:
    max_draw = (12, 13, 14)
    sum_ids = 0

    for i, game in enumerate(games):
        for draw in game:
            if any(num_cubes > max_cubes for num_cubes, max_cubes in zip(draw, max_draw)):
                break
        else:
            sum_ids += i + 1

    return sum_ids

def part_2(games: list[Game]) -> int:
    sum_powers = 0

    for game in games:
        min_cubes = [0] * 3
        for draw in game:
            for i, num_cubes in enumerate(draw):
                min_cubes[i] = max(min_cubes[i], num_cubes)
        sum_powers += prod(min_cubes)

    return sum_powers


def main():
    games = parse_input()
    print(part_1(games))
    print(part_2(games))


if __name__ == '__main__':
    main()
