from enum import auto, Enum
import os.path
from typing import NoReturn, Sequence, Set, Tuple

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

Deck = Tuple[int, ...]


def parse_deck(raw_deck: str) -> Deck:
    header, *cards = raw_deck.splitlines()
    return tuple(int(card) for card in cards)


def score_deck(deck: Sequence[int]) -> int:
    return sum(v * p for v, p in zip(deck, range(len(deck), 0, -1)))


def combat(deck_1: Deck, deck_2: Deck) -> Tuple[Deck, Deck]:
    while deck_1 and deck_2:
        card_1, *_rest_1 = deck_1
        card_2, *_rest_2 = deck_2
        rest_1, rest_2 = tuple(_rest_1), tuple(_rest_2)

        if card_1 > card_2:
            deck_1 = rest_1 + (card_1, card_2)
            deck_2 = rest_2
        else:
            deck_1 = rest_1
            deck_2 = rest_2 + (card_2, card_1)

    return deck_1, deck_2


class EndState(Enum):
    ONE_WON = auto()
    TWO_WON = auto()


def recursive_combat(
    deck_1: Deck,
    deck_2: Deck,
) -> Tuple[EndState, Deck, Deck]:
    previous_states: Set[Tuple[Deck, Deck]] = set()
    while True:
        if (deck_1, deck_2) in previous_states:
            return EndState.ONE_WON, deck_1, deck_2
        previous_states.add((deck_1, deck_2))

        card_1, *_rest_1 = deck_1
        card_2, *_rest_2 = deck_2
        rest_1, rest_2 = tuple(_rest_1), tuple(_rest_2)

        if card_1 <= len(rest_1) and card_2 <= len(rest_2):
            round_winner, _, _ = \
                recursive_combat(rest_1[:card_1], rest_2[:card_2])
        else:
            round_winner = \
                EndState.ONE_WON if card_1 > card_2 else EndState.TWO_WON

        if round_winner is EndState.ONE_WON:
            deck_1 = rest_1 + (card_1, card_2)
            deck_2 = rest_2
        elif round_winner is EndState.TWO_WON:
            deck_1 = rest_1
            deck_2 = rest_2 + (card_2, card_1)
        else:
            absurd: NoReturn = round_winner
            raise ValueError(f"reached absurd with value {absurd}")

        if not deck_2:
            return EndState.ONE_WON, deck_1, deck_2
        if not deck_1:
            return EndState.TWO_WON, deck_1, deck_2


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_deck_1, raw_deck_2 = f.read().split('\n\n')

    deck_1 = parse_deck(raw_deck_1)
    deck_2 = parse_deck(raw_deck_2)

    res_1, res_2 = combat(deck_1, deck_2)
    answer_1 = max(score_deck(res_1), score_deck(res_2))
    assert answer_1 == 32472
    print(answer_1)

    _, rec_res_1, rec_res_2 = recursive_combat(deck_1, deck_2)
    answer_2 = max(score_deck(rec_res_1), score_deck(rec_res_2))
    assert answer_2 == 36463
    print(answer_2)


if __name__ == "__main__":
    main()
