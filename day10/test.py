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
    ["expected", "jolt_diffs"],
    (
        (8, (1, 3, 1, 1, 1, 3, 1, 1, 3, 1, 3, 3)),
        (19208, (
            1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 1,
            1, 3, 3, 1, 1, 1, 1, 3, 1, 3, 3, 1, 1, 1, 1, 3,
        )),
    )
)
def test_charger_sequences(expected: int, jolt_diffs: Tuple[int, ...]) -> None:
    assert main.charger_sequences(jolt_diffs) == expected
