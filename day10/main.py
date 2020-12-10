from functools import lru_cache
import os.path
from typing import List, Literal, Tuple

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

JoltDiff = Literal[1, 3]


def all_chargers_jolt_diffs(jolts: List[int]) -> List[int]:
    sorted_jolts = sorted(jolts)
    return [upper - lower for lower, upper
            in zip(sorted_jolts[:-1], sorted_jolts[1:])]


@lru_cache(maxsize=None)
def charger_sequences(jolt_diffs: Tuple[int, ...]) -> int:
    if len(jolt_diffs) == 0:
        return 1
    elif len(jolt_diffs) == 1:
        return charger_sequences(jolt_diffs[1:])
    elif len(jolt_diffs) == 2:
        a, b, *_ = jolt_diffs
        if a == b == 1:
            return (
                charger_sequences(jolt_diffs[1:]) +
                charger_sequences(jolt_diffs[2:])
            )
        else:
            return charger_sequences(jolt_diffs[1:])
    else:
        a, b, c, *_ = jolt_diffs
        if a == 3 or b == 3:
            return charger_sequences(jolt_diffs[1:])
        elif c == 3:
            return (
                charger_sequences(jolt_diffs[1:]) +
                charger_sequences(jolt_diffs[2:])
            )
        else:
            return (
                charger_sequences(jolt_diffs[1:]) +
                charger_sequences(jolt_diffs[2:]) +
                charger_sequences(jolt_diffs[3:])
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

    answer_2 = charger_sequences(tuple(jolt_diffs))
    assert answer_2 == 169255295254528
    print(answer_2)


if __name__ == "__main__":
    main()
