from . import main


def test_main() -> None:
    main.main()


def test_next_departure_bus_and_wait() -> None:
    arrival = 939
    buses = [7, 13, 59, 31, 19]
    assert main.next_departure_bus_and_wait(arrival, buses) == (59, 5)


def test_crt() -> None:
    congruences = [
        main.ModularCongruence(0, 7),
        main.ModularCongruence(-1, 13),
        main.ModularCongruence(-4, 59),
        main.ModularCongruence(-6, 31),
        main.ModularCongruence(-7, 19),
    ]
    assert main.crt(congruences) == 1068781
