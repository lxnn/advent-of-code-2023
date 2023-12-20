from __future__ import annotations
import sys
from itertools import combinations, chain, islice
from collections import deque


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Vector = tuple[int, int]
type Cell = Vector
type Pipe = str


N = (-1, 0)
S = (+1, 0)
W = (0, -1)
E = (0, +1)


PIPES: dict[Pipe, set[Vector]] = {
    "|": {N, S},
    "-": {W, E},
    "L": {N, E},
    "J": {N, W},
    "7": {S, W},
    "F": {S, E},
    "S": {N, S, E, W},
    ".": set(),
}


def part1(raw: str):
    start, pipes = parse(raw)
    loop = get_loop(start, pipes)
    assert len(loop) % 2 == 0, "odd-length loops shouldn't be possible"
    return len(loop) // 2


def part2(raw: str):
    start, pipes = parse(raw)
    loop = get_loop(start, pipes)
    left_edge = set()
    right_edge = set()
    left_turns = 0
    for pred, cell, succ in sliding_window(chain(loop[-1:], loop, loop[:+1]), 3):
        entry_direction = sub(cell, pred)
        exit_direction = sub(succ, cell)
        left_edge |= {
            add(cell, rotate_90_ccw(entry_direction)),
            add(cell, rotate_90_ccw(exit_direction)),
        }
        right_edge |= {
            add(cell, rotate_90_cw(entry_direction)),
            add(cell, rotate_90_cw(exit_direction)),
        }
        if exit_direction == rotate_90_ccw(entry_direction):
            left_turns += 1
        if exit_direction == rotate_90_cw(entry_direction):
            left_turns -= 1
    assert left_turns in (-4, 4)
    if left_turns == 4:
        return len(flood_fill(left_edge, set(loop)))
    if left_turns == -4:
        return len(flood_fill(right_edge, set(loop)))


def parse(raw: str) -> tuple[Cell, dict[Cell, Pipe]]:
    pipes = {
        (r, c): char
        for r, line in enumerate(raw.strip().splitlines())
        for c, char in enumerate(line)
    }
    (start,) = (cell for cell, pipe in pipes.items() if pipe == "S")
    return start, pipes


def get_loop(start: Cell, pipes: dict[Cell, Pipe]) -> tuple[Cell, ...]:
    paths = [[start, neighbour] for neighbour in connections(start, pipes)]
    assert paths
    while paths:
        for path_a, path_b in combinations(paths, 2):
            assert len(path_a) == len(path_b)
            if path_a[-1] == path_b[-1]:
                return *path_a, *reversed(path_b[1:-1])
            if path_a[-1] in connections(path_b[-1], pipes):
                return *path_a, *reversed(path_b[1:])
        remaining_paths = []
        for path in paths:
            extensions = connections(path[-1], pipes) - {path[-2]}
            if not extensions:
                continue
            assert len(extensions) == 1
            (extension,) = extensions
            remaining_paths.append(path + [extension])
        paths = remaining_paths
    assert False, "no loop found"


def add(u: Vector, v: Vector) -> Vector:
    return (u[0] + v[0], u[1] + v[1])


def sub(u: Vector, v: Vector) -> Vector:
    return (u[0] - v[0], u[1] - v[1])


def neighbours(cell: Cell | set[Cell]) -> set[Cell]:
    if isinstance(cell, set):
        return set.union(*map(neighbours, cell))
    return {add(cell, direction) for direction in (N, E, S, W)}


def pipe_ends(cell: Cell, pipe: Pipe) -> set[Cell]:
    return {add(cell, direction) for direction in PIPES[pipe]}


def connections(cell: Cell, pipes: dict[Cell, Pipe]) -> set[Cell]:
    return {
        end
        for end in pipe_ends(cell, pipes[cell])
        if end in pipes
        if cell in pipe_ends(end, pipes[end])
    }


def rotate_90_cw(vector: Vector) -> Vector:
    a, b = vector
    return (b, -a)


def rotate_90_ccw(vector: Vector) -> Vector:
    a, b = vector
    return (-b, a)


def flood_fill(sources: set[Cell], walls: set[Cell]) -> set[Cell]:
    filled = set()
    frontier = sources - walls
    while frontier:
        filled |= frontier
        frontier = neighbours(frontier) - walls - filled
    return filled


def sliding_window(iterable, n):
    it = iter(iterable)
    window = deque(islice(it, n - 1), maxlen=n)
    for x in it:
        window.append(x)
        yield tuple(window)


if __name__ == "__main__":
    raise SystemExit(main())
