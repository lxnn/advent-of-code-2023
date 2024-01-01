import sys
import re
from collections import Counter
from collections.abc import Iterable


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Card = tuple[list[int], list[int]]


def part1(raw: str):
    total = 0
    for need, have in parse(raw):
        matching = (Counter(need) & Counter(have)).total()
        if matching:
            total += 1 << (matching - 1)
    return total


def part2(raw: str):
    copies = Counter()
    for card_id, card in enumerate(parse(raw)):
        copies[card_id] += 1
        need, have = card
        matching = (Counter(need) & Counter(have)).total()
        for offset in range(matching):
            copies[card_id + offset + 1] += copies[card_id]
    return copies.total()


def parse(raw: str) -> Iterable[Card]:
    for line in raw.strip().splitlines():
        _, card = line.split(":")
        left, right = card.split("|")
        yield ints(left), ints(right)


def ints(string: str) -> list[int]:
    return list(map(int, re.findall(r"\d+", string)))


if __name__ == "__main__":
    raise SystemExit(main())
