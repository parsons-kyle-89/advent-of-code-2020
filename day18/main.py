import os.path
import re

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


class NewNum:
    def __init__(self, num: int) -> None:
        self._num = num

    def __str__(self) -> str:
        return str(self._num)

    def __repr__(self) -> str:
        return f"NewNum({self._num})"

    def __lshift__(self, other: "NewNum") -> "NewNum":
        "actually +"
        return NewNum(self._num + other._num)

    def __rshift__(self, other: "NewNum") -> "NewNum":
        "actually *"
        return NewNum(self._num * other._num)

    def __int__(self) -> int:
        return self._num


class NewerNum:
    def __init__(self, num: int) -> None:
        self._num = num

    def __str__(self) -> str:
        return str(self._num)

    def __repr__(self) -> str:
        return f"NewerNum({self._num})"

    def __add__(self, other: "NewerNum") -> "NewerNum":
        "actually *"
        return NewerNum(self._num * other._num)

    def __mul__(self, other: "NewerNum") -> "NewerNum":
        "actually +"
        return NewerNum(self._num + other._num)

    def __int__(self) -> int:
        return self._num


def translate_raw_equation(raw_equation: str) -> str:
    return (
        re.sub(r"(\d+)", lambda m: f"NewNum({m.group(0)})", raw_equation)
        .replace('+', '<<')
        .replace('*', '>>')
    )


def other_translate_raw_equation(raw_equation: str) -> str:
    return (
        re.sub(r"(\d+)", lambda m: f"NewerNum({m.group(0)})", raw_equation)
        .replace('+', '^')
        .replace('*', '+')
        .replace('^', '*')
    )


def new_math(eq: str) -> int:
    return int(eval(translate_raw_equation(eq)))


def newer_math(eq: str) -> int:
    return int(eval(other_translate_raw_equation(eq)))


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        eqs = list(f.readlines())

    answer_1 = sum(new_math(eq) for eq in eqs)
    assert answer_1 == 13976444272545
    print(answer_1)

    answer_2 = sum(newer_math(eq) for eq in eqs)
    assert answer_2 == 88500956630893
    print(answer_2)


if __name__ == "__main__":
    main()
