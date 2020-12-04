import pytest

from . import main


@pytest.mark.parametrize(
    ['record', 'is_valid'],

    (
        ("ecl:gry pid:860033327 eyr:2020 hcl:#fffffd\n"
         "byr:1937 iyr:2017 cid:147 hgt:183cm",
         True),

        ("iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884\n"
         "hcl:#cfa07d byr:1929",
         False),

        ("hcl:#ae17e1 iyr:2013\n"
         "eyr:2024\n"
         "ecl:brn pid:760753108 byr:1931\n"
         "hgt:179cm",
         True),

        ("hcl:#cfa07d eyr:2025 pid:166559648\n"
         "iyr:2011 ecl:brn hgt:59in",
         False),
    )
)
def test_validate_password(record: str, is_valid: bool) -> None:
    assert main.validate_passport(main.parse_record(record)) == is_valid
