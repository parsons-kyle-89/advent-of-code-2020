from dataclasses import dataclass
import os.path
import re
from typing import Collection, Container, Dict, FrozenSet, Iterable, Mapping

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


@dataclass(frozen=True)
class FoodInfo:
    ingredients: FrozenSet[str]
    allergens: FrozenSet[str]


def parse_food_info(line: str) -> FoodInfo:
    match = re.fullmatch(r"([^\(]+) \(contains ([^\)]+)\)", line)
    assert match is not None
    raw_ingredients, raw_alergens = match.groups()
    return FoodInfo(
        frozenset(raw_ingredients.split()),
        frozenset(raw_alergens.split(', ')),
    )


def collect_ingredients(food_infos: Iterable[FoodInfo]) -> FrozenSet[str]:
    return frozenset.union(
        *(food_info.ingredients for food_info in food_infos)
    )


def collect_allergens(food_infos: Iterable[FoodInfo]) -> FrozenSet[str]:
    return frozenset.union(
        *(food_info.allergens for food_info in food_infos)
    )


def find_possible_allergens(
    food_infos: Collection[FoodInfo],
    all_allergens: Iterable[str],
    all_ingredients: FrozenSet[str],
) -> Dict[str, FrozenSet[str]]:
    return {
        allergen: all_ingredients.intersection(*(
            food_info.ingredients
            for food_info in food_infos
            if allergen in food_info.allergens
        ))
        for allergen in all_allergens
    }


def eliminate_possible_allergens(
    possible_allergens: Mapping[str, Container[str]],
    ingredients: Iterable[str],
) -> FrozenSet[str]:
    return frozenset(
        ingredient for ingredient in ingredients
        if not any(
            ingredient in possible_ingredients
            for possible_ingredients in possible_allergens.values()
        )
    )


def determine_allergens(
    possible_allergens: Dict[str, FrozenSet[str]],
) -> Dict[str, str]:
    definite_allergens = {}
    while possible_allergens:
        allergen, (ingredient,) = next(
            (allergen, ingredients)
            for allergen, ingredients in possible_allergens.items()
            if len(ingredients) == 1
        )
        definite_allergens[allergen] = ingredient
        possible_allergens = {
            alrgn: frozenset(ingr for ingr in ingrs if ingr != ingredient)
            for alrgn, ingrs in possible_allergens.items()
            if alrgn != allergen
        }
    return definite_allergens


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        food_infos = {parse_food_info(line.strip()) for line in f.readlines()}

    all_ingredients = collect_ingredients(food_infos)
    all_allergens = collect_allergens(food_infos)
    possible_allergens = find_possible_allergens(
        food_infos,
        all_allergens,
        all_ingredients,
    )
    safe_ingredients = eliminate_possible_allergens(
        possible_allergens, all_ingredients
    )
    answer_1 = sum(
        sum(1 for food_info in food_infos
            if safe_ingredient in food_info.ingredients)
        for safe_ingredient in safe_ingredients
    )
    assert answer_1 == 2374
    print(answer_1)

    definite_allergens = determine_allergens(possible_allergens)
    answer_2 = ','.join(
        pair[1]
        for pair in sorted(definite_allergens.items(), key=lambda p: p[0])
    )
    assert answer_2 == 'fbtqkzc,jbbsjh,cpttmnv,ccrbr,tdmqcl,vnjxjg,nlph,mzqjxq'
    print(answer_2)


if __name__ == "__main__":
    main()
