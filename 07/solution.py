import sys
from collections import Counter


def main():
    raw = sys.stdin.read()
    if "1" in sys.argv:
        print(f"Part 1: {part1(raw)}")
    if "2" in sys.argv:
        print(f"Part 2: {part2(raw)}")
    return 0


type Hand = str
type Card = str
type Bid = int


def part1(raw: str):
    hand_bid = parse(raw)
    hands = hand_bid.keys()
    ranked_hands = sorted(hands, key=hand_strength_1)
    return sum(rank * hand_bid[hand] for rank, hand in enumerate(ranked_hands, start=1))


def part2(raw: str):
    hand_bid = parse(raw)
    hands = hand_bid.keys()
    ranked_hands = sorted(hands, key=hand_strength_2)
    return sum(rank * hand_bid[hand] for rank, hand in enumerate(ranked_hands, start=1))


def parse(raw: str) -> dict[Hand, Bid]:
    hand_bid = {}
    for line in raw.strip().splitlines():
        hand, bid = line.split()
        assert hand not in hand_bid
        hand_bid[hand] = int(bid)
    return hand_bid


def hand_strength_1(hand: Hand, *, part2: bool = False) -> tuple[int, ...]:
    return hand_type_1(hand), *map(card_strength_1, hand)


def hand_strength_2(hand: Hand) -> tuple[int, ...]:
    return hand_type_2(hand), *map(card_strength_2, hand)


def hand_type_1(hand: Hand) -> int:
    card_counts = sorted(Counter(hand).values(), reverse=True)
    match card_counts:
        case [5]:
            return 7
        case [4, 1]:
            return 6
        case [3, 2]:
            return 5
        case [3, 1, 1]:
            return 4
        case [2, 2, 1]:
            return 3
        case [2, 1, 1, 1]:
            return 2
        case [1, 1, 1, 1, 1]:
            return 1
        case _:
            assert False


def hand_type_2(hand: Hand) -> int:
    return max(hand_type_1(new_hand) for new_hand in joker_subs(hand))


def joker_subs(hand: Hand):
    if "J" in hand:
        for card in "23456789TQKA":
            yield from joker_subs(hand.replace("J", card, 1))
    else:
        yield hand


def card_strength_1(card: Card) -> int:
    return "23456789TJQKA".index(card)


def card_strength_2(card: Card) -> int:
    return "J23456789TQKA".index(card)


if __name__ == "__main__":
    raise SystemExit(main())
