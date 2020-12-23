from itertools import islice
import os.path
from typing import Generic, Hashable, Iterable, Iterator, List, TypeVar

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

H = TypeVar('H', bound=Hashable)


def mod(a: int, m: int) -> int:
    "a % m but with a codomain of [1..m]"
    return ((a - 1) % m) + 1


class Rosary(Generic[H]):
    def __init__(self, it: Iterable[H]):
        _iter = iter(it)
        first_value = next(_iter)
        self._lookup = {first_value: first_value}
        self._active = first_value
        self.insert(_iter)

    def __str__(self) -> str:
        return (
            '..., ' +
            ', '.join(str(v) for v in islice(self, len(self._lookup))) +
            ', ...'
        )

    def __iter__(self) -> Iterator[H]:
        iter_head = self._active
        while True:
            yield iter_head
            iter_head = self._lookup[iter_head]

    @property
    def active(self) -> H:
        return self._active

    def scan_to(self, to: H) -> None:
        if to not in self._lookup:
            raise ValueError(f"to {to} not in Rosary")
        self._active = to

    def scan_next(self) -> None:
        self._active = self._lookup[self._active]

    def cut(self, length: int) -> List[H]:
        "Cut after active location, tecnically leaks memory but not materially"
        segment = [v for v in islice(self, 1, length + 1)]
        self._lookup[self._active] = self._lookup[segment[-1]]
        return segment

    def insert(self, segment: Iterable[H]) -> None:
        last_value = self._lookup[self._active]
        key = self._active
        for value in segment:
            self._lookup[key] = value
            key = value
        self._lookup[key] = last_value


def cup_game(order: List[int], rounds: int) -> List[int]:
    n_cups = len(order)
    rosary = Rosary(order)
    for _ in range(rounds):
        current_cup = rosary.active
        removed = rosary.cut(3)
        destination_cup = next(
            d for i in range(1, n_cups + 1) if
            (d := mod(current_cup - i, n_cups)) not in removed
        )
        rosary.scan_to(destination_cup)
        rosary.insert(removed)
        rosary.scan_to(current_cup)
        rosary.scan_next()
    rosary.scan_to(1)
    return rosary.cut(n_cups)


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        order = [int(i) for i in f.read().strip()]

    end_order = cup_game(order, 100)
    answer_1 = int(''.join(str(i) for i in end_order[:-1]))
    assert answer_1 == 24798635
    print(answer_1)

    more_order = order + list(range(max(order) + 1, 1_000_001))
    more_end_order = cup_game(more_order, 10_000_000)
    answer_2 = more_end_order[0] * more_end_order[1]
    assert answer_2 == 12757828710
    print(answer_2)


if __name__ == "__main__":
    main()
