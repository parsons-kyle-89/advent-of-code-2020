from . import main


def test_main() -> None:
    main.main()


def test_parse_tiles() -> None:
    raw_steps = 'esenee'
    steps = main.parse_steps(raw_steps)
    tile = main.reduce_steps(steps)
    assert tile == main.Vec(3, 0)


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
    steps_list = [main.parse_steps(raw_steps) for raw_steps in raw_tiles]
    tiles = [main.reduce_steps(steps) for steps in steps_list]
    tile_parities = main.tile_parities_from_steps(tiles)
    assert sum(tile_parities.values()) == 10
