
"""
Day 5 - If You Give A Seed A Fertilizer
"""

import itertools
import sys
from typing import NamedTuple, Optional


class RangeMap(NamedTuple):
    destination_start: int
    source_start: int
    length: int

    @property
    def source_end(self) -> int:
        return self.source_start + self.length

class PuzzleInput(NamedTuple):
    seeds: list[int]
    maps: list[list[RangeMap]]

class SeedRange(NamedTuple):
    start: int
    length: int

def parse_input() -> PuzzleInput:
    with open('data/day05.txt', encoding='utf8') as f:
        data = f.read().split('\n\n')

    seeds_str = data.pop(0)
    seeds = [int(seed) for seed in seeds_str.removeprefix('seeds: ').split()]

    maps = []

    for chunk in data:
        lines = chunk.splitlines()[1:]

        maps.append(sorted(
            [RangeMap(*(int(x) for x in line.split())) for line in lines],
            key=lambda x: x[1],
        ))

    return PuzzleInput(seeds, maps)


def binary_search(range_maps: list[RangeMap], value: int) -> tuple[int, Optional[int]]:
    # Binary search isn't really needed in this case because the number of range maps is small,
    # but it should be more efficient for larger inputs.

    left, right = 0, len(range_maps) - 1

    while left <= right:
        middle = (left + right) // 2
        rm = range_maps[middle]

        if value < rm.source_start:
            right = middle - 1
        elif value < rm.source_end:
            return rm.destination_start + value - rm.source_start, middle + 1
        else:
            left = middle + 1

    return value, left

def part_1(data: PuzzleInput) -> int:
    min_location = sys.maxsize

    for seed in data.seeds:
        for range_maps in data.maps:
            seed, _ = binary_search(range_maps, seed)
        min_location = min(min_location, seed)

    return min_location

def part_2(data: PuzzleInput) -> int:
    it = iter(data.seeds)
    seed_ranges = []
    while args := list(itertools.islice(it, 2)):
        seed_ranges.append(SeedRange(*args))

    for range_maps in data.maps:
        new_ranges = []

        for sr in seed_ranges:
            start, length = sr

            # In hindsight, sorting the range maps was the correct choice
            dest, idx = binary_search(range_maps, start)
            identity_section = dest == start

            while length > 0:
                if identity_section:
                    dest = start

                    if idx >= len(range_maps):
                        max_length = length
                    else:
                        rm = range_maps[idx]
                        max_length = min(length, rm.source_start - start)

                        start = rm.source_start
                        identity_section = False
                else:
                    # Replacement section
                    curr_rm = range_maps[idx - 1]
                    offset = start - curr_rm.source_start
                    max_length = min(length, curr_rm.length - offset)

                    dest = curr_rm.destination_start + offset
                    start = curr_rm.source_end
                    identity_section = idx >= len(range_maps) or start != range_maps[idx].source_start

                new_ranges.append(SeedRange(dest, max_length))

                length -= max_length
                idx += 1

        seed_ranges = new_ranges

    return min(sr.start for sr in seed_ranges)


def main():
    data = parse_input()
    print(part_1(data))
    print(part_2(data))


if __name__ == '__main__':
    main()
