from typing import List

import pytest

from . import main


@pytest.mark.slow
def test_main() -> None:
    main.main()


@pytest.mark.parametrize(
    ["num_moves", "expected"],
    (
        (10, [9, 2, 6, 5, 8, 3, 7, 4, 1]),
        (100, [6, 7, 3, 8, 4, 5, 2, 9, 1]),
    )
)
def test_moves(num_moves: int, expected: List[int]) -> None:
    order = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    assert main.cup_game(order, num_moves) == expected
