import sys
import re
from pprint import pprint


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Vector = complex
type Tile = Vector
type Graph[N, W] = dict[N, dict[N, list[W]]]


def part1(raw: str):
    start, end, graph = parse(raw)
    return longest_path(start, end, graph)


def part2(raw: str):
    # TODO: optimise with early backtracking
    slopes_removed = re.sub(r"[><v^]", ".", raw)
    start, end, graph = parse(slopes_removed)
    return longest_path(start, end, graph)


DIRECTIONS = {
    ".": (+1, -1, +1j, -1j),
    "v": (+1,),
    "^": (-1,),
    ">": (+1j,),
    "<": (-1j,),
    "#": (),
}


def parse(raw: str) -> tuple[Tile, Tile, Graph[Tile, int]]:
    lines = raw.strip().splitlines()
    height = len(lines)
    grid = {}
    start, end = None, None
    for row, line in enumerate(raw.strip().splitlines()):
        for col, char in enumerate(line):
            tile = row + col * 1j
            grid[tile] = char
            if char == "." and row == 0:
                start = tile
            if char == "." and row == height - 1:
                end = tile
    assert start is not None
    assert end is not None
    return start, end, to_graph(grid)


def to_graph(grid: dict[Tile, str]) -> Graph[Tile, int]:
    navigable = extract(grid, ".^v<>")
    junctions_and_ends = {
        tile for tile in navigable if len(neighbors(tile) & navigable) != 2
    }
    connected_tiles = {
        tile: {tile + direction for direction in DIRECTIONS[grid[tile]]} & navigable
        for tile in navigable
    }
    unexplored = junctions_and_ends.copy()
    graph: Graph[Tile, int] = {}
    while unexplored:
        node = unexplored.pop()
        for tile in connected_tiles[node]:
            previous_tile, current_tile = node, tile
            distance = 1
            while current_tile not in junctions_and_ends:
                successors = connected_tiles[current_tile] - {previous_tile}
                if not successors:
                    break
                (successor,) = successors
                previous_tile, current_tile = current_tile, successor
                distance += 1
            else:
                edges = graph.setdefault(node, {})
                weights = edges.setdefault(current_tile, [])
                weights.append(distance)
    return graph


def longest_path(
    start: Tile,
    end: Tile,
    graph: Graph[Tile, int],
    visited: set[Tile] | None = None,
) -> int:
    if start == end:
        return 0
    if visited is None:
        visited = set()
    result = -1
    visited.add(start)
    for successor in graph[start]:
        if successor not in visited:
            path_cost = longest_path(successor, end, graph, visited)
            edge_cost = max(graph[start][successor])
            if path_cost != -1:
                result = max(result, path_cost + edge_cost)
    visited.remove(start)
    return result


def extract(grid: dict[Tile, str], symbols: str) -> set[Tile]:
    return {tile for tile, char in grid.items() if char in symbols}


def neighbors(tile: Tile) -> set[Tile]:
    return {tile + direction for direction in DIRECTIONS["."]}


if __name__ == "__main__":
    raise SystemExit(main())
