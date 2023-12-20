import sys
import re


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


def part1(raw: str):
    ...


def part2(raw: str):
    ...


def ints(string: str, *, negatives: bool = False) -> list[int]:
    if negatives:
        return list(map(int, re.findall(r"-?[0-9]+", string)))
    else:
        return list(map(int, re.findall(r"[0-9]+", string)))


if __name__ == "__main__":
    raise SystemExit(main())
