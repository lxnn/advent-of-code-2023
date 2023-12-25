import sys
import re


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Vector = complex
type Coord = Vector


def part1(raw: str):
    grid = parse(raw)
    (start,) = extract(grid, "S")
    return len(reachable(grid, start, steps=64))


def part2(raw: str):
    ...


def reachable(grid: dict[Coord, str], start: Coord, steps: int) -> set[Coord]:
    navigable = extract(grid, ".") | extract(grid, 'S')
    positions = {start}
    for step in range(64):
        positions = neighbors(positions) & navigable
    return positions


def distance(a: Coord, b: Coord, grid: dict[Coord, str]) -> int:
    navigable = extract(grid, ".") | extract(grid, "S")
    positions = {a}
    steps = 0
    while b not in positions:
        positions = neighbors(positions) & navigable
        steps += 1
    return steps


def dimensions(grid: dict[Coord, str]) -> tuple[int, int]:
    height = int(1 + max(coord.real for coord in grid))
    width = int(1 + max(coord.imag for coord in grid))
    return height, width


def corners(grid: dict[Coord, str]) -> list[Coord]:
    NW_corner = 0 + 0j
    SE_corner = max(grid, key=lambda coord: (coord.real, coord.imag))
    NE_corner = 0 + SE_corner.imag * 1j
    SW_corner = SE_corner.real + 0j
    return [NW_corner, SE_corner, NE_corner, SW_corner]


def parse(raw: str) -> dict[Coord, str]:
    return {
        r + c * 1j: char
        for r, line in enumerate(raw.strip().splitlines())
        for c, char in enumerate(line)
    }


def neighbors(coords: Coord | set[Coord]) -> set[Coord]:
    if isinstance(coords, set):
        return set.union(*map(neighbors, coords))
    else:
        return {coords + direction for direction in (+1, -1, +1j, -1j)}


def extract(grid: dict[Coord, str], target: str) -> set[Coord]:
    return {coord for coord, tile in grid.items() if tile == target}


if __name__ == "__main__":
    raise SystemExit(main())
