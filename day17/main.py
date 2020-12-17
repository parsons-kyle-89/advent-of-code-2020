from enum import Enum
from itertools import product
import os.path
from typing import (
    Callable, Iterable, Iterator, NewType, Mapping, Tuple, TypeVar
)

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
Point = NewType('Point', Tuple[int, ...])
Vector = NewType('Vector', Tuple[int, ...])


def vadd(point: Point, vector: Vector) -> Point:
    assert len(point) == len(vector)
    return Point(tuple(x + v for x, v in zip(point, vector)))


class CubeState(Enum):
    ACTIVE = '#'
    INACTIVE = '.'

    def next_state(self, neighbors: int) -> "CubeState":
        if self is CubeState.ACTIVE and 2 <= neighbors <= 3:
            return CubeState.ACTIVE
        elif self is CubeState.INACTIVE and neighbors == 3:
            return CubeState.ACTIVE
        return CubeState.INACTIVE


class ConwayCube(Mapping[Point, A]):

    def __init__(self, lattice: Mapping[Point, A], null: A, dim: int):
        self._null = null
        self._dim = dim
        for p in lattice:
            self._validate_point(p)
        self._lattice = {p: v for p, v in lattice.items() if v != null}

    def __repr__(self) -> str:
        return f"{type(self).__name__}({str(self._lattice)}, null={self.null})"

    def __len__(self) -> int:
        return len(self._lattice)

    def __getitem__(self, point: Point) -> A:
        self._validate_point(point)
        return self._lattice.get(point, self._null)

    def __delitem__(self, point: Point) -> None:
        del self._lattice[point]

    def __setitem__(self, point: Point, value: A) -> None:
        self._validate_point(point)
        if value == self._null and point in self._lattice:
            del self._lattice[point]
        else:
            self._lattice[point] = value

    def __iter__(self) -> Iterator[Point]:
        return iter(self._lattice)

    @property
    def null(self) -> A:
        return self._null

    @property
    def dim(self) -> int:
        return self._dim

    def shift(self, vector: Vector) -> "ConwayCube[A]":
        return ConwayCube(
            {vadd(p, vector): v for p, v in self.items()},
            self.null,
            self.dim,
        )

    def _validate_point(self, point: Point) -> None:
        if not len(point) == self._dim:
            raise ValueError(
                f"Point dimension ({len(point)}) must match cube "
                f"dimension ({self._dim})"
            )


def bin_op_cubes(
    f: Callable[[A, B], C],
    cube_l: ConwayCube[A],
    cube_r: ConwayCube[B],
    null: C,
) -> ConwayCube[C]:
    assert cube_l.dim == cube_r.dim
    return ConwayCube({
        p: f(cube_l[p], cube_r[p])
        for p in set(cube_l.keys()).union(set(cube_r.keys()))
    }, null, cube_l.dim)


def associate_cubes(
    f: Callable[[Iterable[A]], B],
    cubes: Iterable[ConwayCube[A]],
    null: B,
) -> ConwayCube[B]:
    "The null of each cube should be the same and be the identity for f"
    "Iterates over cubes thrice!!"
    dims = {cube.dim for cube in cubes}
    dim = dims.pop()
    assert not dims
    return ConwayCube({
        p: f([cube[p] for cube in cubes])
        for p in set.union(*(set(cube.keys()) for cube in cubes))
    }, null, dim)


def count_active_neighbors(cube: ConwayCube[CubeState]) -> ConwayCube[int]:
    shifts = [
        Vector(vec)
        for vec in product([-1, 0, 1], repeat=cube.dim)
        if vec != (0,) * cube.dim
    ]
    return associate_cubes(
        lambda neighbors: sum(1 for n in neighbors if n is CubeState.ACTIVE),
        [cube.shift(vec) for vec in shifts],
        0
    )


def next_state(cube: ConwayCube[CubeState]) -> ConwayCube[CubeState]:
    counts = count_active_neighbors(cube)
    return bin_op_cubes(
        CubeState.next_state, cube, counts, CubeState.INACTIVE
    )


def parse_initial_state(raw_lattice: str, dim: int) -> ConwayCube[CubeState]:
    return ConwayCube({
        Point(
            (row_num, col_num, *[0 for _ in range(dim - 2)])
        ): CubeState(cell)
        for row_num, row in enumerate(raw_lattice.splitlines())
        for col_num, cell in enumerate(row)
    }, CubeState.INACTIVE, dim)


def startup_cube(cube: ConwayCube[CubeState]) -> ConwayCube[CubeState]:
    for _ in range(6):
        cube = next_state(cube)
    return cube


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_lattice = f.read()
        cube = parse_initial_state(raw_lattice, 3)
        hypercube = parse_initial_state(raw_lattice, 4)

    started_cube = startup_cube(cube)
    answer_1 = len(started_cube)
    assert answer_1 == 338
    print(answer_1)

    started_hypercube = startup_cube(hypercube)
    answer_2 = len(started_hypercube)
    assert answer_2 == 2440
    print(answer_2)


if __name__ == "__main__":
    main()
