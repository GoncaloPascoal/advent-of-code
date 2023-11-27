
"""
Day 2 - Rock Paper Scissors
"""

from enum import Enum
from typing import Self, TypeAlias


class Move(Enum):
    ROCK = {'score': 1}
    PAPER = {'score': 2}
    SCISSORS = {'score': 3}

    @property
    def score(self) -> int:
        return self.value['score']

    @property
    def beats(self) -> Self:
        return self.value['beats']

    @property
    def beat_by(self) -> Self:
        return self.value['beat_by']

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}.{self.name}'

Move.ROCK.value['beats'] = Move.SCISSORS
Move.PAPER.value['beats'] = Move.ROCK
Move.SCISSORS.value['beats'] = Move.PAPER

for move in Move:
    move.value['beats'].value['beat_by'] = move


SCORE_LOSS = 0
SCORE_DRAW = 3
SCORE_WIN = 6

StrategyGuide: TypeAlias = list[tuple[Move, str]]


def parse_input() -> StrategyGuide:
    with open('data/day02.txt', encoding='utf8') as f:
        data = f.readlines()

    guide_map = {
        'A': Move.ROCK,
        'B': Move.PAPER,
        'C': Move.SCISSORS,
    }

    guide = []
    for line in data:
        move_opp, code = line.strip().split()
        guide.append((guide_map[move_opp], code))

    return guide


def calc_score(move_opp: Move, move_self: Move) -> int:
    score = move_self.score

    if move_opp is move_self:
        score += SCORE_DRAW
    elif move_opp.beats is move_self:
        score += SCORE_LOSS
    else:
        score += SCORE_WIN

    return score


def part_1(guide: StrategyGuide) -> int:
    move_map = {'X': Move.ROCK, 'Y': Move.PAPER, 'Z': Move.SCISSORS}
    return sum(calc_score(move_opp, move_map[code]) for (move_opp, code) in guide)

def part_2(guide: StrategyGuide) -> int:
    total_score = 0

    for (move_opp, code) in guide:
        if code == 'X':
            # Lose
            move_self = move_opp.beats
        elif code == 'Y':
            # Draw
            move_self = move_opp
        else:
            # Win
            move_self = move_opp.beat_by

        total_score += calc_score(move_opp, move_self)

    return total_score


def main():
    guide = parse_input()
    print(part_1(guide))
    print(part_2(guide))


if __name__ == '__main__':
    main()
