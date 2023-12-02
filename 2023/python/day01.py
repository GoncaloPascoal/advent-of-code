
"""
Day 1 - Trebuchet?!
"""

import re

def parse_input() -> list[str]:
    with open('data/day01.txt', encoding='utf8') as f:
        return f.readlines()


def part_1(lines: list[str]) -> int:
    regex = r'(\d)'

    def extract_number(line: str):
        occurrences = re.findall(regex, line)
        return int(occurrences[0] + occurrences[-1])

    return sum(extract_number(line) for line in lines)


def part_2(lines: list[str]) -> int:
    digits = {
        digit: str(i + 1)
        for i, digit in enumerate(
            ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        )
    }

    digit_regex = '|'.join(digits)
    regex = f'(?=(\\d|{digit_regex}))'

    def extract_number(line: str):
        occurrences = [match.group(1) for match in re.finditer(regex, line)]

        first, second = occurrences[0], occurrences[-1]
        if len(first) > 1:
            first = digits[first]
        if len(second) > 1:
            second = digits[second]

        return int(first + second)

    return sum(extract_number(line) for line in lines)


def main():
    lines = parse_input()
    print(part_1(lines))
    print(part_2(lines))


if __name__ == '__main__':
    main()
