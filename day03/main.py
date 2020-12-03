from enum import Enum, auto
from functools import reduce
from operator import mul
import os.path
from typing import List, Tuple

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


class Terrain(Enum):
    OPEN = auto()
    TREE = auto()


class Map:
    def __init__(self, map_: List[List[Terrain]]):
        if len(map_) == 0:
            raise ValueError('map_ must have at least 1 row: got 0')
        first_row_len = len(map_[0])
        if not all(len(row) == first_row_len for row in map_):
            raise ValueError('all rows must have the same length')

        self._map = map_
        self._nrows = len(map_)
        self._ncols = first_row_len

    def __getitem__(self, where: Tuple[int, int]) -> Terrain:
        row, col = where
        return self._map[row][col % self._ncols]

    def __len__(self) -> int:
        return self._nrows


def parse_map(raw_map: str) -> Map:
    return Map([parse_row(row) for row in raw_map.split()])


def parse_row(raw_row: str) -> List[Terrain]:
    return [parse_terrain(terrain) for terrain in raw_row]


def parse_terrain(raw_terrain: str) -> Terrain:
    if raw_terrain == '.':
        return Terrain.OPEN
    elif raw_terrain == '#':
        return Terrain.TREE
    raise ValueError(f"raw_terrain should be '.' or '#': got {raw_terrain}")


def sled_at_angle(map_: Map, d_row: int, d_col: int) -> List[Terrain]:
    return [map_[k * d_row, k * d_col] for k in range(len(map_) // d_row)]


def trees_encountered(map_: Map, d_row: int, d_col: int) -> int:
    path = sled_at_angle(map_, d_row, d_col)
    return sum(1 for terrain in path if terrain == Terrain.TREE)


def prod_trees_encountered(map_: Map, slopes: List[Tuple[int, int]]) -> int:
    return reduce(
        mul,
        (trees_encountered(map_, d_row, d_col) for d_row, d_col in slopes),
        1,
    )


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_map = f.read()
    map_ = parse_map(raw_map)

    solution_1 = trees_encountered(map_, 1, 3)
    print(solution_1)

    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    solution_2 = prod_trees_encountered(map_, slopes)
    print(solution_2)


if __name__ == "__main__":
    main()
