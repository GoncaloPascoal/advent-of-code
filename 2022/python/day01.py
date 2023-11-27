
"""
Day 1 - Calorie Counting
"""

def parse_input() -> list[list[int]]:
    with open('data/day01.txt', encoding='utf8') as f:
        data = str(f.read())

    return [
        [int(meal) for meal in elf.split()]
        for elf in data.split('\n\n')
    ]


def part_1(elves: list[list[int]]) -> int:
    return sum(max(elves, key=sum))

def part_2(elves: list[list[int]]) -> int:
    total_calories = sorted((sum(elf) for elf in elves), reverse=True)
    return sum(total_calories[:3])


def main():
    elves = parse_input()

    print(part_1(elves))
    print(part_2(elves))


if __name__ == '__main__':
    main()
