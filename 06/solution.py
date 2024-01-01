import sys
import re
import math


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


def part1(raw: str):
    races = parse(raw)
    product = 1
    for time, distance in races:
        min_time, max_time = max_and_min_time(time, distance)
        product *= max_time - min_time + 1
    return product


def part2(raw: str):
    [(time, distance)] = parse(raw.replace(" ", ""))
    min_time, max_time = max_and_min_time(time, distance)
    return max_time - min_time + 1


def max_and_min_time(time, distance):
    assert time**2 >= 4 * distance
    x = time / 2
    y = (time**2 - 4 * distance) ** 0.5 / 2
    return math.ceil(x - y), math.floor(x + y)


def ints(string: str) -> list[int]:
    return list(map(int, re.findall(r"\d+", string)))


def parse(raw: str) -> list[tuple[int, int]]:
    times, distances = raw.strip().splitlines()
    return list(zip(ints(times), ints(distances)))


if __name__ == "__main__":
    raise SystemExit(main())
