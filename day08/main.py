from dataclasses import dataclass
from enum import auto, Enum
import os.path
from typing import Iterator, List, Set

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


class Operation(Enum):
    NOP = auto()
    ACC = auto()
    JMP = auto()


@dataclass(frozen=True)
class Instruction:
    operation: Operation
    argument: int


Program = List[Instruction]


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


@dataclass(frozen=True)
class ProgramTermination(Exception):
    pass


class TerminationReason(Enum):
    InfiniteLoop = auto()
    NormalTermination = auto()


class TracingInterpreter:
    def __init__(self, program: Program) -> None:
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
        if next_state.line_number == len(self._program):
            raise ProgramTermination
        self._state = next_state
        self._line_cache.add(next_state.line_number)

    def run(self) -> TerminationReason:
        while True:
            try:
                self._run_step_or_raise()
            except InfiniteLoopError:
                return TerminationReason.InfiniteLoop
            except ProgramTermination:
                return TerminationReason.NormalTermination

    @property
    def accumulator(self) -> int:
        return self._state.accumulator


def program_patches(program: Program) -> Iterator[Program]:
    for i, instruction in enumerate(program):
        if instruction.operation == Operation.NOP:
            new_instruction = Instruction(Operation.JMP, instruction.argument)
        elif instruction.operation == Operation.JMP:
            new_instruction = Instruction(Operation.NOP, instruction.argument)
        else:
            continue
        patch = program.copy()
        patch[i] = new_instruction
        yield patch


def patch_program(program: Program) -> Program:
    for patched_program in program_patches(program):
        interpreter = TracingInterpreter(patched_program)
        termination_reason = interpreter.run()
        if termination_reason == TerminationReason.NormalTermination:
            return patched_program
    raise RuntimeError('Patch could not be found')


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        program = [
            parse_instruction(raw_instruction)
            for raw_instruction in f.readlines()
        ]

    interpreter = TracingInterpreter(program)
    termination_reason = interpreter.run()
    assert termination_reason == TerminationReason.InfiniteLoop
    answer_1 = interpreter.accumulator
    assert answer_1 == 1553, "first answer is wrong"
    print(answer_1)

    patch = patch_program(program)
    interpreter = TracingInterpreter(patch)
    interpreter.run()
    answer_2 = interpreter.accumulator
    assert answer_2 == 1877, "second answer is wrong"
    print(answer_2)


if __name__ == "__main__":
    main()
