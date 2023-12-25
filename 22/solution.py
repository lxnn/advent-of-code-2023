import sys
import re
from collections.abc import Iterable
from collections import defaultdict, deque


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Vector = tuple[int, int, int]
type Voxel = Vector
type Brick = tuple[Voxel, Voxel]


def part1(raw: str):
    bricks = resting_state(parse(raw))
    supporting = support_structure(bricks)
    resting_on = invert_graph(supporting)
    extra_supported = {brick for brick in bricks if len(resting_on[brick]) > 1}
    safe = {brick for brick in bricks if supporting[brick] <= extra_supported}
    return len(safe)


def part2(raw: str):
    bricks = resting_state(parse(raw))
    supporting = support_structure(bricks)
    resting_on = invert_graph(supporting)
    total = 0
    for initial_brick in bricks:
        queue = deque([initial_brick])
        removed = set()
        while queue:
            brick = queue.popleft()
            removed.add(brick)
            queue.extend(
                other for other in supporting[brick] if resting_on[other] <= removed
            )
        total += len(removed) - 1
    return total


def parse(raw: str) -> Iterable[Brick]:
    for line in raw.strip().splitlines():
        lhs, rhs = line.split("~")
        start = tuple(int(number) for number in lhs.split(","))
        end = tuple(int(number) for number in rhs.split(","))
        assert sum(a != b for a, b in zip(start, end)) <= 1
        assert len(start) == 3
        assert len(end) == 3
        yield start, end


def voxels(brick: Brick) -> set[Voxel]:
    start, end = brick
    match (start, end):
        case ((x0, y0, z0), (x1, y1, z1)) if x0 == x1 and y0 == y1:
            return {(x0, y0, z) for z in range(z0, z1 + 1)}
        case ((x0, y0, z0), (x1, y1, z1)) if x0 == x1 and z0 == z1:
            return {(x0, y, z0) for y in range(y0, y1 + 1)}
        case ((x0, y0, z0), (x1, y1, z1)) if y0 == y1 and z0 == z1:
            return {(x, y0, z0) for x in range(x0, x1 + 1)}
        case _:
            raise ValueError("start aligned with axis")


def resting_state(bricks: Iterable[Brick]) -> set[Brick]:
    bricks_ascending = sorted(bricks, key=base)
    new_state = set()
    height = defaultdict(lambda: 0)
    for brick in bricks_ascending:
        new_base = 1 + max(height[x, y] for (x, y, z) in voxels(brick))
        offset = (0, 0, new_base - base(brick))
        moved = move(brick, offset)
        for x, y, z in voxels(moved):
            height[x, y] = max(height[x, y], z)
        new_state.add(moved)
    return new_state


def base(brick: Brick) -> int:
    return min(z for (x, y, z) in brick)


def move(brick: Brick, offset: Vector) -> Brick:
    start, end = brick
    return add(start, offset), add(end, offset)


def add(u: Vector, v: Vector) -> Vector:
    x0, y0, z0 = u
    x1, y1, z1 = v
    return (x0 + x1, y0 + y1, z0 + z1)


def support_structure(bricks: set[Brick]) -> dict[Brick, set[Brick]]:
    voxel_to_brick = {voxel: brick for brick in bricks for voxel in voxels(brick)}
    return {
        brick: {
            voxel_to_brick[above]
            for voxel in voxels(brick)
            if (above := add(voxel, (0, 0, 1))) in voxel_to_brick
        }
        - {brick}
        for brick in bricks
    }


def invert_graph[N](graph: dict[N, set[N]]) -> dict[N, set[N]]:
    inverted = defaultdict(set)
    for x, ys in graph.items():
        for y in ys:
            inverted[y].add(x)
    return inverted


def visualize(bricks: set[Brick]) -> str:
    all_voxels = set.union(*map(voxels, bricks))
    xs, ys, zs = zip(*all_voxels)
    xrange = range(min(xs), max(xs) + 1)
    zrange = range(min(zs), max(zs) + 1)
    yrange = range(min(ys), max(ys) + 1)
    return f"""
    {'x':^{len(xrange)}}
    {
        '\n    '.join(
                ''.join(
                    '.#'[any((x, y, z) in all_voxels for y in yrange)]
                    for x in xrange
                )
            for z in reversed(zrange)
        )
    }

    {'y':^{len(yrange)}}
    {
        '\n    '.join(
                ''.join(
                    '.#'[any((x, y, z) in all_voxels for x in xrange)]
                    for y in yrange
                )
            for z in reversed(zrange)
        )
    }
    """


if __name__ == "__main__":
    raise SystemExit(main())
