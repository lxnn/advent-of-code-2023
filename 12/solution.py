from __future__ import annotations
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import combinations
from collections import Counter
import re


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


def part1(raw: str):
    records = list(parse(raw))
    total = 0
    for string, blocks in records:
        total += count_arrangements(string, blocks)
    return total


def part2(raw: str):
    records = [("?".join([string] * 5), blocks * 5) for string, blocks in parse(raw)]
    total = 0
    for string, blocks in records:
        total += count_arrangements(string, blocks)
    return total


def parse(raw: str):
    for line in raw.strip().splitlines():
        prefix, suffix = line.split()
        yield prefix, ints(suffix)


def count_arrangements(string: str, blocks: Iterable[int]) -> int:
    PATTERN = re.compile(r"[?#]+")
    counts = Counter({0: 1})
    for block in blocks:
        new_counts = Counter()
        for index, count in counts.items():
            for match in PATTERN.finditer(string, index):
                slack = len(match[0]) - block
                starting_positions = range(match.start(), match.start() + slack + 1)
                for start in starting_positions:
                    if "#" in string[match.start() : start]:
                        break
                    if start + block < len(string) and string[start + block] == "#":
                        continue
                    new_counts[start + block + 1] += count
                if "#" in match[0]:
                    break
        counts = new_counts
    return sum(count for index, count in counts.items() if "#" not in string[index:])


def ints(string: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"[0-9]+", string)))


if __name__ == "__main__":
    raise SystemExit(main())
