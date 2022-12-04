import pytest

from .input import RucksackInputs, RucksackInput
from .models import PrioritiesMap, Rucksacks, Rucksack, Compartment, Item


@pytest.fixture
def priorities_map() -> PrioritiesMap:
    return PrioritiesMap.build()


class TestPrioritiesMap:
    @pytest.mark.parametrize(
        "_type, expected_priority",
        [("p", 16), ("L", 38), ("P", 42), ("v", 22), ("t", 20), ("s", 19)],
    )
    def test__build__expected_priorities(
        self, _type: str, expected_priority: int, priorities_map: PrioritiesMap
    ) -> None:
        assert priorities_map.map[_type] == expected_priority


class TestRuckSacks:
    @pytest.mark.parametrize(
        "rucksack_inputs, expected_rucksacks",
        [
            (  # single input
                RucksackInputs(inputs=[RucksackInput("abcd")]),
                Rucksacks(
                    rucksacks=[
                        Rucksack(
                            compartment_1=Compartment(
                                items=[
                                    Item(type="a", priority=1),
                                    Item(type="b", priority=2),
                                ]
                            ),
                            compartment_2=Compartment(
                                items=[
                                    Item(type="c", priority=3),
                                    Item(type="d", priority=4),
                                ]
                            ),
                        )
                    ]
                ),
            ),
            (  # multiple inputs
                RucksackInputs(inputs=[RucksackInput("ab"), RucksackInput("cd")]),
                Rucksacks(
                    rucksacks=[
                        Rucksack(
                            compartment_1=Compartment(
                                items=[
                                    Item(type="a", priority=1),
                                ]
                            ),
                            compartment_2=Compartment(
                                items=[
                                    Item(type="b", priority=2),
                                ]
                            ),
                        ),
                        Rucksack(
                            compartment_1=Compartment(
                                items=[
                                    Item(type="c", priority=3),
                                ]
                            ),
                            compartment_2=Compartment(
                                items=[
                                    Item(type="d", priority=4),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
        ],
    )
    def test__from_rucksack_inputs(
        self,
        rucksack_inputs: RucksackInputs,
        expected_rucksacks: Rucksacks,
        priorities_map: PrioritiesMap,
    ) -> None:
        assert (
            Rucksacks.from_rucksack_inputs(rucksack_inputs.inputs, priorities_map)
            == expected_rucksacks
        )

    @pytest.mark.parametrize(
        "rucksack_inputs, expected_priority",
        [
            (RucksackInputs(inputs=[RucksackInput("bb"), RucksackInput("aa")]), 3),
            (RucksackInputs(inputs=[RucksackInput("abcd")]), 0),
            (RucksackInputs(inputs=[RucksackInput("bb")]), 2),
            (RucksackInputs(inputs=[RucksackInput("abab")]), 3),
        ],
    )
    def test__priority(
        self,
        rucksack_inputs: RucksackInputs,
        expected_priority: int,
        priorities_map: PrioritiesMap,
    ) -> None:
        rucksacks = Rucksacks.from_rucksack_inputs(
            rucksack_inputs.inputs, priorities_map
        )
        assert (
            rucksacks.common_rucksack_compartment_item_priorities_sum
            == expected_priority
        )


class TestRucksack:
    def test__from_rucksack_input(self, priorities_map: PrioritiesMap) -> None:
        rucksack_input = RucksackInput("ab")
        expected_rucksack = Rucksack(
            compartment_1=Compartment(
                items=[
                    Item(type="a", priority=1),
                ]
            ),
            compartment_2=Compartment(
                items=[
                    Item(type="b", priority=2),
                ]
            ),
        )
        assert (
            Rucksack.from_rucksack_input(rucksack_input, priorities_map)
            == expected_rucksack
        )

    def test__common_items(self) -> None:
        common_item = Item(type="a", priority=1)
        rucksack = Rucksack(
            compartment_1=Compartment(items=[common_item]),
            compartment_2=Compartment(items=[common_item, Item(type="b", priority=2)]),
        )
        assert rucksack.common_compartment_items == [common_item]

    @pytest.mark.parametrize(
        "rucksack, expected_priority",
        [
            (
                Rucksack(
                    compartment_1=Compartment(items=[Item(type="a", priority=1)]),
                    compartment_2=Compartment(
                        items=[Item(type="a", priority=1), Item(type="b", priority=2)]
                    ),
                ),
                1,
            ),
            (
                Rucksack(
                    compartment_1=Compartment(items=[Item(type="a", priority=1)]),
                    compartment_2=Compartment(items=[Item(type="b", priority=2)]),
                ),
                0,
            ),
        ],
    )
    def test__priority(self, rucksack: Rucksack, expected_priority: int) -> None:
        assert rucksack.common_compartment_items_priority == expected_priority


class TestCompartment:
    @pytest.mark.parametrize(
        "string, expected_compartment",
        [
            (  # no items
                "",
                Compartment(items=[]),
            ),
            (  # single item
                "a",
                Compartment(items=[Item(type="a", priority=1)]),
            ),
            (  # multiple items
                "aB",
                Compartment(
                    items=[Item(type="a", priority=1), Item(type="B", priority=28)]
                ),
            ),
        ],
    )
    def test__from_string(
        self,
        string: str,
        expected_compartment: Compartment,
        priorities_map: PrioritiesMap,
    ) -> None:
        assert Compartment.from_string(string, priorities_map) == expected_compartment

    @pytest.mark.parametrize(
        "other_compartment, expected_common_items",
        [
            (Compartment(items=[]), []),  # no common items
            (  # single common item
                Compartment(items=[Item(type="a", priority=1)]),
                [Item(type="a", priority=1)],
            ),
            (  # multiple common items
                Compartment(
                    items=[Item(type="a", priority=1), Item(type="B", priority=28)]
                ),
                [Item(type="a", priority=1), Item(type="B", priority=28)],
            ),
            (  # common items not duplicated
                Compartment(
                    items=[
                        Item(type="a", priority=1),
                        Item(type="a", priority=1),
                        Item(type="B", priority=28),
                    ]
                ),
                [
                    Item(type="a", priority=1),
                    Item(type="B", priority=28),
                ],
            ),
        ],
    )
    def test__common_items(
        self, other_compartment: Compartment, expected_common_items: list[Item]
    ) -> None:
        compartment = Compartment(
            items=[Item(type="a", priority=1), Item(type="B", priority=28)]
        )
        assert compartment.common_items(other_compartment) == expected_common_items


class TestItem:
    @pytest.mark.parametrize(
        "string, expected_item",
        [("a", Item(type="a", priority=1)), ("Z", Item(type="Z", priority=52))],
    )
    def test__from_string(
        self, string: str, expected_item: Item, priorities_map: PrioritiesMap
    ) -> None:
        assert Item.from_string(string, priorities_map) == expected_item

    @pytest.mark.parametrize(
        "item, items, expected_is_in",
        [
            (Item(type="a", priority=1), [], False),
            (Item(type="a", priority=1), [Item(type="a", priority=1)], True),
        ],
    )
    def test__is_in(self, item: Item, items: list[Item], expected_is_in: bool) -> None:
        assert item.is_in(items) == expected_is_in
