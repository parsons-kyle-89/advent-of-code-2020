from typing import DefaultDict, Generator

import pytest

from . import main


@pytest.mark.slow
def test_main() -> None:
    main.main()


def test_parse_tiles() -> None:
    assert main.parse_steps('esenee') == main.Vec(3, 0)


def test_tile_parities() -> None:
    raw_tiles = [
        'sesenwnenenewseeswwswswwnenewsewsw',
        'neeenesenwnwwswnenewnwwsewnenwseswesw',
        'seswneswswsenwwnwse',
        'nwnwneseeswswnenewneswwnewseswneseene',
        'swweswneswnenwsewnwneneseenw',
        'eesenwseswswnenwswnwnwsewwnwsene',
        'sewnenenenesenwsewnenwwwse',
        'wenwwweseeeweswwwnwwe',
        'wsweesenenewnwwnwsenewsenwwsesesenwne',
        'neeswseenwwswnwswswnw',
        'nenwswwsewswnenenewsenwsenwnesesenew',
        'enewnwewneswsewnwswenweswnenwsenwsw',
        'sweneswneswneneenwnewenewwneswswnese',
        'swwesenesewenwneswnwwneseswwne',
        'enesenwswwswneneswsenwnewswseenwsese',
        'wnwnesenesenenwwnenwsewesewsesesew',
        'nenewswnwewswnenesenwnesewesw',
        'eneswnwswnwsenenwnwnwwseeswneewsenese',
        'neswnwewnwnwseenwseesewsenwsweewe',
        'wseweeenwnesenwwwswnew',
    ]
    vecs = [main.parse_steps(raw_steps) for raw_steps in raw_tiles]
    tiles = main.tiles_from_initial_vecs(vecs)
    assert main.count_black_tiles(tiles) == 10


@pytest.mark.parametrize(
    ["days", "expected_count"],
    (
        (1, 15),
        (2, 12),
        (3, 25),
        (4, 14),
        (5, 23),
        (6, 28),
        (7, 41),
        (8, 37),
        (9, 49),
        (10, 37),
    )
)
def test_black_tiles_by_day(
    initial_arr: DefaultDict[main.Vec, main.Tile],
    days: int,
    expected_count: int
) -> None:
    tiles = initial_arr
    for _ in range(days):
        tiles = main.next_arrangement(tiles)
    assert main.count_black_tiles(tiles) == expected_count


@pytest.fixture(scope="module")
def initial_arr() -> Generator[DefaultDict[main.Vec, main.Tile], None, None]:
    raw_tiles = [
        'sesenwnenenewseeswwswswwnenewsewsw',
        'neeenesenwnwwswnenewnwwsewnenwseswesw',
        'seswneswswsenwwnwse',
        'nwnwneseeswswnenewneswwnewseswneseene',
        'swweswneswnenwsewnwneneseenw',
        'eesenwseswswnenwswnwnwsewwnwsene',
        'sewnenenenesenwsewnenwwwse',
        'wenwwweseeeweswwwnwwe',
        'wsweesenenewnwwnwsenewsenwwsesesenwne',
        'neeswseenwwswnwswswnw',
        'nenwswwsewswnenenewsenwsenwnesesenew',
        'enewnwewneswsewnwswenweswnenwsenwsw',
        'sweneswneswneneenwnewenewwneswswnese',
        'swwesenesewenwneswnwwneseswwne',
        'enesenwswwswneneswsenwnewswseenwsese',
        'wnwnesenesenenwwnenwsewesewsesesew',
        'nenewswnwewswnenesenwnesewesw',
        'eneswnwswnwsenenwnwnwwseeswneewsenese',
        'neswnwewnwnwseenwseesewsenwsweewe',
        'wseweeenwnesenwwwswnew',
    ]
    vecs = [main.parse_steps(raw_steps) for raw_steps in raw_tiles]
    yield main.tiles_from_initial_vecs(vecs)
