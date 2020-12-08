import pytest

from . import main


def test_main() -> None:
    main.main()


def test_parse_line() -> None:
    line = "1-3 a: abcde"
    expected_policy = main.Policy(1, 3, "a")
    expected_password = main.Password('abcde')

    actual_policy, actual_password = main.parse_line(line)

    assert actual_policy == expected_policy
    assert actual_password == expected_password


@pytest.mark.parametrize(
    ["policy", "password", "match"],

    (
        (
            main.Policy(1, 3, 'a'),
            main.Password('abcde'),
            True,
        ),

        (
            main.Policy(1, 3, 'b'),
            main.Password('cdefg'),
            False,
        ),

        (
            main.Policy(2, 9, 'c'),
            main.Password('ccccccccc'),
            True,
        ),
    )
)
def test_check_password(
    policy: main.Policy,
    password: main.Password,
    match: bool,
) -> None:
    assert main.check_password(password, policy) == match


def test_parse_line_v2() -> None:
    line = "1-3 a: abcde"
    expected_policy = main.PolicyV2(1, 3, "a")
    expected_password = main.Password('abcde')

    actual_policy, actual_password = main.parse_line_v2(line)

    assert actual_policy == expected_policy
    assert actual_password == expected_password


@pytest.mark.parametrize(
    ["policy", "password", "match"],

    (
        (
            main.PolicyV2(1, 3, 'a'),
            main.Password('abcde'),
            True,
        ),

        (
            main.PolicyV2(1, 3, 'b'),
            main.Password('cdefg'),
            False,
        ),

        (
            main.PolicyV2(2, 9, 'c'),
            main.Password('ccccccccc'),
            False,
        ),
    )
)
def test_check_password_v2(
    policy: main.PolicyV2,
    password: main.Password,
    match: bool,
) -> None:
    assert main.check_password_v2(password, policy) == match
