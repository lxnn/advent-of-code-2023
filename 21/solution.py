import sys
import numpy as np


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Vector = complex
type Coord = Vector


def part1(raw: str):
    grid = parse(raw)
    (start,) = extract(grid, "S")
    visualise(grid, possible_locations(grid, start, steps=6))
    return len(possible_locations(grid, start, steps=6))


P2_STEPS = 26501365


def part2(raw: str):
    grid = parse(raw)
    height, width = dimensions(grid)
    x0 = P2_STEPS % height
    x1 = x0 + height
    x2 = x1 + height
    tiled = tile(grid, 7, 7)
    (start,) = extract(tiled, "S")
    y0 = len(possible_locations(tiled, start, steps=x0))
    y1 = len(possible_locations(tiled, start, steps=x1))
    y2 = len(possible_locations(tiled, start, steps=x2))
    A = np.array(
        [
            [x0**2, x0, 1],
            [x1**2, x1, 1],
            [x2**2, x2, 1],
        ]
    )
    y = np.array([y0, y1, y2])
    a, b, c = np.linalg.inv(A) @ y
    return a * P2_STEPS**2 + b * P2_STEPS + c


def tile(grid, m, n):
    height, width = dimensions(grid)
    assert m % 2 == 1
    assert n % 2 == 1
    tiled_grid = {
        coord + height * i + width * j * 1j: "." if char == "S" else char
        for i in range(m)
        for j in range(n)
        for coord, char in grid.items()
    }
    for start in extract(grid, "S"):
        tiled_grid[start + m // 2 * height + n // 2 * width * 1j] = "S"
    return tiled_grid


def possible_locations(grid: dict[Coord, str], start: Coord, steps: int) -> set[Coord]:
    navigable = extract(grid, ".") | extract(grid, "S")
    locations = {start}
    for step in range(steps):
        locations = neighbors(locations) & navigable
    return locations


def distance(a: Coord, b: Coord, grid: dict[Coord, str]) -> int:
    navigable = extract(grid, ".") | extract(grid, "S")
    positions = {a}
    steps = 0
    while b not in positions:
        positions = neighbors(positions) & navigable
        steps += 1
    return steps


def dimensions(grid: dict[Coord, str]) -> tuple[int, int]:
    height = int(1 + max(coord.real for coord in grid))
    width = int(1 + max(coord.imag for coord in grid))
    return height, width


def parse(raw: str) -> dict[Coord, str]:
    return {
        r + c * 1j: char
        for r, line in enumerate(raw.strip().splitlines())
        for c, char in enumerate(line)
    }


def neighbors(coords: Coord | set[Coord]) -> set[Coord]:
    if isinstance(coords, set):
        return set.union(*map(neighbors, coords))
    else:
        return {coords + direction for direction in (+1, -1, +1j, -1j)}


def extract(grid: dict[Coord, str], target: str) -> set[Coord]:
    return {coord for coord, tile in grid.items() if tile == target}


def visualise(grid: dict[Coord, str], filled: set[Coord], fillchar="O"):
    height, width = dimensions(grid)
    for r in range(height):
        for c in range(width):
            coord = r + c * 1j
            if coord in filled:
                print(fillchar, end="")
            else:
                print(grid[coord], end="")
        print()


def save_image(grid, filled, name):
    with open(f"{name}.ppm", "w") as file:
        file.write(to_ppm(grid, filled))


def to_ppm(grid, filled):
    height, width = dimensions(grid)
    fill_colour = "0 0 255"
    colour = {".": "255 255 255", "#": "0 0 0", "S": "0 255 0"}
    return f"P3 {width} {height} 255\n" + "\n".join(
        " ".join(
            fill_colour if r + c * 1j in filled else colour[grid[r + c * 1j]]
            for c in range(width)
        )
        for r in range(height)
    )


if __name__ == "__main__":
    raise SystemExit(main())
