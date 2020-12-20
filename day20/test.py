from typing import List, Tuple

import pytest

from . import main


def test_main() -> None:
    main.main()


@pytest.mark.parametrize(
    ["seq", "expected"],
    (
        ([1], [(1, [])]),
        ([1, 2], [(1, [2]), (2, [1])]),
        ([1, 2, 3], [(1, [2, 3]), (2, [1, 3]), (3, [1, 2])]),
    )
)
def test_partitions_of_one(
    seq: List[int],
    expected: List[Tuple[int, List[int]]],
) -> None:
    assert list(main.partitions_of_one(seq)) == expected


def test_strip_border() -> None:
    img = (
        "abc\n"
        "def\n"
        "ghi"
    )
    assert main.strip_border(img) == "e"
