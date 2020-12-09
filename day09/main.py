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


def first_vulnerable_stride(
    input_numbers: List[int],
    target: int,
) -> Optional[List[int]]:
    for stride_length in range(2, len(input_numbers)):
        this_stride = vulnerable_stride_of_length(
            input_numbers, target, stride_length
        )
        if this_stride is not None:
            return this_stride
    return None


def vulnerable_stride_of_length(
    input_numbers: List[int],
    target: int,
    stride_length: int,
) -> Optional[List[int]]:
    for i in range(len(input_numbers) - stride_length):
        stride = input_numbers[i:(i + stride_length)]
        if sum(stride) == target:
            return stride
    return None


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        numbers = [int(line) for line in f.readlines()]

    answer_1 = first_invalid(numbers, 25)
    assert answer_1 == 57195069
    print(answer_1)

    vulnerable_stride = first_vulnerable_stride(numbers, answer_1)
    assert vulnerable_stride is not None
    assert len(vulnerable_stride) >= 2
    answer_2 = min(vulnerable_stride) + max(vulnerable_stride)
    assert answer_2 == 7409241
    print(answer_2)


if __name__ == "__main__":
    main()
