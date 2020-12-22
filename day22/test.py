import pytest

from . import main


@pytest.mark.slow
def test_main() -> None:
    main.main()


def test_score_deck() -> None:
    deck = (3, 2, 10, 6, 8, 5, 9, 4, 7, 1)
    assert main.score_deck(deck) == 306


def test_Combat() -> None:
    deck_1 = (9, 2, 6, 3, 1)
    deck_2 = (5, 8, 4, 7, 10)
    res_1, res_2 = main.combat(deck_1, deck_2)
    assert res_1 == ()
    assert res_2 == (3, 2, 10, 6, 8, 5, 9, 4, 7, 1)


def test_recursive_combat() -> None:
    deck_1 = (9, 2, 6, 3, 1)
    deck_2 = (5, 8, 4, 7, 10)
    end_state, res_1, res_2 = main.recursive_combat(deck_1, deck_2)
    assert end_state is main.EndState.TWO_WON
    assert res_1 == ()
    assert res_2 == (7, 5, 6, 2, 4, 1, 10, 8, 9, 3)
