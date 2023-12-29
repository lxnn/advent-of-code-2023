import sys
import z3
from itertools import combinations


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Vec2D = tuple[float, float]
type Mat2D = tuple[Vec2D, Vec2D]

TA_MIN = 200_000_000_000_000
TA_MAX = 400_000_000_000_000


def part1(raw: str):
    hailstones = [((px, py), (vx, vy)) for (px, py, _), (vx, vy, _) in parse(raw)]
    total = 0
    for (p1, v1), (p2, v2) in combinations(hailstones, 2):
        solution = solve_2D(p1, v1, p2, v2)
        if solution and in_test_area(solution):
            total += 1
    return total


def part2(raw: str):
    hailstones = parse(raw)
    solver = z3.Solver()
    P = PX, PY, PZ = z3.Ints("PX PY PZ")
    V = VX, VY, VZ = z3.Ints("VX VY VZ")
    for i, (p, v) in enumerate(hailstones):
        T_i = z3.Int(f"T_{i}")
        solver.add(T_i >= 0)
        for p_j, v_j, P_j, V_j in zip(p, v, P, V):
            solver.add(P_j + T_i * V_j == p_j + T_i * v_j)
    satisfied = solver.check()
    assert satisfied
    model = solver.model()
    p = model[PX], model[PY], model[PZ]
    v = model[VX], model[VY], model[VZ]
    print(f"{p = }, {v = }")
    return sum(ir.as_long() for ir in p)


def in_test_area(v: Vec2D) -> bool:
    x, y = v
    return (TA_MIN <= x <= TA_MAX) and (TA_MIN <= y <= TA_MAX)


def parse(raw: str):
    for line in raw.strip().splitlines():
        lhs, rhs = line.split("@")
        position = tuple(int(num) for num in lhs.split(","))
        velocity = tuple(int(num) for num in rhs.split(","))
        yield position, velocity


def solve_2D(p1: Vec2D, v1: Vec2D, p2: Vec2D, v2: Vec2D) -> Vec2D | None:
    A = (v1, v2)
    A_inv = invert_2D(A)
    if A_inv is not None:
        b = sub_2D(p2, p1)
        t1 = b[0] * A_inv[0][0] + b[1] * A_inv[1][0]
        t2 = -(b[0] * A_inv[0][1] + b[1] * A_inv[1][1])
        if t1 > 0 and t2 > 0:
            return add_2D(p1, mul_2D(t1, v1))


def invert_2D(matrix: Mat2D) -> Mat2D | None:
    ((a, b), (c, d)) = matrix
    det = a * d - b * c
    if det != 0:
        return ((d / det, -b / det), (-c / det, a / det))


def mul_2D(s: float, v: Vec2D) -> Vec2D:
    return (s * v[0], s * v[1])


def sub_2D(u: Vec2D, v: Vec2D) -> Vec2D:
    return (u[0] - v[0], u[1] - v[1])


def add_2D(u: Vec2D, v: Vec2D) -> Vec2D:
    return (u[0] + v[0], u[1] + v[1])


if __name__ == "__main__":
    raise SystemExit(main())
