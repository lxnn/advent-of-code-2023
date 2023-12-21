from __future__ import annotations
import sys
from dataclasses import dataclass
from collections.abc import Callable, Iterable
from heapq import heappop, heappush
from itertools import count
from typing import Self


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


def part1(raw: str):
    puzzle = Puzzle.from_str(raw)
    solution = astar_search(
        start=puzzle.starting_states(),
        goal=puzzle.goal,
        successors=puzzle.successors,
        cost=puzzle.cost,
        heuristic=puzzle.heuristic,
    )
    if solution is not None:
        path_cost, path = solution
        return path_cost


def part2(raw: str):
    puzzle: Puzzle2 = Puzzle2.from_str(raw)
    solution = astar_search(
        start=puzzle.starting_states(),
        goal=puzzle.goal,
        successors=puzzle.successors,
        cost=puzzle.cost,
        heuristic=puzzle.heuristic,
    )
    if solution is not None:
        path_cost, path = solution
        return path_cost


@dataclass(frozen=True)
class Vector:
    i: int
    j: int

    def __add__(self, other: Vector) -> Vector:
        return Vector(i=self.i + other.i, j=self.j + other.j)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(i=self.i - other.i, j=self.j - other.j)

    @property
    def mhat_norm(self) -> int:
        return abs(self.i) + abs(self.j)

    def turn_left(self) -> Vector:
        return Vector(i=-self.j, j=self.i)

    def turn_right(self) -> Vector:
        return Vector(i=self.j, j=-self.i)


@dataclass
class Puzzle:
    dimensions: Vector
    grid: dict[Vector, int]

    @dataclass(frozen=True)
    class State:
        block: Vector
        heading: Vector
        distance: int

        def go_forward(self) -> Puzzle.State:
            return Puzzle.State(
                block=self.block + self.heading,
                heading=self.heading,
                distance=self.distance + 1,
            )

        def go_left(self) -> Puzzle.State:
            return Puzzle.State(
                block=self.block + self.heading.turn_left(),
                heading=self.heading.turn_left(),
                distance=1,
            )

        def go_right(self) -> Puzzle.State:
            return Puzzle.State(
                block=self.block + self.heading.turn_right(),
                heading=self.heading.turn_right(),
                distance=1,
            )

    @classmethod
    def from_str(cls, string: str) -> Self:
        lines = string.strip().splitlines()
        return cls(
            dimensions=Vector(len(lines), len(lines[0])),
            grid={
                Vector(row, col): int(char)
                for row, line in enumerate(lines)
                for col, char in enumerate(line)
            },
        )

    def successors(self, state: Puzzle.State) -> Iterable[Puzzle.State]:
        for new_state in (
            state.go_forward(),
            state.go_left(),
            state.go_right(),
        ):
            if new_state.block in self.grid and new_state.distance <= 3:
                yield new_state

    def cost(self, state: Puzzle.State, successor: Puzzle.State) -> int:
        return self.grid[successor.block]

    def heuristic(self, state: Puzzle.State) -> int:
        return (self.goal_block - state.block).mhat_norm

    def starting_states(self) -> Iterable[Puzzle.State]:
        for heading in (Vector(0, 1), Vector(1, 0)):
            yield Puzzle.State(
                block=Vector(0, 0),
                heading=heading,
                distance=0,
            )

    @property
    def goal_block(self) -> Vector:
        return self.dimensions - Vector(1, 1)

    def goal(self, state: Puzzle.State) -> bool:
        return state.block == self.goal_block

    def visualise_path(self, path: Iterable[Puzzle.State]) -> str:
        coordset = {state.block for state in path}
        return "\n".join(
            "".join(
                "#"
                if Vector(row, col) in coordset
                else str(self.grid[Vector(row, col)])
                for col in range(self.dimensions.j)
            )
            for row in range(self.dimensions.i)
        )


class Puzzle2(Puzzle):
    def successors(self, state: Puzzle.State) -> Iterable[Puzzle.State]:
        if state.distance >= 4:
            for new_state in (state.go_left(), state.go_right()):
                if new_state.block in self.grid:
                    yield new_state
        if state.distance < 10:
            new_state = state.go_forward()
            if new_state.block in self.grid:
                yield new_state

    def goal(self, state: Puzzle.State) -> bool:
        return super().goal(state) and state.distance >= 4


def astar_search[
    S
](
    start: Iterable[S],
    goal: Callable[[S], bool],
    successors: Callable[[S], Iterable[S]],
    cost: Callable[[S, S], int],
    heuristic: Callable[[S], int],
) -> (tuple[int, list[S]] | None):
    num_iter = count(0)
    frontier: list[tuple[int, int, int, S, S]] = [
        (0, 0, next(num_iter), state, state) for state in start
    ]
    history = {}
    while frontier:
        _, path_cost, _, prev, state = heappop(frontier)
        if state in history:
            continue
        history[state] = prev
        if goal(state):
            return path_cost, reconstruct_path(state, history)
        for new_state in successors(state):
            new_path_cost = path_cost + cost(state, new_state)
            heappush(
                frontier,
                (
                    new_path_cost + heuristic(new_state),
                    new_path_cost,
                    next(num_iter),
                    state,
                    new_state,
                ),
            )


def reconstruct_path[S](end: S, history: dict[S, S]) -> list[S]:
    reverse_path = [end]
    while True:
        new_state = history[reverse_path[-1]]
        if new_state == reverse_path[-1]:
            break
        reverse_path.append(new_state)
    return list(reversed(reverse_path))


if __name__ == "__main__":
    raise SystemExit(main())
