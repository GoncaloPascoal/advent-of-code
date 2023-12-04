
"""
Day 3 - Gondola Lift
"""

import functools
import re
from typing import Final


def parse_input() -> list[str]:
    with open('data/day03.txt', encoding='utf8') as f:
        return f.readlines()


NUMBER_REGEX: Final[str] = r'\d+'
SYMBOL_REGEX: Final[str] = r'[^\d\.]'
GEAR_REGEX: Final[str] = r'\*'

def part_1(data: list[str]) -> int:
    sum_parts = 0

    for i, line in enumerate(data):
        line = line.strip()

        for match in re.finditer(NUMBER_REGEX, line):
            start, end = match.span()

            start = max(start - 1, 0)
            end = min(end + 1, len(line))

            # If there is a symbol (not a digit or a dot) in the surrounding characters
            if (
                (i > 0 and re.search(SYMBOL_REGEX, data[i - 1][start:end])) or           # Previous line
                (re.search(SYMBOL_REGEX, data[i][start] + data[i][end - 1])) or          # Current line
                (i < len(data) - 1 and re.search(SYMBOL_REGEX, data[i + 1][start:end]))  # Next line
            ):
                sum_parts += int(match.group())

    return sum_parts

def part_2(data: list[str]) -> int:
    sum_gear_ratios = 0
    gear_to_numbers = {}

    # Record part numbers adjacent to each gear (dictionary key is the gear's coordinates)
    for i, line in enumerate(data):
        line = line.strip()

        for number_match in re.finditer(NUMBER_REGEX, line):
            start, end = number_match.span()

            start = max(start - 1, 0)
            end = min(end + 1, len(line))

            def append_match(match: re.Match, line_idx: int, col_idx: int):
                gear_to_numbers.setdefault((line_idx, col_idx), []).append(int(match.group()))
            append_match = functools.partial(append_match, number_match)

            if i > 0:
                for gear_match in re.finditer(GEAR_REGEX, data[i - 1][start:end]):
                    append_match(i - 1, start + gear_match.start())

            for idx in (start, end - 1):
                if data[i][idx] == '*':
                    append_match(i, idx)

            if i < len(data) - 1:
                for gear_match in re.finditer(SYMBOL_REGEX, data[i + 1][start:end]):
                    append_match(i + 1, start + gear_match.start())

    for numbers in gear_to_numbers.values():
        if len(numbers) == 2:
            x, y = numbers
            sum_gear_ratios += x * y

    return sum_gear_ratios


def main():
    data = parse_input()
    print(part_1(data))
    print(part_2(data))


if __name__ == '__main__':
    main()
