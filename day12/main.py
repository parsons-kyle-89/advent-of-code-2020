from dataclasses import dataclass
from enum import auto, Enum
from functools import reduce
import math
import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def cos(deg: float) -> int:
    return int(round(math.cos(deg * math.pi / 180)))


def sin(deg: float) -> int:
    return int(round(math.sin(deg * math.pi / 180)))


class Facing(Enum):
    E = 0
    N = 90
    W = 180
    S = 270


class Action(Enum):
    E = 0
    N = 90
    W = 180
    S = 270
    F = auto()
    R = -1
    L = 1


@dataclass(frozen=True)
class Instruction:
    action: Action
    value: int

    @classmethod
    def parse(cls, raw_instruction: str) -> "Instruction":
        raw_action, raw_value = raw_instruction[0], raw_instruction[1:]
        return cls(parse_action(raw_action), int(raw_value))


def parse_action(raw_action: str) -> Action:
    if raw_action == 'E':
        return Action.E
    elif raw_action == 'N':
        return Action.N
    elif raw_action == 'W':
        return Action.W
    elif raw_action == 'S':
        return Action.S
    elif raw_action == 'F':
        return Action.F
    elif raw_action == 'R':
        return Action.R
    elif raw_action == 'L':
        return Action.L
    raise ValueError(f"Unknown action {raw_action}")


@dataclass(frozen=True)
class ShipState:
    x_pos: int
    y_pos: int
    facing: Facing


def follow_instruction(
    ship_state: ShipState,
    instruction: Instruction,
) -> ShipState:
    action = instruction.action
    value = instruction.value

    x_pos = ship_state.x_pos
    y_pos = ship_state.y_pos
    facing = ship_state.facing

    if action is Action.F:
        return ShipState(
            x_pos + value * cos(facing.value),
            y_pos + value * sin(facing.value),
            facing
        )
    elif (
        action is Action.N or action is Action.S or
        action is Action.E or action is Action.W
    ):
        return ShipState(
            x_pos + value * cos(action.value),
            y_pos + value * sin(action.value),
            facing
        )
    elif action is Action.L or action is Action.R:
        return ShipState(
            x_pos,
            y_pos,
            Facing((facing.value + value * action.value) % 360)
        )


@dataclass(frozen=True)
class WaypointState:
    ship_x: int
    ship_y: int
    waypoint_x: int
    waypoint_y: int


def follow_waypoint_instruction(
    waypoint_state: WaypointState,
    instruction: Instruction,
) -> WaypointState:
    action = instruction.action
    value = instruction.value

    ship_x = waypoint_state.ship_x
    ship_y = waypoint_state.ship_y
    waypoint_x = waypoint_state.waypoint_x
    waypoint_y = waypoint_state.waypoint_y

    if action is Action.F:
        return WaypointState(
            ship_x + value * waypoint_x,
            ship_y + value * waypoint_y,
            waypoint_x,
            waypoint_y
        )
    elif (
        action is Action.N or action is Action.S or
        action is Action.E or action is Action.W
    ):
        return WaypointState(
            ship_x,
            ship_y,
            waypoint_x + value * cos(action.value),
            waypoint_y + value * sin(action.value)
        )
    elif action is Action.L or action is Action.R:
        return WaypointState(
            ship_x,
            ship_y,
            (
                waypoint_x * cos(action.value * value) -
                waypoint_y * sin(action.value * value)
            ),
            (
                waypoint_x * sin(action.value * value) +
                waypoint_y * cos(action.value * value)
            )
        )


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        instructions = [Instruction.parse(line) for line in f.readlines()]

    initial_state = ShipState(0, 0, Facing.E)
    final_state = reduce(follow_instruction, instructions, initial_state)
    answer_1 = abs(final_state.x_pos) + abs(final_state.y_pos)
    assert answer_1 == 1319
    print(answer_1)

    initial_waypoint_state = WaypointState(0, 0, 10, 1)
    final_waypoint_state = reduce(
        follow_waypoint_instruction, instructions, initial_waypoint_state
    )
    answer_2 = (
        abs(final_waypoint_state.ship_x) + abs(final_waypoint_state.ship_y)
    )
    assert answer_2 == 62434
    print(answer_2)


if __name__ == "__main__":
    main()
