from dataclasses import dataclass
from enum import auto, Enum
from itertools import product
import os.path
from typing import cast, Dict, Iterator, List, NoReturn, Optional, Sequence, Set, Tuple, TypeVar

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

TileArrangement = List[List[Optional["Tile"]]]
A = TypeVar("A")


class Angle(Enum):
    ID = auto()
    QUARTER = auto()
    HALF = auto()
    THREE_QUARTER = auto()


class Flip(Enum):
    ID = auto()
    FLIP = auto()


class Direction(Enum):
    ABOVE = auto()
    RIGHT = auto()
    BELOW = auto()
    LEFT = auto()


@dataclass(frozen=True)
class Tile:
    tile_id: int
    border_a: str
    border_b: str
    border_c: str
    border_d: str

    def rotate(self, angle: Angle) -> "Tile":
        if angle is Angle.ID:
            return self
        elif angle is Angle.QUARTER:
            return Tile(
                self.tile_id,
                border_a=self.border_d,
                border_b=self.border_a,
                border_c=self.border_b,
                border_d=self.border_c,
            )
        elif angle is Angle.HALF:
            return Tile(
                self.tile_id,
                border_a=self.border_c,
                border_b=self.border_d,
                border_c=self.border_a,
                border_d=self.border_b,
            )
        elif angle is Angle.THREE_QUARTER:
            return Tile(
                self.tile_id,
                border_a=self.border_b,
                border_b=self.border_c,
                border_c=self.border_d,
                border_d=self.border_a,
            )
        absurd: NoReturn = angle
        raise ValueError(f"found absurd with value {absurd}")

    def flip(self, flip: Flip) -> "Tile":
        if flip is Flip.ID:
            return self
        elif flip is Flip.FLIP:
            return Tile(
                self.tile_id,
                border_a=rev_edge(self.border_a),
                border_b=rev_edge(self.border_d),
                border_c=rev_edge(self.border_c),
                border_d=rev_edge(self.border_b),
            )
        absurd: NoReturn = flip
        raise ValueError(f"found absurd with value {absurd}")

    def matches(self, other: "Tile", direction: Direction) -> bool:
        if direction is Direction.ABOVE:
            return self.border_a == rev_edge(other.border_c)
        elif direction is Direction.RIGHT:
            return self.border_b == rev_edge(other.border_d)
        elif direction is Direction.BELOW:
            return self.border_c == rev_edge(other.border_a)
        elif direction is Direction.LEFT:
            return self.border_d == rev_edge(other.border_b)
        absurd: NoReturn = direction
        raise ValueError(f"found absurd with value {absurd}")


def rev_edge(edge: Sequence[str]) -> str:
    return ''.join(reversed(edge))


def parse_tile(raw_tile: str) -> Tile:
    header, *info_rows = raw_tile.split('\n')
    tile_id = int(header.removeprefix('Tile ').removesuffix(':'))
    border_a = info_rows[0]
    border_b = ''.join(row[-1] for row in info_rows)
    border_c = ''.join(reversed(info_rows[-1]))
    border_d = ''.join(row[0] for row in reversed(info_rows))

    len(border_a) == 10
    set(border_a) <= set('#.')
    len(border_b) == 10
    set(border_b) <= set('#.')
    len(border_c) == 10
    set(border_c) <= set('#.')
    len(border_d) == 10
    set(border_d) <= set('#.')

    return Tile(
        tile_id,
        border_a,
        border_b,
        border_c,
        border_d,
    )


def arrangement_is_full(tile_arr: TileArrangement) -> bool:
    return all(all(loc is not None for loc in row) for row in tile_arr)


def next_empty_loc(tile_arr: TileArrangement) -> Tuple[int, int]:
    row_num = min(i for i, row in enumerate(tile_arr) if None in row)
    col_num = min(i for i, loc in enumerate(tile_arr[row_num]) if loc is None)
    return row_num, col_num


def partitions_of_one(seq: List[A]) -> Iterator[Tuple[A, List[A]]]:
    for i in range(len(seq)):
        yield seq[i], seq[:i] + seq[(i+1):]


def set_loc(
    tile: Tile,
    row_num: int,
    col_num: int,
    tile_arr: TileArrangement,
) -> TileArrangement:
    new_arr = [[loc for loc in row] for row in tile_arr]
    new_arr[row_num][col_num] = tile
    return new_arr


