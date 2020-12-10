from typing import List, Literal, Tuple

import pytest

from . import main


def test_main() -> None:
    main.main()


def test_all_chargers_jolt_diffs() -> None:
    jolts = [
        28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19,
        38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3,
    ]
    jolts.append(0)
    jolts.append(max(jolts) + 3)
    jolt_diffs = main.all_chargers_jolt_diffs(jolts)
    assert jolt_diffs.count(1) == 22
    assert jolt_diffs.count(3) == 10


@pytest.mark.parametrize(
    ["expected", "max_diff", "diffs"],
    (
        (8, 3, (1, 3, 1, 1, 1, 3, 1, 1, 3, 1, 3, 3)),
        (0, 2, (3, 3, 3)),
        (8, 3.1, (1, 3, 1, 1, 1, 3, 1, 1, 3, 1, 3, 3)),
        (2, 4, (2, 2)),
        (19208, 3, (
            1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 1,
            1, 3, 3, 1, 1, 1, 1, 3, 1, 3, 3, 1, 1, 1, 1, 3,
        )),
    )
)
def test_diff_sequences(
    expected: int,
    max_diff: float,
    diffs: Tuple[float, ...],
) -> None:
    assert main.diff_sequences(diffs, max_diff) == expected


@pytest.mark.parametrize(
    ["expected", "diffs"],
    (
        (8, [1, 3, 1, 1, 1, 3, 1, 1, 3, 1, 3, 3]),
        (19208, [
            1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 1,
            1, 3, 3, 1, 1, 1, 1, 3, 1, 3, 3, 1, 1, 1, 1, 3,
        ]),
    )
)
def test_diff_sequences_non_rec(
    expected: int,
    diffs: List[Literal[1, 3]],
) -> None:
    assert main.diff_sequences_non_rec(diffs) == expected


@pytest.mark.parametrize(
    ["n", "expected"],
    (
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 4),
        (5, 7),
        (6, 13),
        (7, 24),
        (8, 44),
        (9, 81),
        (10, 149),
        (36, 1132436852),
        (50, 5742568741225),
    )
)
def test_tribonacci(n: int, expected: int) -> None:
    assert main.tribonacci(n) == expected
