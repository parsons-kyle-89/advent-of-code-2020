import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def decode_boarding_id(boarding_id: str) -> int:
    tr = {
        ord('B'): '1',
        ord('F'): '0',
        ord('R'): '1',
        ord('L'): '0',
    }
    return int(boarding_id.translate(tr), 2)


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        boarding_ids = [
            decode_boarding_id(bid.strip()) for bid in f.readlines()
        ]
    max_id = max(boarding_ids)
    min_id = min(boarding_ids)

    answer_1 = max_id
    assert answer_1 == 989
    print(answer_1)

    missing_ids = set(range(min_id, max_id + 1)) - set(boarding_ids)
    assert len(missing_ids) == 1
    answer_2 = missing_ids.pop()
    assert answer_2 == 548
    print(answer_2)


if __name__ == "__main__":
    main()
