from collections import defaultdict
from dataclasses import dataclass
from enum import auto, Enum
import os.path
import re
from typing import DefaultDict, Iterable, NoReturn, Set

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


@dataclass(frozen=True)
class Vec:
    __slots__ = ('q', 'r')
    q: int
    r: int

    def __add__(self, other: "Vec") -> "Vec":
        return Vec(self.q + other.q, self.r + other.r)


CARDINALS = {
    'ne': Vec(1, -1),
    'nw': Vec(0, -1),
    'se': Vec(0, 1),
    'sw': Vec(-1, 1),
    'e': Vec(1, 0),
    'w': Vec(-1, 0),
}


def parse_steps(raw_steps: str) -> Vec:
    delimited_steps = re.findall('ne|nw|se|sw|e|w', raw_steps)
    return sum(
        (CARDINALS[raw_step] for raw_step in delimited_steps), Vec(0, 0)
    )


class Tile(Enum):
    WHITE = auto()
    BLACK = auto()


TileArr = DefaultDict[Vec, Tile]


def tiles_from_initial_vecs(vecs: Iterable[Vec]) -> TileArr:
    tile_parities: DefaultDict[Vec, int] = defaultdict(lambda: 0)
    for vec in vecs:
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
        for card in CARDINALS.values()
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
        if 1 <= black_neighbor_count <= 2:
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
        vecs = [parse_steps(raw_steps) for raw_steps in f.readlines()]

    tiles = tiles_from_initial_vecs(vecs)

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
