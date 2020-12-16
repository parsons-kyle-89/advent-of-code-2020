from dataclasses import dataclass
from itertools import chain
import os.path
from typing import Iterable, Iterator, List

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

Ticket = List[int]


@dataclass(frozen=True)
class Range:
    lower: int
    upper: int

    def validate(self, value: int) -> bool:
        return self.lower <= value <= self.upper


@dataclass(frozen=True)
class Rule:
    name: str
    lower_range: Range
    upper_range: Range

    def validate(self, value: int) -> bool:
        return (
            self.lower_range.validate(value) or
            self.upper_range.validate(value)
        )

    @classmethod
    def from_str(cls, raw_rule: str) -> "Rule":
        name, raw_ranges = raw_rule.split(': ', 1)
        raw_lower_range, raw_upper_range = raw_ranges.split(' or ')
        return cls(
            name,
            cls._parse_range(raw_lower_range),
            cls._parse_range(raw_upper_range),
        )

    @staticmethod
    def _parse_range(raw_range: str) -> Range:
        raw_lower, raw_upper = raw_range.split('-', 1)
        return Range(int(raw_lower), int(raw_upper))


def parse_ticket(raw_ticket: str) -> Ticket:
    return [int(raw_value) for raw_value in raw_ticket.split(',')]


def invalid_fields(ticket: Ticket, rules: Iterable[Rule]) -> Iterator[int]:
    for field in ticket:
        if all(not rule.validate(field) for rule in rules):
            yield field


def is_valid(ticket: Ticket, rules: Iterable[Rule]) -> bool:
    return len(list(invalid_fields(ticket, rules))) == 0


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_rules, raw_my_ticket, raw_nearby_tickets = (
            f.read().split('\n\n', 2)
        )

    rules = [Rule.from_str(raw_rule) for raw_rule in raw_rules.splitlines()]
    nearby_tickets = [
        parse_ticket(raw_ticket)
        for raw_ticket in raw_nearby_tickets.splitlines()[1:]
    ]

    answer_1 = sum(chain.from_iterable(
        invalid_fields(ticket, rules) for ticket in nearby_tickets
    ))
    print(answer_1)

    valid_nearby_tickets = [
        ticket for ticket in nearby_tickets 
        if is_valid(ticket, rules)
    ]


if __name__ == "__main__":
    main()
