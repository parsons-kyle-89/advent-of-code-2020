from collections import defaultdict
from dataclasses import dataclass
from enum import auto, Enum
import os.path
import re
from typing import DefaultDict, Iterable, Iterator, List, NoReturn, Set

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


@dataclass(frozen=True)
class Vec:
    __slots__ = ('q', 'r')
    q: int
    r: int

    def __add__(self, other: "Vec") -> "Vec":
        return Vec(self.q + other.q, self.r + other.r)

    @staticmethod
    def cardinals() -> "Iterator[Vec]":
        yield from iter([
            Vec(0, -1), Vec(1, -1), Vec(1, 0),
            Vec(0, 1), Vec(-1, 1), Vec(-1, 0),
        ])


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


class Tile(Enum):
    WHITE = auto()
    BLACK = auto()


TileArr = DefaultDict[Vec, Tile]


def tiles_from_steps(tiles: Iterable[Vec]) -> TileArr:
    tile_parities: DefaultDict[Vec, int] = defaultdict(lambda: 0)
    for vec in tiles:
        tile_parities[vec] = (tile_parities[vec] + 1) % 2
    return defaultdict(lambda: Tile.WHITE, {
        vec: Tile.WHITE if parity == 0 else Tile.BLACK
        for vec, parity in tile_parities.items()
    })


def count_black_tiles(tiles: TileArr) -> int:
    return sum(1 for tile in tiles.values() if tile is Tile.BLACK)


def next_arrangement(tile_arr: TileArr) -> TileArr:
    shifts = [
        defaultdict(lambda: Tile.WHITE, {
            vec + card: tile for vec, tile in tile_arr.items()
        })
        for card in Vec.cardinals()
    ]
    no_vecs: Set[Vec] = set()
    black_neighbor_counts = defaultdict(lambda: 0, {
        vec: [shift[vec] for shift in shifts].count(Tile.BLACK)
        for vec in no_vecs.union(*shifts)
    })
    return defaultdict(lambda: Tile.WHITE, {
        vec: next_tile(tile_arr[vec], black_neighbor_counts[vec])
        for vec in no_vecs.union(tile_arr, black_neighbor_counts)
    })


def next_tile(tile: Tile, black_neighbor_count: int) -> Tile:
    if tile is Tile.BLACK:
        if black_neighbor_count in [1, 2]:
            return Tile.BLACK
        else:
            return Tile.WHITE
    elif tile is Tile.WHITE:
        if black_neighbor_count == 2:
            return Tile.BLACK
        else:
            return Tile.WHITE
    absurd: NoReturn = tile
    raise ValueError(f"found absurd with value {absurd}")


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        steps_list = [parse_steps(raw_steps) for raw_steps in f.readlines()]

    duped_tiles = [reduce_steps(steps) for steps in steps_list]
    tiles = tiles_from_steps(duped_tiles)

    answer_1 = count_black_tiles(tiles)
    assert answer_1 == 232
    print(answer_1)

    for _ in range(100):
        tiles = next_arrangement(tiles)
    answer_2 = count_black_tiles(tiles)
    assert answer_2 == 3519
    print(answer_2)


if __name__ == "__main__":
    main()
