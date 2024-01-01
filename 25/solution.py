import sys
import networkx as nx
from itertools import combinations


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Node = str
type Edge = tuple[Node, Node]


def part1(raw: str):
    G = parse(raw)
    for s, t in combinations(G.nodes, 2):
        cut_value, partition = nx.minimum_cut(G, s, t)
        S, T = partition
        if cut_value == 3:
            return len(S) * len(T)


def part2(raw: str):
    return "✨"


def parse(raw: str) -> nx.Graph:
    G = nx.Graph()
    for line in raw.strip().splitlines():
        lhs, rhs = line.split(":")
        u = lhs.strip()
        for v in rhs.split():
            G.add_edge(u, v, capacity=1)
    return G


if __name__ == "__main__":
    raise SystemExit(main())
