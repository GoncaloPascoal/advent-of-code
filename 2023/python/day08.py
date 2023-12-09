
"""
Day 8 - Haunted Wasteland
"""

import math
from typing import NamedTuple


class Instructions(NamedTuple):
    directions: str
    network: dict[str, tuple[str, str]]

def parse_input() -> Instructions:
    with open('data/day08.txt', encoding='utf8') as f:
        lines = f.read()

    directions, network_str = lines.split('\n\n')
    network = {}

    for line in network_str.splitlines():
        start, left, right = line[:3], line[7:10], line[12:15]
        network[start] = (left, right)

    return Instructions(directions, network)


def part_1(instructions: Instructions) -> int:
    node = 'AAA'
    steps = 0
    dir_idx = 0

    while node != 'ZZZ':
        direction = instructions.directions[dir_idx]
        node = instructions.network[node][0 if direction == 'L' else 1]

        steps += 1
        dir_idx = (dir_idx + 1) % len(instructions.directions)

    return steps

def part_2(instructions: Instructions) -> int:
    # This implementation can handle loops with offsets that cannot be solved purely with LCM.
    # TODO: investigate special cases when there are multiple "Z" nodes within a loop or where a single "Z"
    #  node is visited more than once.

    nodes = [node for node in instructions.network if node[-1] == 'A']

    steps_until_loop = []
    loop_lengths = []

    for node in nodes:
        steps = 0
        dir_idx = 0

        def next_node(node: str) -> str:
            nonlocal steps, dir_idx

            direction = instructions.directions[dir_idx]
            steps += 1
            dir_idx = (dir_idx + 1) % len(instructions.directions)

            return instructions.network[node][0 if direction == 'L' else 1]

        while node[-1] != 'Z':
            node = next_node(node)
        steps_until_loop.append(steps)

        steps = 0
        node = next_node(node)
        while node[-1] != 'Z':
            node = next_node(node)
        loop_lengths.append(steps)

    steps = max(steps_until_loop)
    positions = [steps % val for val in steps_until_loop]
    congruences = [(-pos % length, length) for pos, length in zip(positions, loop_lengths)]

    while len(congruences) > 1:
        b1, n1 = congruences.pop()
        b2, n2 = congruences.pop()

        i = 0
        while (val := b1 + i * n1) % n2 != b2:
            i += 1

        congruences.append((val, math.lcm(n1, n2)))

    return steps + congruences[0][0]


def main():
    instructions = parse_input()
    print(part_1(instructions))
    print(part_2(instructions))


if __name__ == '__main__':
    main()
