from __future__ import annotations
from dataclasses import dataclass

from .input import RucksackInputs, RucksackInput


@dataclass
class PrioritiesMap:
    map: dict[str, int]

    @classmethod
    def build(cls) -> PrioritiesMap:
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        item_types = alphabet + alphabet.upper()
        priorities = list(range(1, len(item_types) + 1))

        _map = {}
        for i, type in enumerate(item_types):
            _map[type] = priorities[i]
        return cls(map=_map)


@dataclass
class Item:
    type: str
    priority: int

    def is_in(self, items: list[Item]) -> bool:
        return self.type in {item.type for item in items}

    @classmethod
    def from_string(cls, type: str, priorities_map: PrioritiesMap) -> Item:
        return cls(type=type, priority=priorities_map.map[type])


@dataclass
class Compartment:
    items: list[Item]

    def common_items(self, other_compartment: Compartment) -> list[Item]:
        types_to_items = {item.type: item for item in self.items}
        other_compartment_type_set = {item.type for item in other_compartment.items}
        common_types = set(types_to_items).intersection(other_compartment_type_set)
        common_items = [types_to_items[type] for type in common_types]
        return common_items

    @classmethod
    def from_string(
        cls, compartment_str: str, priorities_map: PrioritiesMap
    ) -> Compartment:
        items = [Item.from_string(char, priorities_map) for char in compartment_str]
        return cls(items=items)


@dataclass
class Rucksack:
    compartment_1: Compartment
    compartment_2: Compartment

    @property
    def all_items(self) -> list[Item]:
        return self.compartment_1.items + self.compartment_2.items

    @property
    def common_compartment_items(self) -> list[Item]:
        return self.compartment_1.common_items(self.compartment_2)

    @property
    def common_compartment_items_priority(self) -> int:
        return sum([item.priority for item in self.common_compartment_items])

    @classmethod
    def from_rucksack_input(
        cls, rucksack_input: RucksackInput, priorities_map: PrioritiesMap
    ) -> Rucksack:
        compartment_1_string = rucksack_input.value[: rucksack_input.compartment_length]
        compartment_2_string = rucksack_input.value[rucksack_input.compartment_length :]
        return cls(
            compartment_1=Compartment.from_string(compartment_1_string, priorities_map),
            compartment_2=Compartment.from_string(compartment_2_string, priorities_map),
        )


@dataclass
class Rucksacks:
    rucksacks: list[Rucksack]

    @property
    def common_rucksack_compartment_item_priorities_sum(self) -> int:
        return sum(
            [rucksack.common_compartment_items_priority for rucksack in self.rucksacks]
        )

    @property
    def common_rucksack_items(self) -> list[Item]:
        comparison_rucksack = self.rucksacks[0]
        other_rucksacks = self.rucksacks[1:]

        comparison_types_to_items = {
            item.type: item for item in comparison_rucksack.all_items
        }
        other_rucksack_type_sets = [
            {item.type for item in other_rucksack.all_items}
            for other_rucksack in other_rucksacks
        ]

        common_types = set(comparison_types_to_items).intersection(
            *other_rucksack_type_sets
        )
        common_items = [comparison_types_to_items[type] for type in common_types]
        return common_items

    @property
    def common_rucksack_items_priorities_sum(self) -> int:
        return sum([item.priority for item in self.common_rucksack_items])

    @classmethod
    def from_rucksack_inputs(
        cls, rucksack_inputs: RucksackInputs, priorities_map: PrioritiesMap
    ) -> Rucksacks:
        rucksacks = [
            Rucksack.from_rucksack_input(rucksack_input, priorities_map)
            for rucksack_input in rucksack_inputs
        ]
        return cls(rucksacks=rucksacks)
