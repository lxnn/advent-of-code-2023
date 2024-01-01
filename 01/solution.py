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
    total = 0
    for line in raw.splitlines():
        digits = re.findall(r"\d", line)
        total += int(digits[0] + digits[-1])
    return total


def part2(raw: str):
    digit_names = "zero one two three four five six seven eight nine".split()
    digits = {
        **{name: value for value, name in enumerate(digit_names)},
        **{str(value): value for value in range(10)},
    }
    total = 0
    for line in raw.splitlines():
        first_occurrence = [
            (line.index(digit), digit) for digit in digits if digit in line
        ]
        last_occurrence = [
            (line.rindex(digit), digit) for digit in digits if digit in line
        ]
        _, left = min(first_occurrence)
        _, right = max(last_occurrence)
        total += 10 * digits[left] + digits[right]
    return total


if __name__ == "__main__":
    raise SystemExit(main())
