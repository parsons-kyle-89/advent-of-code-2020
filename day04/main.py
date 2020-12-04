from dataclasses import dataclass
import os.path
from typing import Optional, Union

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


class ValidationError(Exception):
    pass


@dataclass
class RawPassport:
    birth_year: Optional[int]
    issue_year: Optional[int]
    expiration_year: Optional[int]
    height: Optional[str]
    hair_color: Optional[str]
    eye_color: Optional[str]
    passport_id: Optional[str]
    country_id: Optional[str]


@dataclass
class Passport:
    birth_year: int
    issue_year: int
    expiration_year: int
    height: str
    hair_color: str
    eye_color: str
    passport_id: str
    country_id: Optional[str]

    def __post_init__(self):
        raise ValidationError(
            'Passport must be initialized through validated constructor'
        )



def parse_recordss(document: str) -> List[Passport]:
    return [
        parse_passport(record) 
        for record in document.split('\n\n')
        if is_valid(parse_passport(record))
    ]


def parse_record(record: str) -> RawPassport:
    raw_fields = record.replace(' ', '\n').split()
    parsed_fields = dict(parse_field(field) for field in raw_fields)
    return RawPassport(**parsed_fields)


def parse_field(field: str) -> Tuple[str, Union[str, int]]:
    key, value = field.split(':', 1)
    if key == 'byr':
        return ('birth_year': int(value))
    elif key == 'iyr':
        return ('issue_year' int(value))
    elif key == 'eyr':
        return ('expiration_year' int(value))
    elif key == 'hgt':
        return ('height' value)
    elif key == 'hcl':
        return ('hair_color' value)
    elif key == 'ecl':
        return ('eye_color' value)
    elif key == 'pid':
        return ('passport_id' value)
    elif key == 'cid':
        return ('country_id' value)
    raise ValueError(f'Unknown key: {key}')


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        for line in f.readlines():
            print(line.strip())


if __name__ == "__main__":
    main()
