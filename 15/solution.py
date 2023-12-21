import sys
import re


assert sys.version_info >= (3, 7)


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


def part1(raw: str):
    parts = raw.strip().split(",")
    return sum(map(hash_, parts))


def hash_(string: str) -> int:
    current = 0
    for char in string:
        current += ord(char)
        current *= 17
        current %= 256
    return current


def part2(raw: str):
    instructions = raw.strip().split(",")
    boxes = [{} for boxnum in range(256)]
    for instruction in instructions:
        match = re.match(r"([a-z]+)([=-])([0-9]*)", instruction)
        assert match
        match match.groups():
            case (label, "=", focal_length):
                box = boxes[hash_(label)]
                box[label] = focal_length
            case (label, "-", ""):
                box = boxes[hash_(label)]
                if label in box:
                    del box[label]
            case _:
                assert False
    return sum(
        (boxnum + 1) * (lensnum + 1) * int(focal_length)
        for boxnum, box in enumerate(boxes)
        for lensnum, (label, focal_length) in enumerate(box.items())
    )


if __name__ == "__main__":
    raise SystemExit(main())
