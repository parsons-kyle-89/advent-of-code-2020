from dataclasses import dataclass
from itertools import product
import os.path
from typing import Dict, Iterator, Set, Tuple, Union

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


@dataclass(frozen=True)
class RuleRef:
    ref: int

    def __repr__(self) -> str:
        return str(self.ref)


@dataclass(frozen=True)
class BaseRule:
    rule: str

    def __repr__(self) -> str:
        return str(self.rule)


RuleComponent = Union[RuleRef, BaseRule]
SimpleRule = Tuple[RuleComponent, ...]
Rule = Set[SimpleRule]
RuleDictionary = Dict[RuleRef, Rule]


def parse_compound_rule(rule: str) -> Tuple[RuleRef, Rule]:
    this_rule_ref, pipe_delim_rules = rule.split(": ", 1)
    simple_rules = {
        parse_simple_rule(simple_rule)
        for simple_rule in pipe_delim_rules.split(" | ")
    }
    return RuleRef(int(this_rule_ref)), simple_rules


def parse_simple_rule(simple_rule: str) -> SimpleRule:
    return tuple(
        parse_rule_component(rule_component)
        for rule_component in simple_rule.split(' ')
    )


def parse_rule_component(rule_component: str) -> RuleComponent:
    if '"' in rule_component:
        return BaseRule(rule_component.strip('"'))
    return RuleRef(int(rule_component))


def has_refs(rule: Rule) -> bool:
    return any(simple_has_refs(simple_rule) for simple_rule in rule)


def simple_has_refs(simple_rule: SimpleRule) -> bool:
    return any(isinstance(comp, RuleRef) for comp in simple_rule)


def full_simplify_rule_dict(rule_dict: RuleDictionary) -> RuleDictionary:
    while any(has_refs(rule) for rule in rule_dict.values()):
        rule_dict = simplify_rule_dict(rule_dict)
    return rule_dict


def simplify_rule_dict(rule_dict: RuleDictionary) -> RuleDictionary:
    return {
        rule_ref: simplify_rule(rule, rule_dict)
        for rule_ref, rule in rule_dict.items()
    }


def simplify_rule(rule: Rule, rule_dict: RuleDictionary) -> Rule:
    no_rules: Rule = set()
    return no_rules.union(
        *(simplify_simple_rule(simple_rule, rule_dict) for simple_rule in rule)
    )


def simplify_simple_rule(
    simple_rule: SimpleRule,
    rule_dict: RuleDictionary,
) -> Rule:
    no_rules: Rule = set()
    return no_rules.union(
        sum(prod, tuple()) for prod in product(*(
            component_to_rule(comp, rule_dict) for comp in simple_rule
        ))
    )


def component_to_rule(comp: RuleComponent, rule_dict: RuleDictionary) -> Rule:
    return (
        rule_dict[comp]
        if isinstance(comp, RuleRef)
        else {(comp,)}
    )


def flatten_rule(rule: Rule) -> Set[str]:
    return {''.join(map(str, simple_rule)) for simple_rule in rule}


def pref_removed_once_or_more(
    string: str,
    flat_rule: Set[str],
) -> Iterator[str]:
    for rule in flat_rule:
        if (stripped := string.removeprefix(rule)) != string:
            yield stripped
            yield from pref_removed_once_or_more(stripped, flat_rule)


def matches_front_and_back_equal(
    string: str,
    pref_flat_rule: Set[str],
    suff_flat_rule: Set[str],
) -> bool:
    return (
        any(
            string == pref + suff
            for pref in pref_flat_rule
            for suff in suff_flat_rule
        ) or
        any(
            matches_front_and_back_equal(
                stripped,
                pref_flat_rule,
                suff_flat_rule,
            )
            for pref in pref_flat_rule
            for suff in suff_flat_rule
            if len(stripped := (
               string
               .removeprefix(pref)
               .removesuffix(suff)
            )) == len(string) - len(pref) - len(suff)
        )
    )


def matches_special_case(
    example: str,
    flat_rule_42: Set[str],
    flat_rule_31: Set[str],
) -> int:
    return any(
        matches_front_and_back_equal(stripped, flat_rule_42, flat_rule_31)
        for stripped in pref_removed_once_or_more(example, flat_rule_42)
    )


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        block_rules, block_examples = f.read().split('\n\n')

    rule_dict = dict(
        parse_compound_rule(compound_rule)
        for compound_rule in block_rules.splitlines()
    )
    simple_rule_dict = full_simplify_rule_dict(rule_dict)
    flat_rule_0 = flatten_rule(simple_rule_dict[RuleRef(0)])

    examples = block_examples.splitlines()
    answer_1 = sum(
        1 for example in examples if example in flat_rule_0
    )
    assert answer_1 == 176
    print(answer_1)

    flat_rule_42 = flatten_rule(simple_rule_dict[RuleRef(42)])
    flat_rule_31 = flatten_rule(simple_rule_dict[RuleRef(31)])
    answer_2 = sum(
        1 for example in examples
        if matches_special_case(example, flat_rule_42, flat_rule_31)
    )
    assert answer_2 == 352
    print(answer_2)


if __name__ == "__main__":
    main()
