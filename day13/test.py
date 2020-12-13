from . import main


def test_main() -> None:
    main.main()


def test_next_departure_bus_and_wait() -> None:
    arrival = 939
    buses = [7, 13, 59, 31, 19]
    assert main.next_departure_bus_and_wait(arrival, buses) == (59, 5)
