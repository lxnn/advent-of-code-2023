import sys
import re
import bisect
import math
from itertools import batched


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


def part1(raw: str):
    seeds, mappings = parse(raw)
    values = seeds
    for mapping in mappings:
        values = [apply(mapping, value) for value in values]
    return min(values)


def part2(raw: str):
    seeds, mappings = parse(raw)
    ranges = [(start, start + length) for (start, length) in batched(seeds, 2)]
    for mapping in mappings:
        ranges = sort_and_coalesce(apply_to_ranges(mapping, ranges))
    return min(ranges)[0]


type Mapping = tuple[list[int], list[int]]
type Range = tuple[int, int]


def apply(m: Mapping, x: int) -> int:
    old, new = m
    idx = bisect.bisect(old, x) - 1
    return new[idx] + x - old[idx]


def apply_to_ranges(m: Mapping, ranges: list[Range]) -> list[Range]:
    old, new = m
    result = []
    for start, stop in ranges:
        start_idx = bisect.bisect_right(old, start) - 1
        stop_idx = bisect.bisect_left(old, stop)
        for idx in range(start_idx, stop_idx):
            dest = new[idx] + start - old[idx]
            bound = old[idx + 1] if idx + 1 < len(old) else math.inf
            length = min(stop, bound) - start
            result.append((dest, dest + length))
            start += length
    for start, stop in result:
        assert start < stop
    return result


def sort_and_coalesce(ranges: list[Range]) -> list[Range]:
    result = []
    if not ranges:
        return result
    range_iter = iter(sorted(ranges))
    curr_start, curr_stop = next(range_iter)
    for start, stop in range_iter:
        if start > curr_stop:
            result.append((curr_start, curr_stop))
            curr_start, curr_stop = start, stop
        else:
            curr_stop = stop
    result.append((curr_start, curr_stop))
    return result


def parse(raw: str) -> tuple[list[int], list[Mapping]]:
    paras = raw.strip().split("\n\n")
    first, *rest = paras
    seeds = list(ints(first))
    mappings = [parse_mapping(para) for para in rest]
    return seeds, mappings


def parse_mapping(raw: str) -> Mapping:
    """
    >>> s = '''
    ... 0 15 37
    ... 37 52 2
    ... 39 0 15
    ... '''
    >>> parse_mapping(s)
    ([-1, 0, 15, 52, 54], [-1, 39, 0, 37, 54])
    """
    old = [-1]
    new = [-1]
    ranges = [ints(line) for line in raw.strip().splitlines()]
    ranges = list(filter(None, ranges))
    ranges.sort(key=lambda r: r[1])
    for dest, source, length in ranges:
        source_end = source + length
        assert old[-1] <= source
        if old[-1] == source:
            old.pop()
            new.pop()
        old.append(source)
        old.append(source_end)
        new.append(dest)
        new.append(source_end)
    return (old, new)


def ints(string: str) -> list[int]:
    return list(map(int, re.findall(r"\d+", string)))


if __name__ == "__main__":
    raise SystemExit(main())