def arrange_tiles(
    tiles: List[Tile],
    initial_arr: TileArrangement,
) -> Iterator[List[List[Tile]]]:
    if arrangement_is_full(initial_arr):
        yield cast(List[List[Tile]], initial_arr)
    else:
        row_num, col_num = next_empty_loc(initial_arr)
        for tile, rest_tiles in partitions_of_one(tiles):
            for angle, flip in product(Angle, Flip):
                trans_tile = tile.rotate(angle).flip(flip)
                if row_num > 0:
                    to_the_above = initial_arr[row_num - 1][col_num]
                    assert to_the_above is not None
                    if not trans_tile.matches(to_the_above, Direction.ABOVE):
                        continue
                if col_num > 0:
                    to_the_left = initial_arr[row_num][col_num - 1]
                    assert to_the_left is not None
                    if not trans_tile.matches(to_the_left, Direction.LEFT):
                        continue
                next_arr = set_loc(trans_tile, row_num, col_num, initial_arr)
                print(overview_arr_2(next_arr))
                print()
                yield from arrange_tiles(rest_tiles, next_arr)


def overview_arr_2(arr: TileArrangement) -> str:
    return '\n'.join(
        ''.join(
            '#' if loc is not None else '.'
            for loc in row
        ) for row in arr
    )


def anneal_tiles(tiles: List[Tile]) -> Dict[Tuple[int, int], Tile]:
    arr: Dict[Tuple[int, int], Tile] = {}
    open_locs: Set[Tuple[int, int]] = set()
    tile = tiles.pop()
    _add_tile(tile, (0, 0), arr, open_locs)
    while tiles:
        loc = open_locs.pop()
        for tile, rot, flip in product(tiles, Angle, Flip):
            trans_tile = tile.rotate(rot).flip(flip)
            if _check_loc(trans_tile, loc, arr):
                tiles.remove(tile)
                _add_tile(tile, loc, arr, open_locs)
                break
        else:
            print(overview_arr(arr))
            print()
    return arr


def _check_loc(
    tile: Tile,
    loc: Tuple[int, int],
    arr: Dict[Tuple[int, int], Tile],
) -> bool:
    x, y = loc
    for dx, dy, direction in (
        (0, 1, Direction.RIGHT),
        (0, -1, Direction.LEFT),
        (1, 0, Direction.ABOVE),
        (-1, 0, Direction.BELOW),
    ):
        new_loc = (x + dx, y + dy)
        if (
            (neighbor_tile := arr.get(new_loc)) is not None and
            not tile.matches(neighbor_tile, direction)
        ):
            return False
    return True


def _add_tile(
    tile: Tile,
    loc: Tuple[int, int],
    arr: Dict[Tuple[int, int], Tile],
    open_locs: Set[Tuple[int, int]],
) -> None:
    arr[loc] = tile
    x, y = loc
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        new_loc = (x + dx, y + dy)
        if new_loc not in arr:
            open_locs.add(new_loc)


def overview_arr(arr: Dict[Tuple[int, int], Tile]) -> str:
    x_min = min(p[0] for p in arr)
    x_max = max(p[0] for p in arr)
    y_min = min(p[1] for p in arr)
    y_max = max(p[1] for p in arr)
    return '\n'.join(
        ''.join(
            '#' if (x, y) in arr else '.' 
            for y in range(y_min, y_max + 1)
        ) for x in range(x_min, x_max + 1)
    )


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        tiles = [parse_tile(tile.strip()) for tile in f.read().split('\n\n')]

#     arrangement = anneal_tiles(tiles)
#     print(arrangement)
    side_len = 12
    assert side_len ** 2 == len(tiles)
    initial_arr: TileArrangement = [[None] * side_len] * side_len
    arrangements = list(arrange_tiles(tiles, initial_arr))
    print(len(arrangements))
    arrangement = arrangements[0]
    answer_1 = (
        arrangement[0][0].tile_id *
        arrangement[0][-1].tile_id *
        arrangement[-1][-1].tile_id *
        arrangement[-1][0].tile_id
    )
    print(answer_1)


if __name__ == "__main__":
    main()
