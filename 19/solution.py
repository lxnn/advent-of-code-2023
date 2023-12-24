import sys, math, re


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Cond = tuple[str, str, int]
type Rule = tuple[Cond | None, str]
type Workflow = list[Rule]
type WorkflowTable = dict[str, Workflow]
type Part = dict[str, int]
type PartSet = dict[str, range]


def part1(raw: str):
    workflows, parts = parse(raw)
    acceptable_parts = [part for part in parts if is_acceptable(workflows, part)]
    return sum(sum(part.values()) for part in acceptable_parts)


def part2(raw: str):
    workflows, parts = parse(raw)
    every_combination = dict(
        x=range(1, 4001), m=range(1, 4001), a=range(1, 4001), s=range(1, 4001)
    )
    return count_acceptable(workflows, "in", every_combination)


def parse(raw: str) -> tuple[WorkflowTable, list[Part]]:
    raw_workflows, raw_parts = raw.split("\n\n")
    workflows = {}
    for line in raw_workflows.splitlines():
        name, workflow = parse_workflow(line)
        workflows[name] = workflow
    parts = []
    for line in raw_parts.splitlines():
        parts.append(parse_part(line))
    return workflows, parts


def parse_workflow(raw: str) -> tuple[str, Workflow]:
    match = re.match(r"([A-Za-z]+)\{([^}]*)\}", raw)
    assert match
    return match[1], [parse_rule(word) for word in match[2].split(",")]


def parse_rule(raw: str) -> Rule:
    match = re.match(r"(([xmas]+)([><])([0-9]+):)?([A-Za-z]+)", raw)
    assert match
    condition = None
    if match[1]:
        condition = match[2], match[3], int(match[4])
    return condition, match[5]


def parse_part(raw: str) -> Part:
    part = {}
    for word in raw.strip().strip("{}").split(","):
        axis, value = word.split("=")
        part[axis] = int(value)
    return part


def is_acceptable(workflows: WorkflowTable, part: Part) -> bool:
    name = "in"
    while name not in ("A", "R"):
        workflow = workflows[name]
        for rule in workflow:
            cond, dest = rule
            if cond is None:
                name = dest
                break
            axis, op, value = cond
            if op == "<" and part[axis] < value or op == ">" and part[axis] > value:
                name = dest
                break
    return name == "A"


def count_acceptable(
    workflows: WorkflowTable,
    name: str,
    partset: PartSet,
) -> int:
    if name == "A":
        return math.prod(len(range_) for range_ in partset.values())
    if name == "R":
        return 0
    total = 0
    workflow = workflows[name]
    for rule in workflow:
        cond, dest = rule
        if cond is None:
            total += count_acceptable(workflows, dest, partset)
            break
        axis, op, value = cond
        range_ = partset[axis]
        if op == "<":
            lower = range(range_.start, min(range_.stop, value))
            upper = range(max(range_.start, value), range_.stop)
            total += count_acceptable(workflows, dest, {**partset, axis: lower})
            partset = {**partset, axis: upper}
        elif op == ">":
            lower = range(range_.start, min(range_.stop, value + 1))
            upper = range(max(range_.start, value + 1), range_.stop)
            total += count_acceptable(workflows, dest, {**partset, axis: upper})
            partset = {**partset, axis: lower}
        else:
            assert False
    return total


if __name__ == "__main__":
    sys.exit(main())
