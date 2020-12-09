from itertools import combinations
import os.path
from typing import List, Optional

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def first_invalid(input_numbers: List[int], lag: int) -> Optional[int]:
    for i, a in enumerate(input_numbers):
        if i < lag:
            continue

        local_preamble = input_numbers[(i - lag):i]
        if a not in {x + y for x, y in combinations(local_preamble, 2)}:
            return a
    return None


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        numbers = [int(line) for line in f.readlines()]

    answer_1 = first_invalid(numbers, 25)
    assert answer_1 == 57195069
    print(answer_1)


if __name__ == "__main__":
    main()
