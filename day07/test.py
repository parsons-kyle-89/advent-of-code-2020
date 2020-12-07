from . import main


def test_main() -> None:
    main.main()


def test_transitive_able_to_contain_any() -> None:
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

    rules = [main.parse_rule(rule.strip()) for rule in raw_rules.split('\n')]
    actual = main.transitive_able_to_contain_any(
        {main.BagType('shiny gold')}, rules
    )
    assert len(actual) == 4


def test_bags_inside() -> None:
    raw_rules = """
        shiny gold bags contain 2 dark red bags.
        dark red bags contain 2 dark orange bags.
        dark orange bags contain 2 dark yellow bags.
        dark yellow bags contain 2 dark green bags.
        dark green bags contain 2 dark blue bags.
        dark blue bags contain 2 dark violet bags.
        dark violet bags contain no other bags.
    """.strip()

    rules = [main.parse_rule(rule.strip()) for rule in raw_rules.split('\n')]
    rule_map = {rule.bag_type: rule for rule in rules}
    actual = main.bags_inside(main.BagType('shiny gold'), rule_map)
    assert sum(count for count in actual.values()) == 126
