from . import main

EXAMPLE_NUMBERS = [
    35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102,
    117, 150, 182, 127, 219, 299, 277, 309, 576,
]


def test_main() -> None:
    main.main()


def test_first_invalid() -> None:
    assert main.first_invalid(EXAMPLE_NUMBERS, 5) == 127


def test_first_vulnerable_stride() -> None:
    assert (
        main.first_vulnerable_stride(EXAMPLE_NUMBERS, 127) == [15, 25, 47, 40]
    )
