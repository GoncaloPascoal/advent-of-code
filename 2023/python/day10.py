
"""
Day 10 - Pipe Maze
"""

from typing import NamedTuple, Self
from queue import Queue


def parse_input() -> list[str]:
    with open('data/day10.txt', encoding='utf8') as f:
        return [line.strip() for line in f.readlines()]


class Position(NamedTuple):
    row: int
    col: int

    def north(self) -> Self:
        return Position(self.row - 1, self.col)

    def south(self) -> Self:
        return Position(self.row + 1, self.col)

    def west(self) -> Self:
        return Position(self.row, self.col - 1)

    def east(self) -> Self:
        return Position(self.row, self.col + 1)

def start_position(maze: list[str]) -> Position:
    for i, line in enumerate(maze):
        for j, character in enumerate(line):
            if character == 'S':
                return Position(i, j)

    raise RuntimeError('Could not find starting point')

def is_position_valid(maze: list[str], pos: Position) -> bool:
    return 0 <= pos.row < len(maze) and 0 <= pos.col < len(maze[0])

def get_neighbors(maze: list[str], pos: Position) -> set[Position]:
    match maze[pos.row][pos.col]:
        case 'S':
            neighbors = {pos.north(), pos.south(), pos.west(), pos.east()}
        case '|':
            neighbors = {pos.north(), pos.south()}
        case '-':
            neighbors = {pos.west(), pos.east()}
        case 'L':
            neighbors = {pos.north(), pos.east()}
        case 'J':
            neighbors = {pos.north(), pos.west()}
        case '7':
            neighbors = {pos.west(), pos.south()}
        case 'F':
            neighbors = {pos.east(), pos.south()}
        case _:
            neighbors = set()

    neighbors = {n for n in neighbors if is_position_valid(maze, n) and maze[n.row][n.col] != '.'}

    if maze[pos.row][pos.col] == 'S':
        neighbors = {n for n in neighbors if pos in get_neighbors(maze, n)}

    return neighbors

def part_1(maze: list[str]) -> int:
    start = start_position(maze)

    max_distance = 0
    distance_to_start = {start: 0}

    q = Queue()
    q.put(start)

    # Breadth-first search
    while not q.empty():
        node: Position = q.get()
        neighbors = get_neighbors(maze, node)

        for neighbor in neighbors:
            if neighbor not in distance_to_start:
                distance_to_start[neighbor] = distance_to_start[node] + 1
                q.put(neighbor)

                max_distance = max(max_distance, distance_to_start[neighbor])

    return max_distance

def part_2(maze: list[str]) -> int:
    start = start_position(maze)

    visited = {start}
    q = [start]

    # Depth-first search
    while q:
        node: Position = q.pop()
        neighbors = get_neighbors(maze, node)

        # TODO: replace this with something nicer
        if node == start:
            if neighbors == {node.north(), node.south()}:
                replacement = '|'
            elif neighbors == {node.west(), node.east()}:
                replacement = '-'
            elif neighbors == {node.north(), node.east()}:
                replacement = 'L'
            elif neighbors == {node.north(), node.west()}:
                replacement = 'J'
            elif neighbors == {node.west(), node.south()}:
                replacement = '7'
            elif neighbors == {node.east(), node.south()}:
                replacement = 'F'
            else:
                raise RuntimeError('Invalid start position')

            maze[node.row] = maze[node.row].replace('S', replacement)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)

    num_inside = 0
    toggle_corners = {'F': '7', 'L': 'J'}

    for i, line in enumerate(maze):
        inside = False
        last_corner = None

        for j, character in enumerate(line):
            node = Position(i, j)

            if node in visited:
                match character:
                    case '|':
                        inside = not inside
                    case 'F' | 'L':
                        inside = not inside
                        last_corner = character
                    case '7' | 'J':
                        if toggle_corners.get(last_corner) == character:
                            inside = not inside
                            last_corner = None
            elif inside:
                num_inside += 1

    return num_inside


def main():
    maze = parse_input()
    print(part_1(maze))
    print(part_2(maze))


if __name__ == '__main__':
    main()
