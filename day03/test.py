from . import main

RAW_TEST_MAP = """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""".strip()
TEST_MAP = main.parse_map(RAW_TEST_MAP)


def test_main() -> None:
    main.main()


def test_trees_encountered() -> None:
    assert main.trees_encountered(TEST_MAP, 1, 3) == 7


def test_prod_trees_encountered() -> None:
    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    assert main.prod_trees_encountered(TEST_MAP, slopes) == 336
