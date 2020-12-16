import pytest

from . import main


def test_main() -> None:
    main.main()


@pytest.mark.parametrize(
    ["ticket", "expected"],
    (
        ([7, 3, 47], True),
        ([40, 4, 50], False),
        ([55, 2, 20], False),
        ([38, 6, 12], False),
    )
)
def test_is_valid(ticket: main.Ticket, expected: bool) -> None:
    rules = [
        main.Rule.from_str('class: 1-3 or 5-7'),
        main.Rule.from_str('row: 6-11 or 33-44'),
        main.Rule.from_str('seat: 13-40 or 45-50'),
    ]

    assert main.is_valid(ticket, rules) == expected


def test_deduce() -> None:
    rules = [
        main.Rule.from_str('class: 0-1 or 4-19'),
        main.Rule.from_str('row: 0-5 or 8-19'),
        main.Rule.from_str('seat: 0-13 or 16-19'),
    ]
    tickets = [
        [11, 12, 13],
        [3, 9, 18],
        [15, 1, 5],
        [5, 14, 9],
    ]
    expected = {0: 'row', 1: 'class', 2: 'seat'}
    assert main.deduce(tickets, rules) == expected
