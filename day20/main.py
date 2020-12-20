from collections import defaultdict
from dataclasses import dataclass
from enum import auto, Enum
from functools import reduce
from itertools import product
import os.path
from typing import (
    cast, Dict, Iterator, List, MutableMapping, NoReturn, Optional, Protocol,
    Sequence, Tuple, TypeVar
)

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

TileArrangement = List[List[Optional["Tile"]]]
A = TypeVar("A")


def rev_str(edge: Sequence[str]) -> str:
    return ''.join(reversed(edge))


def cols(image: str) -> List[str]:
    return [''.join(col) for col in zip(*image.splitlines())]


def rows(image: str) -> List[str]:
    return image.splitlines()


class Transformation(Protocol):
    def transform(self, image: str) -> str:
        ...


class Angle(Enum):
    ID = auto()
    QUARTER = auto()
    HALF = auto()
    THREE_QUARTER = auto()

    def transform(self, image: str) -> str:
        if self is Angle.ID:
            return image
        elif self is Angle.QUARTER:
            return '\n'.join(
                rev_str(col)
                for col in cols(image)
            )
        elif self is Angle.HALF:
            return '\n'.join(
                rev_str(row)
                for row in reversed(rows(image))
            )
        elif self is Angle.THREE_QUARTER:
            return '\n'.join(
                col
                for col in reversed(cols(image))
            )
        absurd: NoReturn = self
        raise ValueError(f"found absurd with value {absurd}")


class Flip(Enum):
    ID = auto()
    FLIP = auto()

    def transform(self, image: str) -> str:
        if self is Flip.ID:
            return image
        elif self is Flip.FLIP:
            return '\n'.join(rev_str(row) for row in image.splitlines())
        absurd: NoReturn = self
        raise ValueError(f"found absurd with value {absurd}")


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
    image: str
    transformations: List[Transformation]

    def rotate(self, angle: Angle) -> "Tile":
        transformations = self.transformations + [angle]
        if angle is Angle.ID:
            return self
        elif angle is Angle.QUARTER:
            return Tile(
                self.tile_id,
                border_a=self.border_d,
                border_b=self.border_a,
                border_c=self.border_b,
                border_d=self.border_c,
                image=self.image,
                transformations=transformations,
            )
        elif angle is Angle.HALF:
            return Tile(
                self.tile_id,
                border_a=self.border_c,
                border_b=self.border_d,
                border_c=self.border_a,
                border_d=self.border_b,
                image=self.image,
                transformations=transformations,
            )
        elif angle is Angle.THREE_QUARTER:
            return Tile(
                self.tile_id,
                border_a=self.border_b,
                border_b=self.border_c,
                border_c=self.border_d,
                border_d=self.border_a,
                image=self.image,
                transformations=transformations,
            )
        absurd: NoReturn = angle
        raise ValueError(f"found absurd with value {absurd}")

    def flip(self, flip: Flip) -> "Tile":
        if flip is Flip.ID:
            return self
        elif flip is Flip.FLIP:
            return Tile(
                self.tile_id,
                border_a=rev_str(self.border_a),
                border_b=rev_str(self.border_d),
                border_c=rev_str(self.border_c),
                border_d=rev_str(self.border_b),
                image=self.image,
                transformations=self.transformations + [flip],
            )
        absurd: NoReturn = flip
        raise ValueError(f"found absurd with value {absurd}")

    def matches(self, other: "Tile", direction: Direction) -> bool:
        if direction is Direction.ABOVE:
            return self.border_a == rev_str(other.border_c)
        elif direction is Direction.RIGHT:
            return self.border_b == rev_str(other.border_d)
        elif direction is Direction.BELOW:
            return self.border_c == rev_str(other.border_a)
        elif direction is Direction.LEFT:
            return self.border_d == rev_str(other.border_b)
        absurd: NoReturn = direction
        raise ValueError(f"found absurd with value {absurd}")

    def flatten(self) -> "Tile":
        trans_image = reduce(
            lambda img, trans: trans.transform(img),
            self.transformations,
            self.image
        )
        return Tile(
            self.tile_id,
            self.border_a,
            self.border_b,
            self.border_c,
            self.border_d,
            image=trans_image,
            transformations=[],
        )


def parse_tile(raw_tile: str) -> Tile:
    header, *info_rows = raw_tile.split('\n')
    tile_id = int(header.removeprefix('Tile ').removesuffix(':'))
    border_a = info_rows[0]
    border_b = ''.join(row[-1] for row in info_rows)
    border_c = ''.join(reversed(info_rows[-1]))
    border_d = ''.join(row[0] for row in reversed(info_rows))
    image = '\n'.join(info_rows)

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
        image,
        [],
    )


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
                yield from arrange_tiles(rest_tiles, next_arr)


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


