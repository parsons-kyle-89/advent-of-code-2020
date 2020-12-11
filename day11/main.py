from enum import Enum
import os.path
from typing import Callable, Sequence, Tuple

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


class State(Enum):
    Empty = 'L'
    Occupied = '#'
    Floor = '.'


class StateArrangement:
    def __init__(self, states: Sequence[Sequence[State]]):
        n_rows = len(states)
        if n_rows == 0:
            raise ValueError(f"States must be nonempty, got: {states}")

        n_cols = len(states[0])
        for i, row in enumerate(states):
            if len(row) != n_cols:
                raise ValueError(
                    f"All rows must be same length, found row {i} with"
                    f"with length {len(row)} instead of {n_cols}: {row}"
                )

        self._states = states
        self._n_rows = n_rows
        self._n_cols = n_cols

    def __str__(self) -> str:
        return '\n'.join(''.join(s.value for s in row) for row in self._states)

    def __getitem__(self, idx: Tuple[int, int]) -> State:
        row, col = idx
        if (0 <= row < self._n_rows) and (0 <= col < self._n_cols):
            return self._states[row][col]
        return State.Empty

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StateArrangement):
            return NotImplemented
        return self._states == other._states

    def _next_state(
        self,
        neighbor_func: Callable[[int, int], int],
        tolerance: int,
    ) -> "StateArrangement":
        return StateArrangement([
            [
                self._next_loc_state(row, col, neighbor_func, tolerance)
                for col in range(self._n_cols)
            ]
            for row in range(self._n_rows)
        ])

    def next_state_adjacent(self) -> "StateArrangement":
        return self._next_state(self._adjacent_neighbors, 4)

    def _adjacent_neighbors(self, row: int, col: int) -> int:
        return sum(
            self[r, c] == State.Occupied
            for r in range(row - 1, row + 2)
            for c in range(col - 1, col + 2)
            if not (r == row and c == col)
        )

    def _next_loc_state(
        self,
        row: int,
        col: int,
        neighbor_func: Callable[[int, int], int],
        tolerance: int,
    ) -> State:
        this_state = self[row, col]
        if this_state is State.Floor:
            return State.Floor
        num_neighbors = neighbor_func(row, col)
        if num_neighbors == 0 and this_state is State.Empty:
            return State.Occupied
        if num_neighbors >= tolerance and this_state == State.Occupied:
            return State.Empty
        return this_state

    def num_in_state(self, state: State) -> int:
        return sum(s is state for row in self._states for s in row)

    @classmethod
    def from_raw(cls, raw_states: str) -> "StateArrangement":
        return cls([
            [State(raw_state) for raw_state in raw_row]
            for raw_row in raw_states.splitlines()
        ])


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        arrangement = StateArrangement.from_raw(f.read())

    while True:
        next_arrangement = arrangement.next_state_adjacent()
        if arrangement == next_arrangement:
            break
        arrangement = next_arrangement

    answer_1 = arrangement.num_in_state(State.Occupied)
    assert answer_1 == 2277
    print(answer_1)


if __name__ == "__main__":
    main()
