
"""
Day 3 - Rucksack Reorganization
"""

import itertools


def parse_input() -> list[str]:
    with open('data/day03.txt', encoding='utf8') as f:
        return [line.strip() for line in f.readlines()]

def priority(item: str) -> int:
    # Priority is equal to the code point of the character with a certain offset
    return ord(item) + (27 - ord('A') if item.isupper() else 1 - ord('a'))


def part_1(rucksacks: list[str]) -> int:
    sum_priorities = 0

    for rucksack in rucksacks:
        compartment_size = len(rucksack) // 2
        first, second = rucksack[:compartment_size], rucksack[compartment_size:]

        common_element = (set(first) & set(second)).pop()
        sum_priorities += priority(common_element)

    return sum_priorities

def part_2(rucksacks: list[str]) -> int:
    sum_priorities = 0

    it = iter(rucksacks)
    while group := list(itertools.islice(it, 3)):
        items = set(group[0])
        items.intersection_update(*group[1:])

        common_element = items.pop()
        sum_priorities += priority(common_element)

    return sum_priorities


def main():
    rucksacks = parse_input()
    print(part_1(rucksacks))
    print(part_2(rucksacks))


if __name__ == '__main__':
    main()
