import pytest

from . import main


@pytest.mark.slow
def test_main() -> None:
    main.main()


def test_next_state() -> None:
    raw_states = [
        (
            "L.LL.LL.LL\n"
            "LLLLLLL.LL\n"
            "L.L.L..L..\n"
            "LLLL.LL.LL\n"
            "L.LL.LL.LL\n"
            "L.LLLLL.LL\n"
            "..L.L.....\n"
            "LLLLLLLLLL\n"
            "L.LLLLLL.L\n"
            "L.LLLLL.LL\n"
        ),
        (
            "#.##.##.##\n"
            "#######.##\n"
            "#.#.#..#..\n"
            "####.##.##\n"
            "#.##.##.##\n"
            "#.#####.##\n"
            "..#.#.....\n"
            "##########\n"
            "#.######.#\n"
            "#.#####.##\n"
        ),
        (
            "#.LL.L#.##\n"
            "#LLLLLL.L#\n"
            "L.L.L..L..\n"
            "#LLL.LL.L#\n"
            "#.LL.LL.LL\n"
            "#.LLLL#.##\n"
            "..L.L.....\n"
            "#LLLLLLLL#\n"
            "#.LLLLLL.L\n"
            "#.#LLLL.##\n"
        ),
        (
            "#.##.L#.##\n"
            "#L###LL.L#\n"
            "L.#.#..#..\n"
            "#L##.##.L#\n"
            "#.##.LL.LL\n"
            "#.###L#.##\n"
            "..#.#.....\n"
            "#L######L#\n"
            "#.LL###L.L\n"
            "#.#L###.##\n"
        ),
        (
            "#.#L.L#.##\n"
            "#LLL#LL.L#\n"
            "L.L.L..#..\n"
            "#LLL.##.L#\n"
            "#.LL.LL.LL\n"
            "#.LL#L#.##\n"
            "..L.L.....\n"
            "#L#LLLL#L#\n"
            "#.LLLLLL.L\n"
            "#.#L#L#.##\n"
        ),
        (
            "#.#L.L#.##\n"
            "#LLL#LL.L#\n"
            "L.#.L..#..\n"
            "#L##.##.L#\n"
            "#.#L.LL.LL\n"
            "#.#L#L#.##\n"
            "..L.L.....\n"
            "#L#L##L#L#\n"
            "#.LLLLLL.L\n"
            "#.#L#L#.##\n"
        )
    ]

    states = [main.StateArrangement.from_raw(raw) for raw in raw_states]
    for st_init, st_next in zip(states[:-1], states[1:]):
        assert st_init.next_state_adjacent() == st_next
    assert states[-1].next_state_adjacent() == states[-1]
    assert states[-1].num_in_state(main.State.Occupied) == 37
