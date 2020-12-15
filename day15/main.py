from dataclasses import dataclass, field
import os.path
from typing import Dict, Sequence

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


@dataclass
class Game:
    round: int
    last_number: int
    _number_histories: Dict[int, int] = field(default_factory=dict)

    def speak(self, number: int) -> None:
        self._number_histories[self.last_number] = self.round - 1
        self.last_number = number
        self.round += 1

    def what_to_speak(self) -> int:
        if self.last_number not in self._number_histories:
            return 0
        prev = self._number_histories[self.last_number]
        return self.round - 1 - prev


def run_game(starting_numbers: Sequence[int], to_round: int) -> Game:
    game = Game(1, -1, {})
    for number in starting_numbers:
        game.speak(number)
    while game.round <= to_round:
        game.speak(game.what_to_speak())
    return game


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        starting_numbers = [int(n) for n in f.read().split(',')]

    game = run_game(starting_numbers, 2020)
    answer_1 = game.last_number
    assert answer_1 == 755
    print(answer_1)

    game = run_game(starting_numbers, 30_000_000)
    answer_2 = game.last_number
    assert answer_2 == 11962
    print(answer_2)


if __name__ == "__main__":
    main()
