from functools import reduce
from itertools import accumulate
import os.path
from typing import Callable

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

MODULUS = 20201227
SUBJECT_NUMBER = 7


def mod_mul(factor: int, modulus: int) -> Callable[[int, int], int]:
    def mod_multiplier(acc: int, ignored: int) -> int:
        return (acc * factor) % modulus
    return mod_multiplier


def pubkey(
    loop_size: int,
    subject_number: int = SUBJECT_NUMBER,
    modulus: int = MODULUS,
) -> int:
    accumulator = mod_mul(subject_number, modulus)
    return reduce(accumulator, range(loop_size), 1)


def decode_pubkey(
    pubkey: int,
    subject_number: int = SUBJECT_NUMBER,
    modulus: int = MODULUS,
) -> int:
    accumulator = mod_mul(subject_number, modulus)
    return next(
        loop_size
        for loop_size, key in zip(
            range(modulus),
            accumulate(range(modulus), accumulator, initial=1)
        ) if key == pubkey
    )


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        card_pubkey, door_pubkey = (int(line) for line in f.readlines())

    card_loop_size = decode_pubkey(card_pubkey)
    answer_1 = pubkey(card_loop_size, subject_number=door_pubkey)
    assert answer_1 == 181800
    print(answer_1)


if __name__ == "__main__":
    main()
