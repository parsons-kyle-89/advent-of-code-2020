from collections import defaultdict
from dataclasses import dataclass
from itertools import repeat
import os.path
from typing import (
    Callable, cast, DefaultDict, Dict, Generic, Iterable, Iterator,
    Mapping, NewType, Set, Tuple, TypeVar,
)

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

A = TypeVar('A')
BagType = NewType('BagType', str)


def takeuntil_stable(it: Iterable[A]) -> Iterator[A]:
    iterator = iter(it)
    try:
        this_value = next(iterator)
    except StopIteration:
        return None
    yield this_value

    while True:
        try:
            next_value = next(iterator)
        except StopIteration:
            break

        if this_value == next_value:
            break
        yield next_value

        this_value = next_value


def iterate_func(func: Callable[[A], A], value: A) -> Iterator[A]:
    while True:
        yield value
        value = func(value)


def sum_dicts(
    dicts: Iterable[Mapping[A, int]],
    weights: Iterable[int] = repeat(1),
) -> Dict[A, int]:
    ret: DefaultDict[A, int] = defaultdict(lambda: 0)
    for d, w in zip(dicts, weights):
        for k, v in d.items():
            ret[k] += v * w
    return dict(ret)


@dataclass
class Node(Generic[A]):
    name: A
    out_edges: Dict[A, int]
    in_edges: Set[A]

    def register_in_edge(self, in_node: A) -> None:
        self.in_edges.add(in_node)


class WeightedDigraph(Generic[A]):
    def __init__(self, nodes: Iterable[Node[A]]) -> None:
        self._nodes = {node.name: node for node in nodes}
        for node_name, node in self._nodes.items():
            for out_node_name in node.out_edges.keys():
                self._nodes[out_node_name].register_in_edge(node_name)

    def in_set(self, names: Set[A]) -> Set[A]:
        in_sets = takeuntil_stable(
            iterate_func(
                lambda names_: cast(Set[A], set()).union(
                    *(self._nodes[name].in_edges for name in names_)
                ),
                names
            )
        )
        return cast(Set[A], set()).union(*in_sets)

    def weighted_out_set(
        self, weighted_names: Mapping[A, int],
    ) -> Dict[A, int]:
        out_sets = takeuntil_stable(
            iterate_func(
                lambda weighted_names_: sum_dicts(
                    (
                        self._nodes[name].out_edges
                        for name in weighted_names_.keys()
                    ),
                    weighted_names_.values()
                ),
                weighted_names
            )
        )
        return sum_dicts(out_sets)


def parse_bag_rule(bag_rule: str) -> Node[BagType]:
    raw_bag_type, raw_out_edges = bag_rule.split(' bags contain ', 1)
    bag_type = BagType(raw_bag_type)
    parsed_out_edges = [
        _parse_out_edge(raw_out_edge)
        for raw_out_edge in raw_out_edges.strip('.').split(', ')
    ]
    out_edges = {
        bag_type: count
        for bag_type, count in parsed_out_edges
        if count != 0
    }
    return Node(bag_type, out_edges, set())


def _parse_out_edge(raw_out_edge: str) -> Tuple[BagType, int]:
    stripped_raw_sub_rule = (
        raw_out_edge.removesuffix(' bag').removesuffix(' bags')
    )
    raw_count, raw_bag_type = stripped_raw_sub_rule.split(' ', 1)
    bag_type = BagType(raw_bag_type)
    count = _parse_count(raw_count)
    return bag_type, count


def _parse_count(raw_count: str) -> int:
    if raw_count == 'no':
        return 0
    return int(raw_count)


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        bag_nodes = [
            parse_bag_rule(raw_rule.strip()) for raw_rule in f.readlines()
        ]

    bag_rule_digraph = WeightedDigraph(bag_nodes)
    my_bag = BagType('shiny gold')

    print(len(bag_rule_digraph.in_set({my_bag})) - 1)

    out_set = bag_rule_digraph.weighted_out_set({my_bag: 1})
    print(sum(out_set.values()) - 1)


if __name__ == "__main__":
    main()
