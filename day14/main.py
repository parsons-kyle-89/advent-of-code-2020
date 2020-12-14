from dataclasses import dataclass, field
from enum import Enum
from itertools import product
import os.path
from typing import Dict, Iterator, List, NoReturn, Union

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


class Trit(Enum):
    ONE = '1'
    ZERO = '0'
    NULL = 'X'


Mask = List[Trit]


def apply_mask(i: int, mask: Mask) -> int:
    return int(''.join(
        i_bit if m_trit is Trit.NULL else m_trit.value
        for i_bit, m_trit in zip(format(i, "036b"), mask)
    ), 2)


def mask_register(register: int, mask: Mask) -> Iterator[int]:
    num_null = mask.count(Trit.NULL)
    first_pass = [
        Trit(str(r_bit)) if m_bit is Trit.ZERO else m_bit
        for r_bit, m_bit in zip(format(register, '036b'), mask)
    ]
    for replacements in product([Trit.ONE, Trit.ZERO], repeat=num_null):
        it = iter(replacements)
        yield int(''.join(map(
            lambda t: next(it).value if t is Trit.NULL else t.value,
            first_pass
        )), 2)


@dataclass(frozen=True)
class SetMem:
    register: int
    value: int


@dataclass(frozen=True)
class SetMask:
    mask: Mask


Instruction = Union[SetMem, SetMask]


def parse_instruction(raw_instruction: str) -> Instruction:
    if raw_instruction.startswith('mask'):
        _, raw_mask = raw_instruction.rsplit(' = ', 1)
        return SetMask(parse_mask(raw_mask))
    elif raw_instruction.startswith('mem'):
        raw_register, raw_value = (
            raw_instruction
            .removeprefix('mem[')
            .split('] = ', 1)
        )
        return SetMem(int(raw_register), int(raw_value))
    raise ValueError(f"Unrecognized instruction: {raw_instruction}")


def parse_mask(raw_mask: str) -> Mask:
    return [Trit(t) for t in raw_mask]


@dataclass
class BitmaskComputer:
    mask: Mask = field(default_factory=lambda: [Trit.NULL for _ in range(36)])
    memory: Dict[int, int] = field(default_factory=lambda: {})

    def run_instruction(self, instruction: Instruction) -> None:
        if isinstance(instruction, SetMem):
            self.memory[instruction.register] = (
                apply_mask(instruction.value, self.mask)
            )
        elif isinstance(instruction, SetMask):
            self.mask = instruction.mask
        else:
            absurd: NoReturn = instruction
            raise TypeError(f'absurd reached with value {absurd}')

    def run_instruction_v2(self, instruction: Instruction) -> None:
        if isinstance(instruction, SetMem):
            for register in mask_register(instruction.register, self.mask):
                self.memory[register] = instruction.value
        elif isinstance(instruction, SetMask):
            self.mask = instruction.mask
        else:
            absurd: NoReturn = instruction
            raise TypeError(f'absurd reached with value {absurd}')


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        program = [parse_instruction(line.strip()) for line in f.readlines()]

    comp = BitmaskComputer()
    for instruction in program:
        comp.run_instruction(instruction)
    answer_1 = sum(comp.memory.values())
    assert answer_1 == 16003257187056
    print(answer_1)

    comp = BitmaskComputer()
    for instruction in program:
        comp.run_instruction_v2(instruction)
    answer_2 = sum(comp.memory.values())
    print(answer_2)


if __name__ == "__main__":
    main()
