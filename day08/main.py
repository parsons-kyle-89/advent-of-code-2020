from dataclasses import dataclass
from enum import auto, Enum
import os.path
from typing import List, Set

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


class Operation(Enum):
    NOP = auto()
    ACC = auto()
    JMP = auto()


@dataclass(frozen=True)
class Instruction:
    operation: Operation
    argument: int


def parse_instruction(raw_instruction: str) -> Instruction:
    raw_operation, raw_argument = raw_instruction.split(' ', 1)
    argument = int(raw_argument)
    operation = parse_operation(raw_operation)
    return Instruction(operation, argument)


def parse_operation(raw_operation: str) -> Operation:
    if raw_operation == 'nop':
        return Operation.NOP
    elif raw_operation == 'acc':
        return Operation.ACC
    elif raw_operation == 'jmp':
        return Operation.JMP
    raise ValueError(f"unrecognized operation: {raw_operation}")


@dataclass(frozen=True)
class InterpreterState:
    line_number: int
    accumulator: int

    def accumulate(self, amount: int) -> "InterpreterState":
        return InterpreterState(self.line_number, self.accumulator + amount)

    def jump(self, amount: int) -> "InterpreterState":
        return InterpreterState(self.line_number + amount, self.accumulator)


@dataclass(frozen=True)
class InfiniteLoopError(RuntimeError):
    pass


class TracingInterpreter:
    def __init__(self, program: List[Instruction]) -> None:
        self._program = program
        self._state = InterpreterState(0, 0)
        self._line_cache: Set[int] = set()

    def _calculate_next_state(self) -> InterpreterState:
        instruction = self._program[self._state.line_number]
        if instruction.operation == Operation.NOP:
            return self._state.jump(1)
        elif instruction.operation == Operation.ACC:
            return self._state.accumulate(instruction.argument).jump(1)
        elif instruction.operation == Operation.JMP:
            return self._state.jump(instruction.argument)
        raise RuntimeError("Impossible state reached")

    def _run_step_or_raise(self) -> None:
        next_state = self._calculate_next_state()
        if next_state.line_number in self._line_cache:
            raise InfiniteLoopError
        self._state = next_state
        self._line_cache.add(next_state.line_number)

    def run_until_loop(self) -> None:
        while True:
            try:
                self._run_step_or_raise()
            except InfiniteLoopError:
                break

    @property
    def accumulator(self) -> int:
        return self._state.accumulator


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        program = [parse_instruction(raw_instruction) for raw_instruction in f.readlines()]

    interpreter = TracingInterpreter(program)
    interpreter.run_until_loop()
    print(interpreter.accumulator)


if __name__ == "__main__":
    main()
