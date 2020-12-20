import os.path
from itertools import product
import re
from typing import Dict, Iterator, Set, Tuple

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def parse_rule(raw_rule: str) -> Tuple[int, Set[str]]:
    ref, pipe_delim_parts = raw_rule.split(': ')
    parts = {
        (
            re.sub(r"(\d+)", lambda m: f"{{{m.group(0)}}}", part)
            .replace(' ', '')
            .replace('"', '')
        )
        for part in pipe_delim_parts.split(' | ')
    }
    return int(ref), parts


def fully_simplify_rule_dict(
    rule_dict: Dict[int, Set[str]]
) -> Dict[int, Set[str]]:
    while any(
        any('{' in option for option in rule)
        for rule in rule_dict.values()
    ):
        rule_dict = simplify_rule_dict(rule_dict)
    return rule_dict


def simplify_rule_dict(rule_dict: Dict[int, Set[str]]) -> Dict[int, Set[str]]:
    return {
        ref: simplify_rule(rule, rule_dict)
        for ref, rule in rule_dict.items()
    }


def simplify_rule(rule: Set[str], rule_dict: Dict[int, Set[str]]) -> Set[str]:
    no_rules: Set[str] = set()
    return no_rules.union(*(
        deref_option(option, rule_dict)
        for option in rule
    ))


def deref_option(option: str, rule_dict: Dict[int, Set[str]]) -> Set[str]:
    refs = [int(match) for match in re.findall(r"{(\d+)}", option)]
    stripped_option = re.sub(r"(\d+)", '', option)
    return {
        stripped_option.format(*derefs) for derefs in
        product(*(rule_dict[ref] for ref in refs))
    }


def pref_removed_once_or_more(
    string: str,
    rule: Set[str],
) -> Iterator[str]:
    for option in rule:
        if (stripped := string.removeprefix(option)) != string:
            yield stripped
            yield from pref_removed_once_or_more(stripped, rule)


def matches_front_and_back_equal(
    string: str,
    pref_rule: Set[str],
    suff_rule: Set[str],
) -> bool:
    return (
        any(
            string == pref + suff
            for pref in pref_rule
            for suff in suff_rule
        ) or
        any(
            matches_front_and_back_equal(
                stripped,
                pref_rule,
                suff_rule,
            )
            for pref in pref_rule
            for suff in suff_rule
            if len(stripped := (
               string
               .removeprefix(pref)
               .removesuffix(suff)
            )) == len(string) - len(pref) - len(suff)
        )
    )


def matches_special_case(
    example: str,
    rule_42: Set[str],
    rule_31: Set[str],
) -> int:
    return any(
        matches_front_and_back_equal(stripped, rule_42, rule_31)
        for stripped in pref_removed_once_or_more(example, rule_42)
    )


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        block_rules, block_examples = f.read().split('\n\n')

    examples = block_examples.splitlines()
    rule_dict = dict(parse_rule(rule) for rule in block_rules.splitlines())
    simple_rule_dict = fully_simplify_rule_dict(rule_dict)

    rule_0 = simple_rule_dict[0]
    answer_1 = sum(1 for example in examples if example in rule_0)
    assert answer_1 == 176
    print(answer_1)

    rule_42 = simple_rule_dict[42]
    rule_31 = simple_rule_dict[31]
    answer_2 = sum(
        1 for example in examples
        if matches_special_case(example, rule_42, rule_31)
    )
    assert answer_2 == 352
    print(answer_2)


if __name__ == "__main__":
    main()
