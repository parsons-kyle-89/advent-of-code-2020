from itertools import combinations
import os.path
from typing import List

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def solution_1(expenses: List[int]) -> int:
    products = [
        ex1 * ex2
        for ex1, ex2 in combinations(expenses, 2)
        if ex1 + ex2 == 2020
    ]

    assert len(products) == 1
    answer = products[0]
    return answer


def solution_2(expenses: List[int]) -> int:
    products = [
        ex1 * ex2 * ex3
        for ex1, ex2, ex3 in combinations(expenses, 3)
        if ex1 + ex2 + ex3 == 2020
    ]

    assert len(products) == 1
    answer = products[0]
    return answer


def main():
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        expenses = [int(line) for line in f.readlines()]

    print(solution_1(expenses))
    print(solution_2(expenses))


if __name__ == '__main__':
    main()
