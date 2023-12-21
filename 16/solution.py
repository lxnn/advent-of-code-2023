import sys
import re
from collections.abc import Iterable
from enum import Enum


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Vector = complex
type Coord = Vector


class Dir(complex, Enum):
    N = -1 + 0j
    S = +1 + 0j
    W = 0 - 1j
    E = 0 + 1j


def part1(raw: str):
    grid = parse(raw)
    start_pos = 0 - 1j
    start_vel = 0 + 1j
    return len(energized(grid, start_pos, start_vel))


def part2(raw: str):
    grid = parse(raw)
    height = int(max(coord.real for coord in grid))
    width = int(max(coord.imag for coord in grid))
    west_edge = [row - 1j for row in range(height)]
    east_edge = [row + 1j for row in range(height)]
    north_edge = [-1 + col * 1j for col in range(width)]
    south_edge = [+1 + col * 1j for col in range(width)]
    return max(
        len(energized(grid, start_pos, start_vel))
        for edge, start_vel in (
            (west_edge, Dir.E),
            (east_edge, Dir.W),
            (north_edge, Dir.S),
            (south_edge, Dir.N),
        )
        for start_pos in edge
    )


def parse(raw: str) -> dict[Coord, str]:
    return {
        row + col * 1j: char
        for row, line in enumerate(raw.strip().splitlines())
        for col, char in enumerate(line)
    }


def energized(
    grid: dict[Coord, str], start_pos: Vector, start_vel: Vector
) -> set[Coord]:
    beams = {(start_pos, start_vel)}
    seen = set()
    while beams:
        seen |= beams
        beams = {
            (pos + vel, new_vel)
            for pos, vel in beams
            if pos + vel in grid
            for new_vel in deflect(vel, grid[pos + vel])
        } - seen
    return {pos for (pos, vel) in seen if pos in grid}


def deflect(vel: Vector, char: str) -> Iterable[Vector]:
    match [char, vel]:
        case ("/", (Dir.E | Dir.W)) | ("\\", (Dir.N | Dir.S)):
            yield vel * 1j
        case ("/", (Dir.N | Dir.S)) | ("\\", (Dir.E | Dir.W)):
            yield vel * -1j
        case ("|", (Dir.E | Dir.W)) | ("-", (Dir.N | Dir.S)):
            yield vel * 1j
            yield vel * -1j
        case (("." | "|" | "-"), _):
            yield vel
        case _:
            assert False


if __name__ == "__main__":
    raise SystemExit(main())
