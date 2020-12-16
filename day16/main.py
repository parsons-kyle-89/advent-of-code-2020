from dataclasses import dataclass
from functools import reduce
from itertools import chain
from operator import mul
import os.path
import re
from typing import Dict, Iterable, Iterator, List, Tuple

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

Ticket = List[int]
RULE_RE = re.compile(r'\A([^:]*): (\d*)-(\d*) or (\d*)-(\d*)\Z', re.ASCII)


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
        (name, raw_lower_a, raw_lower_b, raw_upper_a, raw_upper_b), *_ = (
            re.findall(RULE_RE, raw_rule)
        )
        return cls(
            name,
            Range(int(raw_lower_a), int(raw_lower_b)),
            Range(int(raw_upper_a), int(raw_upper_b)),
        )


def parse_ticket(raw_ticket: str) -> Ticket:
    return [int(raw_value) for raw_value in raw_ticket.split(',')]


def invalid_fields(ticket: Ticket, rules: Iterable[Rule]) -> Iterator[int]:
    return iter(
        field for field in ticket
        if all(not rule.validate(field) for rule in rules)
    )


def is_valid(ticket: Ticket, rules: Iterable[Rule]) -> bool:
    return len(list(invalid_fields(ticket, rules))) == 0


def deduce(tickets: Iterable[Ticket], rules: Iterable[Rule]) -> Dict[int, str]:
    idx_to_rules = {
        idx: [
            rule for rule in rules
            if all(rule.validate(value) for value in field)
        ]
        for idx, field in enumerate(zip(*tickets))
    }
    idx_to_name = {}
    while idx_to_rules:
        idx, rule = pop_known_correspondence(idx_to_rules)
        idx_to_name[idx] = rule.name
    return idx_to_name


def pop_known_correspondence(
    idx_to_rules: Dict[int, List[Rule]]
) -> Tuple[int, Rule]:
    try:
        idx, rules = next(
            (idx, rules)
            for idx, rules in idx_to_rules.items()
            if len(rules) == 1
        )
    except StopIteration:
        raise ValueError("idx_to_rules contains no known correspondence")
    rule = rules[0]
    for other_rules in idx_to_rules.values():
        other_rules.remove(rule)
    idx_to_rules.pop(idx)
    return idx, rule


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
    assert answer_1 == 26009
    print(answer_1)

    my_ticket = parse_ticket(raw_my_ticket.splitlines()[1])
    valid_nearby_tickets = [
        ticket for ticket in nearby_tickets
        if is_valid(ticket, rules)
    ] + [my_ticket]
    idx_to_name = deduce(valid_nearby_tickets, rules)
    nice_my_ticket = {name: my_ticket[i] for i, name in idx_to_name.items()}
    answer_2 = reduce(
        mul,
        (
            value for name, value in nice_my_ticket.items()
            if name.startswith('departure')
        ),
        1
    )
    assert answer_2 == 589685618167
    print(answer_2)


if __name__ == "__main__":
    main()
