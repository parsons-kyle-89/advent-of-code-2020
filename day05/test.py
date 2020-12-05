import pytest

from . import main


def test_main() -> None:
    main.main()


@pytest.mark.parametrize(
    ['boarding_id', 'expected'],
    (
        ('BFFFBBFRRR', 567),
        ('FFFBBBFRRR', 119),
        ('BBFFBBFRLL', 820),
    )
)
def test_decode_boarding_id(boarding_id: str, expected: int) -> None:
    assert main.decode_boarding_id(boarding_id) == expected
