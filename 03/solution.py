import sys
import re
from dataclasses import dataclass


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Coord = complex


@dataclass(frozen=True)
class Entity:
    id: int
    position: Coord
    string: str

    def is_number(self):
        return self.string.isnumeric()

    def coords(self):
        return {self.position + offset * 1j for offset in range(len(self.string))}

    def __int__(self):
        if not self.is_number():
            raise ValueError()
        return int(self.string)


def part1(raw: str):
    entities = set(parse_entities(raw))
    numbers = set(filter(Entity.is_number, entities))
    symbols = entities - numbers
    entity_at = {coord: entity for entity in entities for coord in entity.coords()}
    adjacent_entities = {
        entity: {
            entity_at[neighbour]
            for coord in entity.coords()
            for neighbour in neighbours(coord)
            if neighbour in entity_at
        }
        for entity in entities
    }
    parts = {number for number in numbers if adjacent_entities[number] & symbols}
    return sum(int(part.string) for part in parts)


def part2(raw: str):
    entities = set(parse_entities(raw))
    numbers = set(filter(Entity.is_number, entities))
    symbols = entities - numbers
    entity_at = {coord: entity for entity in entities for coord in entity.coords()}
    adjacent_entities = {
        entity: {
            entity_at[neighbour]
            for coord in entity.coords()
            for neighbour in neighbours(coord)
            if neighbour in entity_at
        }
        for entity in entities
    }
    total = 0
    for symbol in symbols:
        adjacent_numbers = adjacent_entities[symbol] & numbers
        if len(adjacent_numbers) == 2:
            a, b = map(int, adjacent_numbers)
            total += a * b
    return total


def parse_entities(schematic: str):
    next_id = 0
    for r, line in enumerate(schematic.strip().splitlines()):
        for match in re.finditer(r"[0-9]+|[^.]", line):
            c = match.start()
            yield Entity(id=next_id, position=r + c * 1j, string=match[0])
            next_id += 1


def neighbours(coord: Coord) -> set[Coord]:
    return {coord + dr + dc for dr in (-1, 0, +1) for dc in (-1j, 0, +1j) if dr or dc}


if __name__ == "__main__":
    raise SystemExit(main())
