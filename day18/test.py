import pytest

from . import main


def test_main() -> None:
    main.main()


@pytest.mark.parametrize(
    ["eq", "expected"],
    (
        ('1 + 2 * 3 + 4 * 5 + 6', 71),
        ('1 + (2 * 3) + (4 * (5 + 6))', 51),
        ('2 * 3 + (4 * 5)', 26),
        ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437),
        ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240),
        ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632),
    )
)
def test_new_math(eq: str, expected: int) -> None:
    assert main.new_math(eq) == expected


@pytest.mark.parametrize(
    ["eq", "expected"],
    (
        ('1 + 2 * 3 + 4 * 5 + 6', 231),
        ('1 + (2 * 3) + (4 * (5 + 6))', 51),
        ('2 * 3 + (4 * 5)', 46),
        ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 1445),
        ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 669060),
        ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 23340),
    )
)
def test_newer_math(eq: str, expected: int) -> None:
    assert main.newer_math(eq) == expected
