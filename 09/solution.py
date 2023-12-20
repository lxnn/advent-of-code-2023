from __future__ import annotations
import sys
from itertools import pairwise
from collections.abc import Iterable
import re


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


def part1(raw: str):
    sequences = parse(raw)
    total = 0
    for sequence in sequences:
        extrapolated = extrapolate(sequence)
        total += extrapolated[-1]
    return total


def part2(raw: str):
    sequences = parse(raw)
    total = 0
    for sequence in sequences:
        hindcasted = extrapolate(sequence, backwards=True)
        total += hindcasted[0]
    return total


def parse(raw: str) -> list[tuple[int, ...]]:
    return [tuple(ints(line)) for line in raw.strip().splitlines()]


def ints(string: str) -> Iterable[int]:
    return map(int, re.findall(r"-?[0-9]+", string))


def extrapolate(sequence: Iterable[int], *, backwards: bool = False) -> tuple[int, ...]:
    if not isinstance(sequence, tuple):
        sequence = tuple(sequence)
    assert len(sequence) > 0
    if len(set(sequence)) == 1:
        return *sequence, sequence[-1]
    differences = tuple(b - a for (a, b) in pairwise(sequence))
    extrapolated_differences = extrapolate(differences, backwards=backwards)
    if backwards:
        return sequence[0] - extrapolated_differences[0], *sequence
    else:
        return *sequence, sequence[-1] + extrapolated_differences[-1]


if __name__ == "__main__":
    raise SystemExit(main())
