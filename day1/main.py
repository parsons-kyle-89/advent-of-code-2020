import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        expenses = [int(line) for line in f.readlines()]

    products = [
        ex1 * ex2
        for i, ex1 in enumerate(expenses)
        for ex2 in expenses[i + 1:]
        if ex1 + ex2 == 2020
    ]

    assert len(products) == 1
    answer_1 = products[0]
    print(answer_1)

    products_2 = [
        ex1 * ex2 * ex3
        for i, ex1 in enumerate(expenses)
        for j, ex2 in enumerate(expenses[i + 1:])
        for ex3 in expenses[j + 1:]
        if ex1 + ex2 + ex3 == 2020
    ]

    assert len(products_2) == 1
    answer_2 = products_2[0]
    print(answer_2)


if __name__ == '__main__':
    main()
