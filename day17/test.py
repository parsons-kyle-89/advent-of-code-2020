import pytest

from . import main


@pytest.mark.slow
def test_main() -> None:
    main.main()


def test_startup_cube() -> None:
    raw_lattice = ".#.\n..#\n###\n"
    cube = main.parse_initial_state(raw_lattice, 3)

    assert len(main.startup_cube(cube)) == 112


@pytest.mark.slow
def test_startup_hypercube() -> None:
    raw_lattice = ".#.\n..#\n###\n"
    cube = main.parse_initial_state(raw_lattice, 4)

    assert len(main.startup_cube(cube)) == 848
