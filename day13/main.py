from dataclasses import dataclass
from functools import reduce
from operator import itemgetter, mul
import os.path
from typing import Iterable, Tuple

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


@dataclass
class ExtendedGCDResult:
    gcd: int
    m: int
    n: int
    a: int
    b: int

    def __post_init__(self) -> None:
        lhs = self.m * self.a + self.n * self.b
        if lhs != self.gcd:
            raise ValueError(
                f"m*a + n*b must equal gcd "
                f"got lhs of {lhs} and rhs of {self.gcd}"
            )

    def __str__(self) -> str:
        return (
            f"ExtendedGCDResult({self.m}*{self.a}"
            f" + {self.n}*{self.b} = {self.gcd})"
        )


def extended_gcd(m: int, n: int) -> ExtendedGCDResult:
    old_d, d = m, n
    old_a, a = 1, 0
    old_b, b = 0, 1

    while d != 0:
        quotient = old_d // d
        old_d, d = d, old_d - quotient * d
        old_a, a = a, old_a - quotient * a
        old_b, b = b, old_b - quotient * b

    return ExtendedGCDResult(
        gcd=old_d,
        m=m,
        n=n,
        a=old_a,
        b=old_b,
    )


def inverse_mod_n(m: int, n: int) -> int:
    return extended_gcd(m, n).a


@dataclass(frozen=True)
class ModularCongruence:
    remainder: int
    modulus: int

    def __str__(self) -> str:
        return f"x = {self.remainder} (mod {self.modulus})"


def prod(it: Iterable[int]) -> int:
    return reduce(mul, it, 1)


def crt(congruences: Iterable[ModularCongruence]) -> int:
    rs = [mc.remainder for mc in congruences]
    ns = [mc.modulus for mc in congruences]
    N = prod(ns)
    ys = [N // n for n in ns]
    zs = [inverse_mod_n(y, n) for y, n in zip(ys, ns)]
    return sum(r * y * z for r, y, z in zip(rs, ys, zs)) % N


def next_departure_bus_and_wait(
    arrival: int, buses: Iterable[int]
) -> Tuple[int, int]:
    return min(
        ((bus, -arrival % bus) for bus in buses), key=itemgetter(1)
    )


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        arrival = int(f.readline().strip())
        second_line = f.readline()
        buses = [int(b) for b in second_line.split(',') if b != 'x']
        congruences = [
            ModularCongruence(-i, int(b))
            for i, b in enumerate(second_line.split(','))
            if b != 'x'
        ]

    bus, wait = next_departure_bus_and_wait(arrival, buses)
    answer_1 = bus * wait
    assert answer_1 == 2545
    print(answer_1)

    answer_2 = crt(congruences)
    assert answer_2 == 266204454441577
    print(answer_2)


if __name__ == "__main__":
    main()
