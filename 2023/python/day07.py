
"""
Day 7 - Scratchcards
"""

import functools
from collections import Counter
from typing import Final, NamedTuple

SCORES: Final[dict[str, int]] = {
    rank: i for i, rank in enumerate(['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'])
}
SCORES_WILDCARDS: Final[dict[str, int]] = {
    rank: i for i, rank in enumerate(['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A'])
}

class Hand(NamedTuple):
    cards: str
    bid: int

def parse_input() -> list[Hand]:
    with open('data/day07.txt', encoding='utf8') as f:
        lines = f.readlines()

    hands = []
    for line in lines:
        hand, bid = line.strip().split()
        hands.append(Hand(hand, int(bid)))

    return hands


def compare(hand_1: Hand, hand_2: Hand, wildcards: bool = False) -> int:
    scores = SCORES_WILDCARDS if wildcards else SCORES

    counts_1 = Counter(hand_1.cards)
    counts_2 = Counter(hand_2.cards)

    if wildcards:
        apply_wildcards(counts_1)
        apply_wildcards(counts_2)

    most_common_1, most_common_2 = counts_1.most_common(), counts_2.most_common()

    if most_common_1[0][1] < most_common_2[0][1]:
        return -1
    if most_common_1[0][1] > most_common_2[0][1]:
        return 1

    # Handle Three of a Kind vs. Full House and Two Pair vs One Pair
    if len(most_common_1) > 1:
        if most_common_1[1][1] < most_common_2[1][1]:
            return -1
        if most_common_1[1][1] > most_common_2[1][1]:
            return 1

    # Hands are of the same type, compare card by card
    for card_1, card_2 in zip(hand_1.cards, hand_2.cards):
        score_1, score_2 = scores[card_1], scores[card_2]
        if score_1 < score_2:
            return -1
        if score_1 > score_2:
            return 1

    return 0

def apply_wildcards(counts: Counter):
    mc = counts.most_common()
    first_rank = mc[0]

    if first_rank[0] == 'J':
        if len(mc) > 1:
            second_rank = mc[1]
            counts[second_rank[0]] += counts.pop('J', 0)
    else:
        counts[first_rank[0]] += counts.pop('J', 0)

def total_winnings(hands: list[Hand], wildcards: bool = False) -> int:
    hands = sorted(hands, key=functools.cmp_to_key(functools.partial(compare, wildcards=wildcards)))  # type: ignore
    return sum((i + 1) * hand.bid for i, hand in enumerate(hands))

def part_1(hands: list[Hand]) -> int:
    return total_winnings(hands)

def part_2(hands: list[Hand]) -> int:
    return total_winnings(hands, wildcards=True)


def main():
    hands = parse_input()
    print(part_1(hands))
    print(part_2(hands))


if __name__ == '__main__':
    main()
