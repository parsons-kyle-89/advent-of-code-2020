import pytest

from . import main


def test_main() -> None:
    main.main()


@pytest.mark.parametrize(
    ['record', 'num_yes'],

    (
        ('abc', 3),
        ('a\nb\nc', 3),
        ('ab\nac', 3),
        ('a\na\na\na', 1),
        ('b', 1),
    )
)
def test_parse_group_or(record: str, num_yes: int) -> None:
    assert len(main.parse_group_or(record)) == num_yes


@pytest.mark.parametrize(
    ['record', 'num_yes'],

    (
        ('abc', 3),
        ('a\nb\nc', 0),
        ('ab\nac', 1),
        ('a\na\na\na', 1),
        ('b', 1),
    )
)
def test_parse_group_and(record: str, num_yes: int) -> None:
    assert len(main.parse_group_and(record)) == num_yes
