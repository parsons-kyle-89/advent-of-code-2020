from typing import Tuple

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
