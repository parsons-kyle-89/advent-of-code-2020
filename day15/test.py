from typing import List

import pytest

from . import main


@pytest.mark.slow
def test_main() -> None:
    main.main()


@pytest.mark.parametrize(
    ["starting_numbers", "expected_number"],
    (
        ([1, 3, 2], 1),
        ([2, 1, 3], 10),
        ([1, 2, 3], 27),
        ([2, 3, 1], 78),
        ([3, 2, 1], 438),
        ([3, 1, 2], 1836),
    )
)
def test_game(starting_numbers: List[int], expected_number: int) -> None:
    game = main.run_game(starting_numbers, 2020)
    assert game.last_number == expected_number
