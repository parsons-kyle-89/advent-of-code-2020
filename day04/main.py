import os.path
import re
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


def validate_passport(passport: Dict[str, str]) -> bool:
    required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    return required_fields <= passport.keys()


def strict_validate_passport(passport: Dict[str, str]) -> bool:
    return (
        validate_passport(passport) and
        validate_int(passport.get('byr', ''), 1920, 2002) and
        validate_int(passport.get('iyr', ''), 2010, 2020) and
        validate_int(passport.get('eyr', ''), 2020, 2030) and
        validate_height(passport.get('hgt', '')) and
        validate_hair_color(passport.get('hcl', '')) and
        validate_eye_color(passport.get('ecl', '')) and
        validate_passport_id(passport.get('pid', ''))
    )


def validate_int(year: str, lower: int, upper: int) -> bool:
    try:
        parsed_year = int(year)
    except ValueError:
        return False
    return lower <= parsed_year <= upper


def validate_height(height: str) -> bool:
    if height.endswith('cm'):
        lower = 150
        upper = 193
    elif height.endswith('in'):
        lower = 59
        upper = 76
    else:
        return False
    num_part = height[:-2]
    return validate_int(num_part, lower, upper)


def validate_hair_color(hair_color: str) -> bool:
    return bool(re.match(r'^#[0-9a-f]{6}$', hair_color))


def validate_eye_color(eye_color: str) -> bool:
    return bool(re.match(r'^(amb|blu|brn|gry|grn|hzl|oth)$', eye_color))


def validate_passport_id(passport_id: str) -> bool:
    return bool(re.match(r'^\d{9}$', passport_id))


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        passport_batch = f.read()
    passports = parse_records(passport_batch)

    answer_1 = sum(1 for passport in passports if validate_passport(passport))
    assert answer_1 == 250
    print(answer_1)

    answer_2 = (
        sum(1 for passport in passports if strict_validate_passport(passport))
    )
    assert answer_2 == 158
    print(answer_2)


if __name__ == "__main__":
    main()
