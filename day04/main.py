import os.path
from typing import Dict, List, Tuple

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def parse_records(document: str) -> List[Dict[str, str]]:
    return [
        parse_record(record)
        for record in document.split('\n\n')
    ]


def parse_record(record: str) -> Dict[str, str]:
    raw_fields = record.replace(' ', '\n').split()

    def split_field(field: str) -> Tuple[str, str]:
        key, value = field.split(':', 1)
        return key, value
    return dict(split_field(field) for field in raw_fields)


def validate_passport(password: Dict[str, str]) -> bool:
    required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    return required_fields <= password.keys()


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        passport_batch = f.read()

    passports = parse_records(passport_batch)
    print(sum(1 for passport in passports if validate_passport(passport)))


if __name__ == "__main__":
    main()
