import sys
import re
from itertools import cycle
from functools import reduce


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Instructions = str
type Network = dict[str, tuple[str, str]]


def part1(raw: str):
    instructions, network = parse(raw)
    start, goal = "AAA", "ZZZ"
    position = start
    steps = 0
    for instruction in cycle(instructions):
        if position == goal:
            break
        position = network[position]["LR".index(instruction)]
        steps += 1
    return steps


def part2(raw: str):
    instructions, network = parse(raw)
    starting_positions = [node for node in network if node.endswith("A")]
    goal_cycles = []
    for position in starting_positions:
        last_seen = {}
        steps = 0
        goal_step = None
        start_of_cycle = None
        for instr_no, instruction in cycle(enumerate(instructions)):
            if (instr_no, position) in last_seen:
                start_of_cycle = last_seen[instr_no, position]
                break
            if position.endswith("Z"):
                assert goal_step is None  # not actually true for the example
                goal_step = steps
            last_seen[instr_no, position] = steps
            position = network[position]["LR".index(instruction)]
            steps += 1
        assert goal_step is not None
        assert start_of_cycle is not None
        assert goal_step >= start_of_cycle
        cycle_length = steps - start_of_cycle
        goal_cycles.append((goal_step, cycle_length))
    goal_steps, cycle_lengths = zip(*goal_cycles)
    common_offset = min(goal_steps)
    remainders = [goal_step - common_offset for goal_step in goal_steps]
    congruences = list(zip(remainders, cycle_lengths))
    return reduce(crt, congruences)[0] + common_offset


def parse(raw: str) -> tuple[Instructions, Network]:
    network = {}
    instructions, graph = raw.strip().split("\n\n")
    for line in graph.splitlines():
        node, left, right = re.findall(r"[1-9A-Z]+", line)
        network[node] = left, right
    return instructions, network


def crt(eqn_1: tuple[int, int], eqn_2: tuple[int, int]) -> tuple[int, int]:
    # https://math.stackexchange.com/a/1644698
    (a, m) = eqn_1
    (b, n) = eqn_2
    d, u, v = euclid(m, n)
    assert (a - b) % d == 0
    return (
        (a - m * u * (a - b) // d) % (m * n // d),
        m * n // d,
    )


def euclid(m, n):
    r0, r1 = m, n
    s0, s1 = 1, 0
    t0, t1 = 0, 1
    while r1 != 0:
        q, r = divmod(r0, r1)
        r0, r1 = r1, r
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
    return r0, s0, t0


if __name__ == "__main__":
    raise SystemExit(main())
