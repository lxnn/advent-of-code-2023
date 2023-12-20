from __future__ import annotations
import sys
from dataclasses import dataclass, replace
from itertools import count


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Vector = tuple[int, int]
type Coord = Vector
type RockKind = str


N = (-1, 0)
S = (+1, 0)
W = (0, -1)
E = (0, +1)


def part1(raw: str):
    rocks = Rocks.parse(raw)
    shifted = rocks.shift(N)
    return shifted.load()


def part2(raw: str):
    rocks = Rocks.parse(raw)
    seen = {}
    history = []
    final_state = None
    for cycle in count(0):
        if rocks in seen:
            loop_start = seen[rocks]
            loop_length = cycle - loop_start
            final_state = history[
                loop_start + (1_000_000_000 - loop_start) % loop_length
            ]
            break
        seen[rocks] = cycle
        history.append(rocks)
        for direction in (N, W, S, E):
            rocks = rocks.shift(direction)
    assert final_state is not None
    return final_state.load()


@dataclass(frozen=True)
class Rocks:
    height: int
    width: int
    rounded: frozenset[Coord]
    square: frozenset[Coord]

    @classmethod
    def parse(cls, raw: str) -> Rocks:
        lines = raw.strip().splitlines()
        return Rocks(
            height=len(lines),
            width=len(lines[0]),
            rounded=frozenset(
                {
                    (row, col)
                    for row, line in enumerate(lines)
                    for col, char in enumerate(line)
                    if char == "O"
                }
            ),
            square=frozenset(
                {
                    (row, col)
                    for row, line in enumerate(lines)
                    for col, char in enumerate(line)
                    if char == "#"
                }
            ),
        )

    def shift(self, direction: Vector):
        if direction not in (N, S, E, W):
            raise ValueError()
        key = {
            N: lambda rock: +rock[0],
            S: lambda rock: -rock[0],
            W: lambda rock: +rock[1],
            E: lambda rock: -rock[1],
        }[direction]
        new_locations = set()
        for rock in sorted(self.rounded, key=key):
            while True:
                shifted = add(rock, direction)
                if (
                    shifted in new_locations
                    or shifted in self.square
                    or not self.in_bounds(shifted)
                ):
                    break
                rock = shifted
            new_locations.add(rock)
        return replace(self, rounded=frozenset(new_locations))

    def in_bounds(self, coord: Coord) -> bool:
        row, col = coord
        return 0 <= row < self.height and 0 <= col < self.width

    def load(self) -> int:
        return sum(self.height - row for (row, col) in self.rounded)

    def char(self, coord: Coord) -> str:
        if coord in self.rounded:
            return "O"
        elif coord in self.square:
            return "#"
        else:
            return "."

    def __str__(self) -> str:
        return "\n".join(
            "".join(self.char((row, col)) for col in range(self.width))
            for row in range(self.height)
        )


def add(u: Vector, v: Vector) -> Vector:
    return (u[0] + v[0], u[1] + v[1])


if __name__ == "__main__":
    raise SystemExit(main())
