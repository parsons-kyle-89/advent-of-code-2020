from collections import defaultdict
from dataclasses import dataclass
import os.path
import re
from typing import Dict, Iterable, List, MutableMapping

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


@dataclass(frozen=True)
class Vec:
    __slots__ = ('q', 'r')
    q: int
    r: int

    def __add__(self, other: "Vec") -> "Vec":
        return Vec(self.q + other.q, self.r + other.r)


def parse_steps(raw_steps: str) -> List[Vec]:
    delimited_steps = re.findall('ne|nw|se|sw|e|w', raw_steps)
    return [parse_step(raw_step) for raw_step in delimited_steps]


def parse_step(raw_step: str) -> Vec:
    if raw_step == 'ne':
        vec = Vec(1, -1)
    elif raw_step == 'nw':
        vec = Vec(0, -1)
    elif raw_step == 'se':
        vec = Vec(0, 1)
    elif raw_step == 'sw':
        vec = Vec(-1, 1)
    elif raw_step == 'e':
        vec = Vec(1, 0)
    elif raw_step == 'w':
        vec = Vec(-1, 0)
    else:
        raise ValueError(f"cannot convert str {raw_step} into Step")
    return vec


def reduce_steps(steps: Iterable[Vec]) -> Vec:
    return sum(steps, Vec(0, 0))


def tile_parities_from_steps(tiles: Iterable[Vec]) -> Dict[Vec, int]:
    tile_parities: MutableMapping[Vec, int] = defaultdict(lambda: 0)
    for vec in tiles:
        tile_parities[vec] = (tile_parities[vec] + 1) % 2
    return dict(tile_parities)


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        steps_list = [parse_steps(raw_steps) for raw_steps in f.readlines()]

    tiles = [reduce_steps(steps) for steps in steps_list]
    tile_parities = tile_parities_from_steps(tiles)
    answer_1 = sum(tile_parities.values())
    print(answer_1)


if __name__ == "__main__":
    main()
