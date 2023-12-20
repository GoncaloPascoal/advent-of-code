
"""
Day 13 - Point of Incidence
"""


def parse_input() -> list[list[str]]:
    with open('data/day13.txt', encoding='utf8') as f:
        return [
            pattern.splitlines()
            for pattern in f.read().replace('.', '0').replace('#', '1').split('\n\n')
        ]


def convert_to_int(pattern: list[str]) -> tuple[list[int], list[int]]:
    horizontal = [int(line, 2) for line in pattern]
    vertical = [int(''.join(line[i] for line in pattern), 2) for i in range(len(pattern[0]))]

    return horizontal, vertical

def is_reflection_axis(data: list[int], axis: int) -> bool:
    return all(left == right for left, right in zip(data[axis - 1::-1], data[axis:]))

def part_1(patterns: list[list[str]]) -> int:
    result = 0

    for pattern in patterns:
        horizontal, vertical = convert_to_int(pattern)

        for axis in range(1, len(pattern)):
            if is_reflection_axis(horizontal, axis):
                result += 100 * axis

        for axis in range(1, len(pattern[0])):
            if is_reflection_axis(vertical, axis):
                result += axis

    return result

def is_power_of_two(x: int) -> bool:
    return x & (x - 1) == 0

def is_smudge_axis(data: list[int], axis: int) -> int:
    found_smudge = False

    for left, right in zip(data[axis - 1::-1], data[axis:]):
        xor = left ^ right

        if xor:
            if found_smudge:
                # Already found a smudge
                return False
            elif is_power_of_two(xor):
                # Check if result of XOR is a power of two - i.e., only one location (bit) is different
                found_smudge = True
            else:
                # Too many smudges
                return False

    return found_smudge

def part_2(patterns: list[list[str]]) -> int:
    result = 0

    for pattern in patterns:
        horizontal, vertical = convert_to_int(pattern)

        for axis in range(1, len(pattern)):
            if is_smudge_axis(horizontal, axis):
                result += 100 * axis

        for axis in range(1, len(pattern[0])):
            if is_smudge_axis(vertical, axis):
                result += axis

    return result


def main():
    patterns = parse_input()
    print(part_1(patterns))
    print(part_2(patterns))


if __name__ == '__main__':
    main()

