import sys
import re
import collections


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Module = tuple[str, list[str]]
type State = dict[str, bool | dict[str, bool]]


def part1(raw: str):
    modules = parse(raw)
    sources = source_graph(modules)
    state = initial_state(modules, sources)
    total_low = 0
    total_high = 0
    for i in range(1000):
        pulses = step(modules, state)
        for source, pulse, destination in pulses:
            total_high += pulse
            total_low += not pulse
    return total_low * total_high


def part2(raw: str):
    print(to_dot(raw))
    ...  # solved by hand by looking at graph


def step(modules: dict[str, Module], state: State) -> list[tuple[str, bool, str]]:
    pulses_sent = []
    frontier = [("button", False, "broadcaster")]
    while frontier:
        new_frontier = []
        for source, pulse, name in frontier:
            # print(f"{source} -{['low', 'high'][pulse]}-> {name}")
            pulses_sent.append((source, pulse, name))
            if name not in modules:
                continue
            kind, destinations = modules[name]
            if kind == "%":
                assert isinstance(state[name], bool)
                if pulse:
                    continue
                else:
                    state[name] = not state[name]
                    outgoing = state[name]
            elif kind == "&":
                state_ = state[name]
                assert isinstance(state_, dict)
                state_[source] = pulse
                if all(state_.values()):
                    outgoing = False
                else:
                    outgoing = True
            else:
                outgoing = pulse
            new_frontier.extend(
                (name, outgoing, destination) for destination in destinations
            )
        frontier = new_frontier
    return pulses_sent


def initial_state(modules: dict[str, Module], sources: dict[str, set[str]]) -> State:
    state = {}
    for name, (kind, destinations) in modules.items():
        if kind == "%":
            state[name] = False
        elif kind == "&":
            state[name] = {source: False for source in sources[name]}
        else:
            pass
    return state


def source_graph(modules: dict[str, Module]) -> dict[str, set[str]]:
    sources = collections.defaultdict(set)
    for name, (kind, destinations) in modules.items():
        for destination in destinations:
            sources[destination].add(name)
    return dict(sources)


def parse(raw: str) -> dict[str, tuple[str, list[str]]]:
    modules = {}
    for line in raw.strip().splitlines():
        match = re.match(r"([%&]?)([a-z]+) -> (.+)", line)
        assert match, f"should match {line!r}"
        kind = match[1]
        name = match[2]
        destinations = [dest.strip() for dest in match[3].split(",")]
        modules[name] = kind, destinations
    return modules


def to_dot(raw: str) -> str:
    lines = []
    for line in raw.splitlines():
        lhs, rhs = line.split("->")
        name = lhs.strip("%&")
        lines.append(f"{name} -> {{{rhs}}}")
        if lhs.startswith("%"):
            lines.append(f"{name} [color=blue]")
        elif lhs.startswith("&"):
            lines.append(f"{name} [color=red]")
        else:
            lines.append(f"{name} [color=green]")
    return f"{{ {'\n'.join(lines)} }}"


if __name__ == "__main__":
    raise SystemExit(main())
