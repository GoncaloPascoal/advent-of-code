
"""
Day 4 - Scratchcards
"""

from typing import NamedTuple


class Scratchcard(NamedTuple):
    winning_nums: frozenset[int]
    my_nums: frozenset[int]

def parse_input() -> list[Scratchcard]:
    with open('data/day04.txt', encoding='utf8') as f:
        lines = [line.strip().split(':')[1] for line in f.readlines()]

    cards = []
    for line in lines:
        winning_str, my_str = line.split(' | ')
        card = Scratchcard(
            frozenset(int(x) for x in winning_str.split()),
            frozenset(int(x) for x in my_str.split()),
        )
        cards.append(card)

    return cards


def part_1(cards: list[Scratchcard]) -> int:
    return sum(
        2 ** (len(matching) - 1)
        for card in cards
        if (matching := card.winning_nums & card.my_nums)
    )

def part_2(cards: list[Scratchcard]) -> int:
    num_cards = len(cards)
    cards_won: dict[int, int] = {}

    for i, card in enumerate(cards):
        match_count = len(card.winning_nums & card.my_nums)
        start, end = min(i + 1, num_cards), min(i + 1 + match_count, num_cards)

        for j in range(start, end):
            cards_won.setdefault(j, 0)
            cards_won[j] += 1 + cards_won.get(i, 0)

    return num_cards + sum(cards_won.values())


def main():
    cards = parse_input()
    print(part_1(cards))
    print(part_2(cards))


if __name__ == '__main__':
    main()
