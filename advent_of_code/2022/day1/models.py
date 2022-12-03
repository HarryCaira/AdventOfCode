from __future__ import annotations
from dataclasses import dataclass
from more_itertools import split_at
from typing import Optional


@dataclass
class FoodItem:
    calories: int

    @classmethod
    def from_int(cls, value: int) -> FoodItem:
        return cls(calories=value)


@dataclass
class Elf:
    food_items: list[FoodItem]

    @classmethod
    def from_food_inputs(cls, food_inputs: list[int]) -> Elf:
        food_items = [FoodItem.from_int(input) for input in food_inputs]
        return cls(food_items=food_items)

    @property
    def calories_carried(self) -> int:
        return sum([food.calories for food in self.food_items])


@dataclass
class Elves:
    elves: list[Elf]

    @classmethod
    def from_food_inputs(cls, food_inputs: list[Optional[int]]) -> Elves:
        elf_food_inputs = list(split_at(food_inputs, lambda x: x is None))
        elves = []
        for food_inputs in elf_food_inputs:
            if not food_inputs:
                continue
            elves.append(Elf.from_food_inputs(food_inputs))

        return cls(elves=elves)

    @property
    def total_calories_carried(self) -> int:
        return sum([elf.calories_carried for elf in self.elves])

    @property
    def top_elf_calories_carried(self) -> int:
        return max([elf.calories_carried for elf in self.elves])

    @property
    def top_three_elves_calories_carried(self) -> int:
        return sum(
            sorted([elf.calories_carried for elf in self.elves], reverse=True)[:3]
        )
