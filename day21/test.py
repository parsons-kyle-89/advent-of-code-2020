from typing import Iterator, List

import pytest

from . import main


def test_main() -> None:
    main.main()


def test_parse_food_info() -> None:
    line = "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)"
    expected = main.FoodInfo(
        frozenset({"mxmxvkd", "kfcds", "sqjhc", "nhms"}),
        frozenset({"dairy", "fish"}),
    )
    assert main.parse_food_info(line) == expected


def test_eliminate_possible_allergens(food_infos: List[main.FoodInfo]) -> None:
    all_ingredients = main.collect_ingredients(food_infos)
    all_allergens = main.collect_allergens(food_infos)
    possible_allergens = main.find_possible_allergens(
        food_infos,
        all_allergens,
        all_ingredients,
    )
    safe_ingredients = main.eliminate_possible_allergens(
        possible_allergens, all_ingredients
    )
    assert safe_ingredients == {"kfcds", "nhms", "sbzzf", "trh"}


def test_determine_allergens(food_infos: List[main.FoodInfo]) -> None:
    all_ingredients = main.collect_ingredients(food_infos)
    all_allergens = main.collect_allergens(food_infos)
    possible_allergens = main.find_possible_allergens(
        food_infos,
        all_allergens,
        all_ingredients,
    )
    definite_allergens = main.determine_allergens(possible_allergens)
    assert definite_allergens == {
        'dairy': 'mxmxvkd',
        'fish': 'sqjhc',
        'soy': 'fvjkl',
    }


@pytest.fixture
def food_infos() -> Iterator[List[main.FoodInfo]]:
    raw_food_infos = (
        "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)\n"
        "trh fvjkl sbzzf mxmxvkd (contains dairy)\n"
        "sqjhc fvjkl (contains soy)\n"
        "sqjhc mxmxvkd sbzzf (contains fish)\n"
    ).strip()
    yield [main.parse_food_info(line) for line in raw_food_infos.splitlines()]
