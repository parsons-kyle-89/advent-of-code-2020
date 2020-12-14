from typing import Set

import pytest

from . import main


@pytest.mark.slow
def test_main() -> None:
    main.main()


@pytest.mark.parametrize(
    ['raw_mask', "inp_", "expected"],
    (
        ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 11, 73),
        ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 101, 101),
        ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 0, 64),
    )
)
def test_apply_mask(raw_mask: str, inp_: int, expected: int) -> None:
    mask = main.parse_mask(raw_mask)
    assert main.apply_mask(inp_, mask) == expected


@pytest.mark.parametrize(
    ["raw_mask", "register", "expected_registers"],
    (
        ('000000000000000000000000000000X1001X', 42, {26, 27, 58, 59}),
        (
            '00000000000000000000000000000000X0XX',
            26,
            {16, 17, 18, 19, 24, 25, 26, 27}
        ),
    )
)
def test_mask_register(
    raw_mask: str,
    register: int,
    expected_registers: Set[int]
) -> None:
    mask = main.parse_mask(raw_mask)
    assert set(main.mask_register(register, mask)) == expected_registers
