from dataclasses import dataclass
import os.path
from typing import NewType, Tuple

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

Password = NewType('Password', str)


@dataclass
class Policy:
    lower: int
    upper: int
    character: str

    def __post_init__(self) -> None:
        if len(self.character) != 1:
            raise ValueError(
                f"character must be string of length one: {self.character}"
            )
        if self.lower > self.upper:
            raise ValueError(
                f"lower is larger than than upper: {self.lower} {self.upper}"
            )


def check_password(password: Password, policy: Policy) -> bool:
    return policy.lower <= password.count(policy.character) <= policy.upper


def parse_line(line: str) -> Tuple[Policy, Password]:
    _range, char_part, raw_password = line.split(' ', 2)

    raw_lower, raw_upper = _range.split('-', 1)
    lower, upper = int(raw_lower), int(raw_upper)
    assert len(char_part) == 2
    char = char_part[0]
    policy = Policy(lower=lower, upper=upper, character=char)

    password = Password(raw_password)

    return policy, password


@dataclass
class PolicyV2:
    index1: int
    index2: int
    character: str

    def __post_init__(self) -> None:
        if len(self.character) != 1:
            raise ValueError(
                f"character must be string of length one: {self.character}"
            )


def check_password_v2(password: Password, policy: PolicyV2) -> bool:
    return (
        (password[policy.index1 - 1] == policy.character) ^
        (password[policy.index2 - 1] == policy.character)
    )


def parse_line_v2(line: str) -> Tuple[PolicyV2, Password]:
    _idxs, char_part, raw_password = line.split(' ', 2)

    raw_idx1, raw_idx2 = _idxs.split('-', 1)
    idx1, idx2 = int(raw_idx1), int(raw_idx2)
    assert len(char_part) == 2
    char = char_part[0]
    policy = PolicyV2(index1=idx1, index2=idx2, character=char)

    password = Password(raw_password)

    return policy, password


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        policy_password_pairs = [
            parse_line(line.strip()) for line in f.readlines()
        ]

    print(sum(
        1 for policy, password in policy_password_pairs
        if check_password(password, policy)
    ))

    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        policy_password_pairs_v2 = [
            parse_line_v2(line.strip()) for line in f.readlines()
        ]

    print(sum(
        1 for policy, password in policy_password_pairs_v2
        if check_password_v2(password, policy)
    ))


if __name__ == '__main__':
    main()
