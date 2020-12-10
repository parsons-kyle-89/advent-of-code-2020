from functools import lru_cache
from itertools import accumulate, chain
import os.path
from typing import List, Tuple

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def all_chargers_jolt_diffs(jolts: List[int]) -> List[int]:
    sorted_jolts = sorted(jolts)
    return [upper - lower for lower, upper
            in zip(sorted_jolts[:-1], sorted_jolts[1:])]


@lru_cache(maxsize=None)
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


if __name__ == "__main__":
    main()
