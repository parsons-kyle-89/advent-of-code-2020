from . import main


EXPENSES = [
    1721,
    979,
    366,
    299,
    675,
    1456,
]


def test_main() -> None:
    main.main()


def test_solution_1() -> None:
    assert main.solution_1(EXPENSES) == 514579


def test_solution_2() -> None:
    assert main.solution_2(EXPENSES) == 241861950
