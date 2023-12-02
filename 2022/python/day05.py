
"""
Day 5 - Supply Stacks
"""

import copy
import re
from typing import TypeAlias

Stacks: TypeAlias = list[list[str]]
Instructions: TypeAlias = list[tuple[int, int, int]]

def parse_input() -> tuple[Stacks, Instructions]:
    with open('data/day05.txt', encoding='utf8') as f:
        data = f.read()

    stack_data, instruction_data = data.split('\n\n')

    stack_data = stack_data.strip().split('\n')[-2::-1]
    instruction_data = instruction_data.strip().split('\n')

    num_stacks = round(len(stack_data[0]) / 3)

    stacks = [[] for _ in range(num_stacks)]
    instructions = []

    for line in stack_data:
        for stack_idx, crate in enumerate(line[1::4]):
            if crate.strip():
                stacks[stack_idx].append(crate)

    instruction_regex = r'move (\d+) from (\d+) to (\d+)'

    for line in instruction_data:
        match = re.match(instruction_regex, line)
        instructions.append(tuple(int(x) for x in match.groups()))

    return stacks, instructions


def part_1(data: tuple[Stacks, Instructions]) -> str:
    stacks, instructions = data
    stacks = copy.deepcopy(stacks)

    for (amount, origin, dest) in instructions:
        # Convert to zero-indexing
        origin = origin - 1
        dest = dest - 1

        stacks[dest] += stacks[origin][:-amount - 1:-1]
        stacks[origin] = stacks[origin][:len(stacks[origin]) - amount]

    return ''.join(stack[-1] if stack else '' for stack in stacks)

def part_2(data: tuple[Stacks, Instructions]) -> str:
    stacks, instructions = data
    stacks = copy.deepcopy(stacks)

    for (amount, origin, dest) in instructions:
        # Convert to zero-indexing
        origin = origin - 1
        dest = dest - 1

        idx = len(stacks[origin]) - amount
        stacks[dest] += stacks[origin][idx:]
        stacks[origin] = stacks[origin][:idx]

    return ''.join(stack[-1] if stack else '' for stack in stacks)


def main():
    data = parse_input()
    print(part_1(data))
    print(part_2(data))


if __name__ == '__main__':
    main()
