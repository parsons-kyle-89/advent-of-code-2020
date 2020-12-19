from dataclasses import dataclass
import os.path
from typing import Dict, List, Literal, Tuple, Union

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


@dataclass
class RuleRef:
    ref: int


@dataclass
class BaseRule:
    rule: str


RuleComponent = Union[RuleRef, BaseRule]
SimpleRule = List[RuleComponent]
Rule = List[SimpleRule]
RuleDictionary = Dict[RuleRef, Rule]


def parse_compound_rule(rule: str) -> Tuple[RuleRef, Rule]:
    this_rule_ref, pipe_delim_rules = rule.split(": ", 1)
    simple_rules = [
        parse_simple_rule(simple_rule)
        for simple_rule in pipe_delim_rules.split(" | ")
    ]
    return RuleRef(int(this_rule_ref)), Rule(simple_rules)


def parse_simple_rule(simple_rule: str) -> SimpleRule:
    return SimpleRule([
        parse_rule_component(rule_component)
        for rule_component in simple_rule.split(' ')
    ])


def parse_rule_component(rule_component: str) -> RuleComponent:
    if '"' in rule_component:
        return BaseRule(rule_component.strip('"'))
    return RuleRef(int(rule_component))


def has_refs(rule: Rule) -> bool:
    return any(simple_has_refs(simple_rule) for simple_rule in rule)


def simple_has_refs(simple_rule: SimpleRule) -> bool:
    return any(isinstance(comp, RuleRef) for comp in simple_rule)


def simplify_rule_dict(rule_dict: RuleDictionary) -> RuleDictionary:
    return RuleDictionary({
        rule_ref: simplify_rule(rule, rule_dict) 
        for rule_ref, rule in rule_dict.itmes()
    })


def simplify_rule(rule: Rule, rule_dict: RuleDictionary) -> Rule:
    return Rule(
        [simplify_simple_rule(simple_rule, rule_dict) for simple_rule in rule]
    )


def simplify_simple_rule(
    simple_rule: SimpleRule,
    rule_dict: RuleDictionary,
) -> Rule:
    nested_rules = [rule_dict[comp] if isinstance(comp, RuleRef) else [comp] for comp in simple_rule]


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        block_rules, block_examples = f.read().split('\n\n')

    rule_dict = RuleDictionary(dict(
        parse_compound_rule(compound_rule)
        for compound_rule in block_rules.splitlines()
    ))
    examples = block_examples.splitlines()


if __name__ == "__main__":
    main()
