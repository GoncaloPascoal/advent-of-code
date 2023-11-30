
"""
Day 4 - Camp Cleanup
"""

from typing import TypeAlias


SectionPair: TypeAlias = tuple[int, int]
PuzzleInput: TypeAlias = list[tuple[SectionPair, SectionPair]]


def parse_input() -> PuzzleInput:
    with open('data/day04.txt', encoding='utf8') as f:
        lines = f.readlines()

    data = []
    for line in lines:
        pairs = tuple(tuple(map(int, pair.split('-'))) for pair in line.split(','))
        data.append(pairs)
    return data


def contains(p1: SectionPair, p2: SectionPair) -> bool:
    return p1[0] <= p2[0] and p1[1] >= p2[1]

def part_1(data: PuzzleInput) -> int:
    num_fully_contained = 0

    for (p1, p2) in data:
        if contains(p1, p2) or contains(p2, p1):
            num_fully_contained += 1

    return num_fully_contained

def part_2(data: PuzzleInput) -> int:
    num_overlapping = 0

    for (p1, p2) in data:
        overlap_min = max(p1[0], p2[0])
        overlap_max = min(p1[1], p2[1])

        if overlap_min <= overlap_max:
            num_overlapping += 1

    return num_overlapping


def main():
    data = parse_input()
    print(part_1(data))
    print(part_2(data))


if __name__ == '__main__':
    main()
