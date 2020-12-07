from collections import defaultdict
from dataclasses import dataclass
from itertools import takewhile
import os.path
from typing import Collection, DefaultDict, Dict, Iterable, Iterator, List, Mapping, NewType, Set

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

BagType = NewType('BagType', str)


@dataclass
class SubRule:
    bag_type: BagType
    count: int


@dataclass
class Rule:
    bag_type: BagType
    sub_rules: List[SubRule]


def parse_rule(raw_rule: str) -> Rule:
    raw_bag_type, raw_sub_rules = raw_rule.split(' bags contain ', 1)
    bag_type = BagType(raw_bag_type)
    parsed_sub_rules = [
        parse_sub_rule(raw_sub_rule)
        for raw_sub_rule in raw_sub_rules.split(', ')
    ]
    sub_rules = [sub_rule for sub_rule in parsed_sub_rules if sub_rule.bag_type != BagType('other')]
    return Rule(bag_type, sub_rules)


def parse_sub_rule(raw_sub_rule: str) -> SubRule:
    stripped_raw_sub_rule = raw_sub_rule.strip('.').removesuffix(' bag').removesuffix(' bags')
    raw_count, raw_bag_type = stripped_raw_sub_rule.split(' ', 1)
    bag_type = BagType(raw_bag_type)
    count = parse_count(raw_count)
    return SubRule(bag_type, count)


def parse_count(raw_count: str) -> int:
    if raw_count == 'no':
        return 0
    return int(raw_count)


def able_to_contain_any(bag_types: Collection[BagType], rules: Iterable[Rule]) -> Set[BagType]:
    return {rule.bag_type for rule in rules if any(bag_type in [sub_rule.bag_type for sub_rule in rule.sub_rules] for bag_type in bag_types)}


def transitive_able_to_contain_any(bag_types: Collection[BagType], rules: Iterable[Rule]) -> Set[BagType]:
    containing_set = able_to_contain_any(bag_types, rules)
    while True:
        new_containing_set = containing_set.union(able_to_contain_any(containing_set, rules))
        if new_containing_set == containing_set:
            break
        containing_set = new_containing_set
    return containing_set


def contained_bags(bag_counts: Mapping[BagType, int], rules: Mapping[BagType, Rule]) -> Dict[BagType, int]:
    _contained_bags: DefaultDict[BagType, int] = defaultdict(lambda: 0)
    for bag_type, outer_bag_count in bag_counts.items():
        rule = rules[bag_type]
        for sub_rule in rule.sub_rules:
            _contained_bags[sub_rule.bag_type] += outer_bag_count * sub_rule.count
    return dict(_contained_bags)


def bag_neighborhoods(bag_type: BagType, rule_map: Mapping[BagType, Rule]) -> Iterator[Dict[BagType, int]]:
    neighborhood = {bag_type: 1}
    while True:
        yield neighborhood
        neighborhood = contained_bags(neighborhood, rule_map)


def bags_inside(bag_type: BagType, rule_map: Mapping[BagType, Rule]) -> Dict[BagType, int]:
    nested_bags = takewhile(bool, bag_neighborhoods(bag_type, rule_map))
    all_bags: DefaultDict[BagType, int] = defaultdict(lambda: 0)
    for nested_bag in nested_bags:
        for bag_type, count in nested_bag.items():
            all_bags[bag_type] += count
    all_bags[bag_type] -= 1
    return dict(all_bags)


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        rules = [parse_rule(raw_rule.strip()) for raw_rule in f.readlines()]

    print(len(transitive_able_to_contain_any({BagType('shiny gold')}, rules)))

    rule_map = {rule.bag_type: rule for rule in rules}
    print(sum(count for count in bags_inside(BagType('shiny gold'), rule_map).values()))


if __name__ == "__main__":
    main()
