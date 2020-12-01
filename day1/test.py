from main import solution_1, solution_2


EXPENSES = [
    1721,
    979,
    366,
    299,
    675,
    1456,
]



def test_solution_1() -> None:
    assert solution_1(EXPENSES) == 514579


def test_solution_2() -> None:
    assert solution_2(EXPENSES) == 241861950
