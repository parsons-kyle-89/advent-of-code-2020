import pytest

from . import main


@pytest.mark.slow
def test_main() -> None:
    main.main()


@pytest.mark.parametrize(
    ["pubkey", "loop_size"],
    (
        (17807724, 11),
        (5764801, 8),
    )
)
def test_decode_pubkey(pubkey: int, loop_size: int) -> None:
    assert main.decode_pubkey(pubkey) == loop_size


@pytest.mark.parametrize(
    ["pubkey", "loop_size"],
    (
        (17807724, 8),
        (5764801, 11),
    )
)
def test_second_encoding(pubkey: int, loop_size: int) -> None:
    assert main.pubkey(loop_size, subject_number=pubkey) == 14897079
