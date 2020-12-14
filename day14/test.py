import pytest

from . import main


@pytest.mark.slow
def test_main() -> None:
    main.main()
