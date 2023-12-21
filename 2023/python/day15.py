
"""
Day 15 - Lens Library
"""

from collections import OrderedDict


def parse_input() -> str:
    with open('data/day15.txt', encoding='utf8') as f:
        return f.read().strip()


def hash_algorithm(s: str) -> int:
    val = 0
    for c in s:
        val = ((val + ord(c)) * 17) % 256
    return val

def part_1(sequence: str) -> int:
    return sum(hash_algorithm(s) for s in sequence.split(','))

def part_2(sequence: str) -> int:
    boxes = [OrderedDict() for _ in range(256)]

    for step in sequence.split(','):
        if step[-1].isdigit():
            # Add or replace lens
            focal_length = int(step[-1])
            label = step[:-2]
            box = boxes[hash_algorithm(label)]
            box[label] = focal_length
        else:
            # Remove lens
            label = step[:-1]
            box = boxes[hash_algorithm(label)]
            box.pop(label, None)

    total_power = 0
    for box_idx, box in enumerate(boxes):
        for lens_idx, focal_length in enumerate(box.values()):
            total_power += (box_idx + 1) * (lens_idx + 1) * focal_length

    return total_power


def main():
    sequence = parse_input()
    print(part_1(sequence))
    print(part_2(sequence))


if __name__ == '__main__':
    main()
