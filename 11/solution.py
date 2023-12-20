import sys
from bisect import bisect
from itertools import combinations


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Vector = tuple[int, int]
type Galaxy = Vector


def part1(raw: str):
    galaxies = parse(raw)
    return sum(mhat_dist(g1, g2) for g1, g2 in combinations(expand(galaxies, 2), 2))


def part2(raw: str):
    galaxies = parse(raw)
    return sum(
        mhat_dist(g1, g2) for g1, g2 in combinations(expand(galaxies, 10**6), 2)
    )


def parse(raw: str) -> set[Galaxy]:
    return {
        (r, c)
        for r, line in enumerate(raw.strip().splitlines())
        for c, char in enumerate(line)
        if char == "#"
    }


def expand(galaxies: set[Galaxy], factor: int = 2) -> set[Galaxy]:
    rows, cols = zip(*galaxies)
    height, width = max(rows), max(cols)
    empty_rows = sorted(set(range(height)) - set(rows))
    empty_cols = sorted(set(range(width)) - set(cols))
    return {
        (
            row + (factor - 1) * bisect(empty_rows, row),
            col + (factor - 1) * bisect(empty_cols, col),
        )
        for (row, col) in galaxies
    }


def mhat_dist(u: Vector, v: Vector) -> int:
    return abs(u[0] - v[0]) + abs(u[1] - v[1])


if __name__ == "__main__":
    raise SystemExit(main())
