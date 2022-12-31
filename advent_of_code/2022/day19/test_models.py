from .models import Resources
import pytest


class TestResources:
    @pytest.mark.parametrize(
        "inventory, cost, expected",
        [
            (  # can afford - no cost
                Resources(ore=0, clay=0, obsidian=0, geode=0),
                Resources(ore=0, clay=0, obsidian=0, geode=0),
                True,
            ),
            (  # can afford everything
                Resources(ore=1, clay=1, obsidian=1, geode=1),
                Resources(ore=1, clay=1, obsidian=1, geode=1),
                True,
            ),
            (  # can't afford ore
                Resources(ore=1, clay=0, obsidian=0, geode=0),
                Resources(ore=2, clay=0, obsidian=0, geode=0),
                False,
            ),
            (  # can't afford clay
                Resources(ore=0, clay=1, obsidian=0, geode=0),
                Resources(ore=0, clay=2, obsidian=0, geode=0),
                False,
            ),
            (  # can't afford obsidian
                Resources(ore=0, clay=0, obsidian=1, geode=0),
                Resources(ore=0, clay=0, obsidian=2, geode=0),
                False,
            ),
            (  # can't afford geode
                Resources(ore=0, clay=0, obsidian=0, geode=1),
                Resources(ore=0, clay=0, obsidian=0, geode=2),
                False,
            ),
            (  # can't afford geode
                Resources(ore=2, clay=2, obsidian=0, geode=0),
                Resources(ore=0, clay=2, obsidian=7, geode=0),
                False,
            ),
        ],
    )
    def test__can_afford(self, inventory: Resources, cost: Resources, expected) -> None:
        assert inventory.can_afford(cost) == expected

    @pytest.mark.parametrize(
        "first, second, expected",
        [
            (
                Resources(ore=0, clay=0, obsidian=0, geode=0),
                Resources(ore=0, clay=0, obsidian=0, geode=0),
                Resources(ore=0, clay=0, obsidian=0, geode=0),
            ),
            (
                Resources(ore=1, clay=1, obsidian=1, geode=1),
                Resources(ore=2, clay=2, obsidian=2, geode=2),
                Resources(ore=-1, clay=-1, obsidian=-1, geode=-1),
            ),
        ],
    )
    def test__subtract(self, first, second, expected) -> None:
        assert first - second == expected
