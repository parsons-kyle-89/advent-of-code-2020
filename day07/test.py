from typing import List, Dict

import pytest

from . import main


def parse_rules(raw_rules: str) -> main.WeightedDigraph[main.BagType]:
    bag_nodes = [
        main.parse_bag_rule(raw_rule.strip())
        for raw_rule in raw_rules.split('\n')
    ]
    return main.WeightedDigraph(bag_nodes)


def test_main() -> None:
    main.main()


@pytest.mark.parametrize(
    ['it', 'expected'],
    (
        ([], []),
        ([1], [1]),
        ([1, 1], [1]),
        ([1, 2], [1, 2]),
        ([1, 2, 3, 4], [1, 2, 3, 4]),
        ([1, 2, 2, 4], [1, 2]),
    )
)
def test_takeuntil_stable(it: List[int], expected: List[int]) -> None:
    assert list(main.takeuntil_stable(it)) == expected


def test_iterate_func() -> None:
    it = main.iterate_func(lambda x: x + 1, 0)
    assert all(actual == expected for actual, expected in zip(it, range(10)))


@pytest.mark.parametrize(
    ['dicts', 'expected'],
    (
        ([{}], {}),
        ([{}, {}], {}),
        ([{}, {}, {}], {}),
        ([{'a': 1}], {'a': 1}),
        ([{'a': 1}, {'b': 2}], {'a': 1, 'b': 2}),
        ([{'a': 1}, {'a': 2}], {'a': 3}),
        ([{'a': 1, 'c': 4}, {'b': 2, 'c': 3}], {'a': 1, 'b': 2, 'c': 7}),
        ([{'a': 1}, {'a': 2}, {'b': 4}], {'a': 3, 'b': 4}),
    )
)
def test_sum_dicti(
    dicts: List[Dict[str, int]],
    expected: Dict[str, int],
) -> None:
    actual = main.sum_dicts(dicts)
    assert actual == expected


def test_in_set() -> None:
    raw_rules = """
        light red bags contain 1 bright white bag, 2 muted yellow bags.
        dark orange bags contain 3 bright white bags, 4 muted yellow bags.
        bright white bags contain 1 shiny gold bag.
        muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
        shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
        dark olive bags contain 3 faded blue bags, 4 dotted black bags.
        vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
        faded blue bags contain no other bags.
        dotted black bags contain no other bags.
    """.strip()

    bag_rule_digraph = parse_rules(raw_rules)
    actual_in_set = bag_rule_digraph.in_set({main.BagType('shiny gold')})
    assert len(actual_in_set) - 1 == 4


def test_weighted_out_set() -> None:
    raw_rules = """
        shiny gold bags contain 2 dark red bags.
        dark red bags contain 2 dark orange bags.
        dark orange bags contain 2 dark yellow bags.
        dark yellow bags contain 2 dark green bags.
        dark green bags contain 2 dark blue bags.
        dark blue bags contain 2 dark violet bags.
        dark violet bags contain no other bags.
    """.strip()

    bag_rule_digraph = parse_rules(raw_rules)
    actual_weighted_out_set = (
        bag_rule_digraph.weighted_out_set({main.BagType('shiny gold'): 1})
    )
    assert sum(actual_weighted_out_set.values()) - 1 == 126