def sort_by_edge_match_count(tiles: List[Tile]) -> List[Tile]:
    edge_counts: MutableMapping[str, int] = defaultdict(int)
    for tile in tiles:
        edge_counts[cannonical_edge(tile.border_a)] += 1
        edge_counts[cannonical_edge(tile.border_b)] += 1
        edge_counts[cannonical_edge(tile.border_c)] += 1
        edge_counts[cannonical_edge(tile.border_d)] += 1

    def _edge_counter(tile: Tile) -> int:
        return (
            edge_counts[cannonical_edge(tile.border_a)] +
            edge_counts[cannonical_edge(tile.border_b)] +
            edge_counts[cannonical_edge(tile.border_c)] +
            edge_counts[cannonical_edge(tile.border_d)]
        )
    return sorted(tiles, key=_edge_counter)


def cannonical_edge(edge: str) -> str:
    return min(edge, rev_str(edge))


def make_image(arr: List[List[Tile]]) -> str:
    flat_images = [
        [strip_border(tile.flatten().image) for tile in row] for row in arr
    ]
    return '\n'.join(
        '\n'.join(
            ''.join(rows)
            for rows in zip(*list(block.splitlines() for block in block_row))
        ) for block_row in flat_images
    )


def strip_border(image: str) -> str:
    rows = image.splitlines()
    row_max = len(rows)
    col_max = len(rows[0])
    return '\n'.join(
        ''.join(
            px for col_num, px in enumerate(row)
            if 0 < col_num < col_max - 1
        )
        for row_num, row in enumerate(rows)
        if 0 < row_num < row_max - 1
    )


def highlight_in_any_orientation(
    image: str,
    pattern: Dict[Tuple[int, int], str],
    highlight: str,
) -> str:
    for angle, flip in product(Angle, Flip):
        trans_image = flip.transform(angle.transform(image))
        highlighted_image = highlight_patterns(trans_image, pattern, highlight)
        if trans_image != highlighted_image:
            return highlighted_image
    raise ValueError("No pattern found in any orientation!!")


def highlight_patterns(
    image: str,
    pattern: Dict[Tuple[int, int], str],
    highlight: str,
) -> str:
    image_matrix = [list(row) for row in image.splitlines()]
    for row_num, row in enumerate(image_matrix):
        for col_num, _ in enumerate(row):
            if is_pattern_at(image_matrix, (row_num, col_num), pattern):
                for (d_row, d_col), _ in pattern.items():
                    image_matrix[row_num + d_row][col_num + d_col] = highlight
    return '\n'.join(''.join(row) for row in image_matrix)


def is_pattern_at(
    img_mat: List[List[str]],
    loc: Tuple[int, int],
    pattern: Dict[Tuple[int, int], str],
) -> bool:
    row_num, col_num = loc
    return all(
        get_px(img_mat, row_num + d_row, col_num + d_col) == px
        for (d_row, d_col), px in pattern.items()
    )


def get_px(
    img_mat: List[List[str]],
    row_num: int,
    col_num: int,
) -> Optional[str]:
    if row_num < 0 or row_num >= len(img_mat):
        return None
    row = img_mat[row_num]
    if col_num < 0 or col_num >= len(row):
        return None
    return row[col_num]


def sea_monster_pattern() -> Dict[Tuple[int, int], str]:
    sea_monster_str = (
        "                  # \n"
        "#    ##    ##    ###\n"
        " #  #  #  #  #  #   \n"
    )
    return {
        (row_num, col_num): px
        for row_num, row in enumerate(sea_monster_str.splitlines())
        for col_num, px in enumerate(row)
        if px == '#'
    }


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        tiles = [parse_tile(tile.strip()) for tile in f.read().split('\n\n')]

    sorted_tiles = sort_by_edge_match_count(tiles)
    side_len = 12
    assert side_len ** 2 == len(tiles)
    initial_arr: TileArrangement = [[None] * side_len] * side_len

    arrangement = next(arrange_tiles(sorted_tiles, initial_arr))
    answer_1 = (
        arrangement[0][0].tile_id *
        arrangement[0][-1].tile_id *
        arrangement[-1][-1].tile_id *
        arrangement[-1][0].tile_id
    )
    assert answer_1 == 12519494280967
    print(answer_1)

    image = make_image(arrangement)
    highlighted_image = highlight_in_any_orientation(
        image, sea_monster_pattern(), '\x1b[6;30;42mO\x1b[0m'
    )
    # print(highlighted_image)
    answer_2 = highlighted_image.count('#')
    assert answer_2 == 2442
    print(answer_2)


if __name__ == "__main__":
    main()
