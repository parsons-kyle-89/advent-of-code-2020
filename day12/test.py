import pytest

from . import main


def test_main() -> None:
    main.main()


@pytest.mark.parametrize(
    ["initial_state", "instruction", "expected_state"],
    (
        (
            main.ShipState(0, 0, main.Facing.E),
            main.Instruction.parse('F10'),
            main.ShipState(10, 0, main.Facing.E),
        ),
        (
            main.ShipState(10, 0, main.Facing.E),
            main.Instruction.parse('N3'),
            main.ShipState(10, 3, main.Facing.E),
        ),
        (
            main.ShipState(10, 3, main.Facing.E),
            main.Instruction.parse('F7'),
            main.ShipState(17, 3, main.Facing.E),
        ),
        (
            main.ShipState(17, 3, main.Facing.E),
            main.Instruction.parse('R90'),
            main.ShipState(17, 3, main.Facing.S),
        ),
        (
            main.ShipState(17, 3, main.Facing.S),
            main.Instruction.parse('F11'),
            main.ShipState(17, -8, main.Facing.S),
        ),
    )
)
def test_follow_instruction(
    initial_state: main.ShipState,
    instruction: main.Instruction,
    expected_state: main.ShipState,
) -> None:
    assert expected_state == main.follow_instruction(
        initial_state, instruction
    )


@pytest.mark.parametrize(
    ["initial_state", "instruction", "expected_state"],
    (
        (
            main.WaypointState(0, 0, 10, 1),
            main.Instruction.parse('F10'),
            main.WaypointState(100, 10, 10, 1),
        ),
        (
            main.WaypointState(100, 10, 10, 1),
            main.Instruction.parse('N3'),
            main.WaypointState(100, 10, 10, 4),
        ),
        (
            main.WaypointState(100, 10, 10, 4),
            main.Instruction.parse('F7'),
            main.WaypointState(170, 38, 10, 4),
        ),
        (
            main.WaypointState(170, 38, 10, 4),
            main.Instruction.parse('R90'),
            main.WaypointState(170, 38, 4, -10),
        ),
        (
            main.WaypointState(170, 38, 4, -10),
            main.Instruction.parse('F11'),
            main.WaypointState(214, -72, 4, -10),
        ),
    )
)
def test_follow_waypoint_instruction(
    initial_state: main.WaypointState,
    instruction: main.Instruction,
    expected_state: main.WaypointState,
) -> None:
    assert expected_state == main.follow_waypoint_instruction(
        initial_state, instruction
    )
