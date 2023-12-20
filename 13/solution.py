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
    for pattern in parse(raw):
        for col in vertical_lines_of_reflection(pattern):
            total += col
        for row in horizontal_lines_of_reflection(pattern):
            total += row * 100
    return total


def part2(raw: str):
    total = 0
    for pattern in parse(raw):
        for col in vertical_lines_of_reflection(pattern, fix_smudge=True):
            total += col
        for row in horizontal_lines_of_reflection(pattern, fix_smudge=True):
            total += row * 100
    return total


def parse(raw: str):
    for para in raw.strip().split("\n\n"):
        yield para.splitlines()


def horizontal_lines_of_reflection(
    pattern: list[str], *, fix_smudge: bool = False
) -> list[int]:
    pre_smudge = []
    post_smudge = []
    for i, line in enumerate(pattern):
        if i > 0:
            pre_smudge.append(i)
        new_pre_smudge = []
        new_post_smudge = []
        for j in pre_smudge:
            if j <= 0 or pattern[j - 1] == line:
                new_pre_smudge.append(j - 1)
            elif almost_equal(pattern[j - 1], line):
                new_post_smudge.append(j - 1)
        for j in post_smudge:
            if j <= 0 or pattern[j - 1] == line:
                new_post_smudge.append(j - 1)
        pre_smudge = new_pre_smudge
        post_smudge = new_post_smudge
    if fix_smudge:
        return [(len(pattern) + j) // 2 for j in post_smudge]
    else:
        return [(len(pattern) + j) // 2 for j in pre_smudge]


def vertical_lines_of_reflection(
    pattern: list[str], *, fix_smudge: bool = False
) -> list[int]:
    return horizontal_lines_of_reflection(transpose(pattern), fix_smudge=fix_smudge)


def almost_equal(s1: str, s2: str) -> bool:
    return sum(c1 != c2 for c1, c2 in zip(s1, s2, strict=True)) <= 1


def transpose(pattern: list[str]) -> list[str]:
    return ["".join(column) for column in zip(*pattern)]


def ints(string: str, *, negatives: bool = False) -> list[int]:
    if negatives:
        return list(map(int, re.findall(r"-?[0-9]+", string)))
    else:
        return list(map(int, re.findall(r"[0-9]+", string)))


if __name__ == "__main__":
    raise SystemExit(main())
