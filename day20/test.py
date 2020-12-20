from itertools import product
from typing import Iterator, List, Optional, Tuple

import pytest

from . import main


@pytest.mark.slow
def test_main() -> None:
    main.main()


@pytest.mark.parametrize(
    ["seq", "expected"],
    (
        ([1], [(1, [])]),
        ([1, 2], [(1, [2]), (2, [1])]),
        ([1, 2, 3], [(1, [2, 3]), (2, [1, 3]), (3, [1, 2])]),
    )
)
def test_partitions_of_one(
    seq: List[int],
    expected: List[Tuple[int, List[int]]],
) -> None:
    assert list(main.partitions_of_one(seq)) == expected


def test_strip_border() -> None:
    img = (
        "abc\n"
        "def\n"
        "ghi"
    )
    assert main.strip_border(img) == "e"


def test_arrange_tiles(test_tiles: List[main.Tile]) -> None:
    initial_arr: List[List[Optional[main.Tile]]] = [[None] * 3] * 3
    arrangements = list(main.arrange_tiles(test_tiles, initial_arr))
    assert len(arrangements) == 8
    assert all((
        arrangement[0][0].tile_id *
        arrangement[0][-1].tile_id *
        arrangement[-1][-1].tile_id *
        arrangement[-1][0].tile_id
        ) == 20899048083289
        for arrangement in arrangements
    )


def test_make_image(test_tiles: List[main.Tile]) -> None:
    expected_image = (
        ".#.#..#.##...#.##..#####\n"
        "###....#.#....#..#......\n"
        "##.##.###.#.#..######...\n"
        "###.#####...#.#####.#..#\n"
        "##.#....#.##.####...#.##\n"
        "...########.#....#####.#\n"
        "....#..#...##..#.#.###..\n"
        ".####...#..#.....#......\n"
        "#..#.##..#..###.#.##....\n"
        "#.####..#.####.#.#.###..\n"
        "###.#.#...#.######.#..##\n"
        "#.####....##..########.#\n"
        "##..##.#...#...#.#.#.#..\n"
        "...#..#..#.#.##..###.###\n"
        ".#.#....#.##.#...###.##.\n"
        "###.#...#..#.##.######..\n"
        ".#.#.###.##.##.#..#.##..\n"
        ".####.###.#...###.#..#.#\n"
        "..#.#..#..#.#.#.####.###\n"
        "#..####...#.#.#.###.###.\n"
        "#####..#####...###....##\n"
        "#.##..#..#...#..####...#\n"
        ".#.###..##..##..####.##.\n"
        "...###...##...#...#..###\n"
    ).strip()

    initial_arr: List[List[Optional[main.Tile]]] = [[None] * 3] * 3
    arrangement = next(main.arrange_tiles(test_tiles, initial_arr))
    img = main.make_image(arrangement)
    assert any(
        main.flip_image(main.rotate_image(img, angle), flip) == expected_image
        for angle, flip in product(main.Angle, main.Flip)
    )


def test_highlight_image() -> None:
    image = (
        ".#.#..#.##...#.##..#####\n"
        "###....#.#....#..#......\n"
        "##.##.###.#.#..######...\n"
        "###.#####...#.#####.#..#\n"
        "##.#....#.##.####...#.##\n"
        "...########.#....#####.#\n"
        "....#..#...##..#.#.###..\n"
        ".####...#..#.....#......\n"
        "#..#.##..#..###.#.##....\n"
        "#.####..#.####.#.#.###..\n"
        "###.#.#...#.######.#..##\n"
        "#.####....##..########.#\n"
        "##..##.#...#...#.#.#.#..\n"
        "...#..#..#.#.##..###.###\n"
        ".#.#....#.##.#...###.##.\n"
        "###.#...#..#.##.######..\n"
        ".#.#.###.##.##.#..#.##..\n"
        ".####.###.#...###.#..#.#\n"
        "..#.#..#..#.#.#.####.###\n"
        "#..####...#.#.#.###.###.\n"
        "#####..#####...###....##\n"
        "#.##..#..#...#..####...#\n"
        ".#.###..##..##..####.##.\n"
        "...###...##...#...#..###\n"
    ).strip()
    highlighted_image = main.highlight_in_any_orientation(
        image, main.sea_monster_pattern(), '0'
    )
    assert highlighted_image.count('#') == 273


@pytest.fixture
def test_tiles() -> Iterator[List[main.Tile]]:
    raw_tiles = (
        "Tile 2311:\n"
        "..##.#..#.\n"
        "##..#.....\n"
        "#...##..#.\n"
        "####.#...#\n"
        "##.##.###.\n"
        "##...#.###\n"
        ".#.#.#..##\n"
        "..#....#..\n"
        "###...#.#.\n"
        "..###..###\n"
        "\n"
        "Tile 1951:\n"
        "#.##...##.\n"
        "#.####...#\n"
        ".....#..##\n"
        "#...######\n"
        ".##.#....#\n"
        ".###.#####\n"
        "###.##.##.\n"
        ".###....#.\n"
        "..#.#..#.#\n"
        "#...##.#..\n"
        "\n"
        "Tile 1171:\n"
        "####...##.\n"
        "#..##.#..#\n"
        "##.#..#.#.\n"
        ".###.####.\n"
        "..###.####\n"
        ".##....##.\n"
        ".#...####.\n"
        "#.##.####.\n"
        "####..#...\n"
        ".....##...\n"
        "\n"
        "Tile 1427:\n"
        "###.##.#..\n"
        ".#..#.##..\n"
        ".#.##.#..#\n"
        "#.#.#.##.#\n"
        "....#...##\n"
        "...##..##.\n"
        "...#.#####\n"
        ".#.####.#.\n"
        "..#..###.#\n"
        "..##.#..#.\n"
        "\n"
        "Tile 1489:\n"
        "##.#.#....\n"
        "..##...#..\n"
        ".##..##...\n"
        "..#...#...\n"
        "#####...#.\n"
        "#..#.#.#.#\n"
        "...#.#.#..\n"
        "##.#...##.\n"
        "..##.##.##\n"
        "###.##.#..\n"
        "\n"
        "Tile 2473:\n"
        "#....####.\n"
        "#..#.##...\n"
        "#.##..#...\n"
        "######.#.#\n"
        ".#...#.#.#\n"
        ".#########\n"
        ".###.#..#.\n"
        "########.#\n"
        "##...##.#.\n"
        "..###.#.#.\n"
        "\n"
        "Tile 2971:\n"
        "..#.#....#\n"
        "#...###...\n"
        "#.#.###...\n"
        "##.##..#..\n"
        ".#####..##\n"
        ".#..####.#\n"
        "#..#.#..#.\n"
        "..####.###\n"
        "..#.#.###.\n"
        "...#.#.#.#\n"
        "\n"
        "Tile 2729:\n"
        "...#.#.#.#\n"
        "####.#....\n"
        "..#.#.....\n"
        "....#..#.#\n"
        ".##..##.#.\n"
        ".#.####...\n"
        "####.#.#..\n"
        "##.####...\n"
        "##..#.##..\n"
        "#.##...##.\n"
        "\n"
        "Tile 3079:\n"
        "#.#.#####.\n"
        ".#..######\n"
        "..#.......\n"
        "######....\n"
        "####.#..#.\n"
        ".#...#.##.\n"
        "#.#####.##\n"
        "..#.###...\n"
        "..#.......\n"
        "..#.###...\n"
    )
    yield [main.parse_tile(tile.strip()) for tile in raw_tiles.split('\n\n')]
