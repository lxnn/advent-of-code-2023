import sys
import math
from collections import Counter


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


def part1(raw: str):
    MAX = Counter(red=12, green=13, blue=14)
    total = 0
    for game_id, draws in parse(raw):
        if all(draw <= MAX for draw in draws):
            total += game_id
    return total


def part2(raw: str):
    total = 0
    for game_id, draws in parse(raw):
        first, *rest = draws
        min_cubes = first
        for draw in rest:
            min_cubes |= draw
        power = math.prod(min_cubes.values())
        total += power
    return total


def parse(raw: str):
    for line in raw.strip().splitlines():
        left, right = line.split(":")
        game_id = int(left.split()[1])
        raw_draws = right.split(";")
        draws = []
        for raw_draw in raw_draws:
            draw = {}
            for part in raw_draw.split(","):
                quantity, colour = part.split()
                draw[colour] = int(quantity)
            draws.append(Counter(draw))
        yield game_id, draws


if __name__ == "__main__":
    raise SystemExit(main())
