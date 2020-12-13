from operator import itemgetter
import os.path
from typing import Iterable, Tuple

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def next_departure_bus_and_wait(
    arrival: int, buses: Iterable[int]
) -> Tuple[int, int]:
    return min(
        ((bus, -arrival % bus) for bus in buses), key=itemgetter(1)
    )


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        arrival = int(f.readline().strip())
        buses = [int(b) for b in f.readline().split(',') if b != 'x']

    bus, wait = next_departure_bus_and_wait(arrival, buses)
    answer_1 = bus * wait
    assert answer_1 == 2545
    print(answer_1)


if __name__ == "__main__":
    main()
