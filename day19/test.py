from typing import Iterator, Set, Tuple

import pytest

from . import main


@pytest.mark.slow
def test_main() -> None:
    main.main()


@pytest.mark.parametrize(
    ["example", "expected"],
    (
        ('ababbb', True),
        ('bababa', False),
        ('abbbab', True),
        ('aaabbb', False),
        ('aaaabbb', False),
    )
)
def test_matches_rule_0(
    example: str,
    expected: bool,
    flat_rule_0: Set[str],
) -> None:
    assert (example in flat_rule_0) == expected


@pytest.mark.parametrize(
    ["example", "expected"],
    (
        ('abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa', False),
        ('bbabbbbaabaabba', True),
        ('babbbbaabbbbbabbbbbbaabaaabaaa', True),
        ('aaabbbbbbaaaabaababaabababbabaaabbababababaaa', True),
        ('bbbbbbbaaaabbbbaaabbabaaa', True),
        ('bbbababbbbaaaaaaaabbababaaababaabab', True),
        ('ababaaaaaabaaab', True),
        ('ababaaaaabbbaba', True),
        ('baabbaaaabbaaaababbaababb', True),
        ('abbbbabbbbaaaababbbbbbaaaababb', True),
        ('aaaaabbaabaaaaababaa', True),
        ('aaaabbaaaabbaaa', False),
        ('aaaabbaabbaaaaaaabbbabbbaaabbaabaaa', True),
        ('babaaabbbaaabaababbaabababaaab', False),
        ('aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba', True),
    )
)
def test_special_case_answer_2(
    example: str,
    expected: bool,
    flat_rules_42_and_31: Tuple[Set[str], Set[str]],
) -> None:
    flat_rule_42, flat_rule_31 = flat_rules_42_and_31
    assert (
        main.matches_special_case(example, flat_rule_42, flat_rule_31) ==
        expected
    )


@pytest.fixture(scope='module')
def flat_rule_0() -> Iterator[Set[str]]:
    block_rules = (
        '0: 4 1 5\n'
        '1: 2 3 | 3 2\n'
        '2: 4 4 | 5 5\n'
        '3: 4 5 | 5 4\n'
        '4: "a"\n'
        '5: "b"\n'
    )
    rule_dict = dict(
        main.parse_compound_rule(compound_rule)
        for compound_rule in block_rules.splitlines()
    )
    simple_rule_dict = main.full_simplify_rule_dict(rule_dict)

    yield main.flatten_rule(simple_rule_dict[main.RuleRef(0)])


@pytest.fixture(scope='module')
def flat_rules_42_and_31() -> Iterator[Tuple[Set[str], Set[str]]]:
    block_rules = (
        '42: 9 14 | 10 1\n'
        '9: 14 27 | 1 26\n'
        '10: 23 14 | 28 1\n'
        '1: "a"\n'
        '11: 42 31\n'
        '5: 1 14 | 15 1\n'
        '19: 14 1 | 14 14\n'
        '12: 24 14 | 19 1\n'
        '16: 15 1 | 14 14\n'
        '31: 14 17 | 1 13\n'
        '6: 14 14 | 1 14\n'
        '2: 1 24 | 14 4\n'
        '0: 8 11\n'
        '13: 14 3 | 1 12\n'
        '15: 1 | 14\n'
        '17: 14 2 | 1 7\n'
        '23: 25 1 | 22 14\n'
        '28: 16 1\n'
        '4: 1 1\n'
        '20: 14 14 | 1 15\n'
        '3: 5 14 | 16 1\n'
        '27: 1 6 | 14 18\n'
        '14: "b"\n'
        '21: 14 1 | 1 14\n'
        '25: 1 1 | 1 14\n'
        '22: 14 14\n'
        '8: 42\n'
        '26: 14 22 | 1 20\n'
        '18: 15 15\n'
        '7: 14 5 | 1 21\n'
        '24: 14 1\n'
    )
    rule_dict = dict(
        main.parse_compound_rule(compound_rule)
        for compound_rule in block_rules.splitlines()
    )
    simple_rule_dict = main.full_simplify_rule_dict(rule_dict)

    flat_rule_42 = main.flatten_rule(simple_rule_dict[main.RuleRef(42)])
    flat_rule_31 = main.flatten_rule(simple_rule_dict[main.RuleRef(31)])
    yield flat_rule_42, flat_rule_31
