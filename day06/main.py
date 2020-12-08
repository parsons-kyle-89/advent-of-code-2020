import os.path
from string import ascii_lowercase
from typing import Set

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def parse_group_or(record: str) -> Set[str]:
    return set('').union(*(set(form) for form in record.split()))


def parse_group_and(record: str) -> Set[str]:
    return set(ascii_lowercase).intersection(
        *(set(form) for form in record.split()),
    )


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_records = f.read().split('\n\n')

    or_groups = [parse_group_or(record) for record in raw_records]
    answer_1 = sum(len(group) for group in or_groups)
    assert answer_1 == 6768
    print(answer_1)

    and_groups = [parse_group_and(record) for record in raw_records]
    answer_2 = sum(len(group) for group in and_groups)
    assert answer_2 == 3489
    print(answer_2)


if __name__ == "__main__":
    main()
