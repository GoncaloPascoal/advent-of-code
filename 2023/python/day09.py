
"""
Day 9 - Mirage Maintenance
"""


def parse_input() -> list[list[int]]:
    with open('data/day09.txt', encoding='utf8') as f:
        return [[int(x) for x in line.strip().split()] for line in f.readlines()]


def calculate_differences(series: list[int]) -> list[list[int]]:
    differences = [series]
    while any(differences[-1]):
        differences.append([b - a for a, b in zip(differences[-1], differences[-1][1:])])
    return differences

def part_1(data: list[list[int]]) -> int:
    sum_extrapolated = 0

    for series in data:
        differences = calculate_differences(series)

        differences[-1].append(0)
        for prev_seq, seq in zip(differences[::-1], differences[-2::-1]):
            seq.append(seq[-1] + prev_seq[-1])

        sum_extrapolated += differences[0][-1]

    return sum_extrapolated

def part_2(data: list[list[int]]):
    sum_extrapolated = 0

    for series in data:
        differences = calculate_differences(series)

        # Doesn't matter where the zero is inserted (sequence is all zeros)
        differences[-1].append(0)
        for prev_seq, seq in zip(differences[::-1], differences[-2::-1]):
            seq.insert(0, seq[0] - prev_seq[0])

        sum_extrapolated += differences[0][0]

    return sum_extrapolated


def main():
    data = parse_input()
    print(part_1(data))
    print(part_2(data))


if __name__ == '__main__':
    main()
