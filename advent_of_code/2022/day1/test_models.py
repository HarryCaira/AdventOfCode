from .models import FoodItem, Elf, Elves
import pytest


class TestFoodItem:
    @pytest.mark.parametrize(
        "value, expected", [(123, FoodItem(123)), (0, FoodItem(0))]
    )
    def test__from_int(self, value: int, expected: FoodItem) -> None:
        assert FoodItem.from_int(value) == expected


class TestElf:
    def test__from_food_inputs(self) -> None:
        food_inputs = [1, 2, 3, 4]
        expected_elf = Elf(
            food_items=[FoodItem(1), FoodItem(2), FoodItem(3), FoodItem(4)]
        )
        actual_elf = Elf.from_food_inputs(food_inputs)
        assert actual_elf == expected_elf

    @pytest.mark.parametrize(
        "elf, expected_calories",
        [
            (Elf(food_items=[FoodItem(23)]), 23),
            (Elf(food_items=[FoodItem(20), FoodItem(30)]), 50),
        ],
    )
    def test__calories_carried(self, elf: Elf, expected_calories: int) -> None:
        assert elf.calories_carried == expected_calories


class TestElves:
    @pytest.mark.parametrize(
        "food_inputs, expected_elves",
        [
            ([1, 2, None], Elves(elves=[Elf(food_items=[FoodItem(1), FoodItem(2)])])),
            (
                [1, None, 2],
                Elves(
                    elves=[Elf(food_items=[FoodItem(1)]), Elf(food_items=[FoodItem(2)])]
                ),
            ),
        ],
    )
    def test__from_food_inputs(
        self, food_inputs: list[int], expected_elves: Elves
    ) -> None:
        actual_elves = Elves.from_food_inputs(food_inputs)
        assert expected_elves == actual_elves

    def test__total_calories_carried(self) -> None:
        elves = Elves(
            elves=[Elf(food_items=[FoodItem(1)]), Elf(food_items=[FoodItem(2)])]
        )
        assert elves.total_calories_carried == 3

    def test___top_elf_calories_carried(self) -> None:
        elves = Elves(
            elves=[Elf(food_items=[FoodItem(1)]), Elf(food_items=[FoodItem(2)])]
        )
        assert elves.top_elf_calories_carried == 2

    def test___top_three_elves_calories_carried(self) -> None:
        elves = Elves(
            elves=[
                Elf(food_items=[FoodItem(1)]),
                Elf(food_items=[FoodItem(2)]),
                Elf(food_items=[FoodItem(2)]),
                Elf(food_items=[FoodItem(4)]),
            ]
        )
        assert elves.top_three_elves_calories_carried == 8
