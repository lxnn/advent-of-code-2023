from collections.abc import Iterable
from itertools import tee, islice, chain, pairwise
import re
import sys

Vector = complex


class Point(Vector):
    pass


Triangle = tuple[Point, Point, Point]


R, D, L, U = +1, -1j, -1, +1j


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


def part1(raw: str):
    instructions = list(parse(raw))
    return find_area(draw_outline(instructions))


def part2(raw: str):
    instructions = list(parse(raw, part2=True))
    return find_area(draw_outline(instructions))


def parse(raw: str, *, part2=False) -> Iterable[Vector]:
    for line in raw.strip().splitlines():
        match = re.match(r"([RLUD]) ([0-9]+) [(]#([0-9a-f]{5})([0-3])[)]", line)
        assert match
        if part2:
            direction = {"0": R, "1": D, "2": L, "3": U}[match[4]]
            distance = int(match[3], 16)
        else:
            direction = {"R": R, "D": D, "L": L, "U": U}[match[1]]
            distance = int(match[2])
        yield distance * direction


def find_area(polygon: list[Point]) -> float:
    return sum(triangle_area(triangle) for triangle in triangulate(polygon))


def triangle_area(triangle: tuple[Point, Point, Point]) -> float:
    a, b, c = triangle
    return cross(b - a, c - b) / 2


def draw_outline(instructions: list[Vector]) -> list[Point]:
    left_turns = sum(
        +1 if is_left_turn(a, b) else -1
        for (a, b) in pairwise(chain(instructions, instructions[:1]))
    )
    assert left_turns in (-4, 4), left_turns
    if left_turns == -4:
        instructions = [-instruction for instruction in reversed(instructions)]
    polygon = []
    position = 0 + 0j
    for before, after in pairwise(chain(instructions[-1:], instructions)):
        match (before / abs(before), after / abs(after)):
            case (-1j, 1) | (1, -1j):
                polygon.append(position)
            case (1, 1j) | (1j, 1):
                polygon.append(position + 1 + 0j)
            case (1j, -1) | (-1, 1j):
                polygon.append(position + 1 + 1j)
            case (-1, -1j) | (-1j, -1):
                polygon.append(position + 0 + 1j)
            case other:
                assert False, other
        position += after
    return polygon


def dot(u: Vector, v: Vector) -> float:
    return (u.conjugate() * v).real


def cross(u: Vector, v: Vector) -> float:
    return (u.conjugate() * v).imag


def is_left_turn(u: Vector, v: Vector) -> bool:
    return cross(u, v) > 0


def triangle_contains(triangle: tuple[Point, Point, Point], point: Point) -> bool:
    return all(
        cross(b - a, point - a) >= 0 for (a, b) in pairwise(triangle + triangle[:1])
    )


def triangulate(polygon: Iterable[Point]) -> Iterable[Triangle]:
    polygon = list(polygon)

    def is_tip(point: Point) -> bool:
        triangle = before, point, after = get_corner(point)
        return is_left_turn(point - before, after - point) and not any(
            triangle_contains(triangle, other)
            for other in polygon
            if other not in triangle
        )

    def get_corner(point: Point) -> tuple[Point, Point, Point]:
        return next(corner for corner in corners(polygon) if corner[1] == point)

    tips = {point for point in polygon if is_tip(point)}

    while len(polygon) >= 3:
        point = tips.pop()
        corner = (a, b, c) = get_corner(point)
        yield corner
        polygon.remove(point)
        for neighbour in (a, c):
            if is_tip(neighbour):
                tips.add(neighbour)
            else:
                tips.discard(neighbour)


def corners(polygon: list[Point]) -> Iterable[tuple[Point, Point, Point]]:
    return triplewise(chain(polygon, polygon[:2]))


def triplewise[T](iterable: Iterable[T]) -> Iterable[tuple[T, T, T]]:
    it0, it1, it2 = tee(iterable, 3)
    return zip(it0, islice(it1, 1, None), islice(it2, 2, None))


if __name__ == "__main__":
    raise SystemExit(main())
