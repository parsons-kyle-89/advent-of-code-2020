from functools import lru_cache, reduce
from itertools import accumulate, chain, groupby
from math import sqrt
from operator import mul
import os.path
from typing import cast, Iterable, List, Literal, Tuple

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


A = (19 + 3 * sqrt(33)) ** (1 / 3)
B = (19 - 3 * sqrt(33)) ** (1 / 3)
C = (586 + 102 * sqrt(33)) ** (1 / 3)


def tribonacci(n: int) -> int:
    return int(round(
        (3 * (((1 / 3) * A + (1 / 3) * B + (1 / 3)) ** n) * C) /
        (C ** 2 + 4 - 2 * C)
    ))


def all_chargers_jolt_diffs(jolts: List[int]) -> List[int]:
    sorted_jolts = sorted(jolts)
    return [upper - lower for lower, upper
            in zip(sorted_jolts[:-1], sorted_jolts[1:])]


@lru_cache
def diff_sequences(diffs: Tuple[float, ...], max_diff: float) -> int:
    if not diffs:
        return 1
    max_steps = [
        acc > max_diff for acc in
        accumulate(chain(diffs, [float('inf')]))
    ].index(True)
    return sum(
        diff_sequences(diffs[step:], max_diff)
        for step in range(1, max_steps + 1)
    )


def diff_sequences_non_rec(diffs: Iterable[Literal[1, 3]]) -> int:
    return reduce(
        mul,
        (tribonacci(len(list(g)) + 1) for v, g in groupby(diffs) if v == 1),
        1
    )


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        jolts = [int(j) for j in f.readlines()]

    jolts.append(0)
    jolts.append(max(jolts) + 3)

    jolt_diffs = all_chargers_jolt_diffs(jolts)
    answer_1 = jolt_diffs.count(1) * jolt_diffs.count(3)
    assert answer_1 == 2201
    print(answer_1)

    answer_2 = diff_sequences(tuple(jolt_diffs), 3)
    assert answer_2 == 169255295254528
    print(answer_2)

    assert all(jolt_diff in (1, 3) for jolt_diff in jolt_diffs)
    literal_jolt_diffs = cast(List[Literal[1, 3]], jolt_diffs)
    answer_2_prime = diff_sequences_non_rec(literal_jolt_diffs)
    assert answer_2 == answer_2_prime


if __name__ == "__main__":
    main()
