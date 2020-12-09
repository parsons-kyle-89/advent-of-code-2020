from . import main


def test_main() -> None:
    main.main()


def test_first_invalid() -> None:
    input_numbers = [
        35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102,
        117, 150, 182, 127, 219, 299, 277, 309, 576,
    ]
    assert main.first_invalid(input_numbers, 5) == 127
