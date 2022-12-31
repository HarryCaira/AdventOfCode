from __future__ import annotations
from dataclasses import dataclass
from colorama import Fore
from enum import Enum


class RobotType(Enum):
    ORE = "ore"
    CLAY = "clay"
    OBSIDIAN = "obsidian"
    GEODE = "geode"


@dataclass(order=True)
class Resources:
    clay: int = 0
    ore: int = 0
    obsidian: int = 0
    geode: int = 0

    def add_clay(self, amount: int) -> None:
        self.clay += amount

    def add_ore(self, amount: int) -> None:
        self.ore += amount

    def add_obsidian(self, amount: int) -> None:
        self.obsidian += amount

    def add_geode(self, amount: int) -> None:
        self.geode += amount

    def can_afford(self, cost: Resources) -> bool:
        if (
            self.clay - cost.clay >= 0
            and self.ore - cost.ore >= 0
            and self.obsidian - cost.obsidian >= 0
            and self.geode - cost.geode >= 0
        ):
            return True
        return False

    def __sub__(self, other: Resources) -> Resources:
        ore = self.ore - other.ore
        clay = self.clay - other.clay
        obsidian = self.obsidian - other.obsidian
        geode = self.geode - other.geode
        return Resources(ore=ore, clay=clay, obsidian=obsidian, geode=geode)

    def __add__(self, other: Resources) -> Resources:
        ore = self.ore + other.ore
        clay = self.clay + other.clay
        obsidian = self.obsidian + other.obsidian
        geode = self.geode + other.geode
        return Resources(ore=ore, clay=clay, obsidian=obsidian, geode=geode)


@dataclass
class RobotFleet:
    ore_robot_cost: Resources
    clay_robot_cost: Resources
    obsidian_robot_cost: Resources
    geode_robot_cost: Resources

    def collect_resources(self, robots: RobotType) -> Resources:
        resources = Resources()
        print(Fore.GREEN)
        for robot in robots:
            if robot == RobotType.ORE:
                print(f"Ore collecting robot collects 1 ore")
                resources.add_ore(1)
            elif robot == RobotType.CLAY:
                print(f"Clay collecting robot collects 1 clay")
                resources.add_clay(1)
            elif robot == RobotType.OBSIDIAN:
                print(f"Obsidian collecting robot collects 1 obsidian")
                resources.add_obsidian(1)
            elif robot == RobotType.GEODE:
                print(f"Geode collecting robot collects 1 geode")
                resources.add_geode(1)

        return resources

    def build_new_robots(
        self, inventory: Resources
    ) -> tuple[Resources, list[RobotType]]:
        new_robots = []
        spent_resources = Resources()

        print(Fore.RED)
        if inventory.can_afford(self.ore_robot_cost + spent_resources):
            print(f"Spent {self.ore_robot_cost} to start building an ore robot")
            spent_resources = spent_resources + self.ore_robot_cost
            new_robots.append(RobotType.ORE)

        if inventory.can_afford(self.clay_robot_cost + spent_resources):
            print(f"Spent {self.clay_robot_cost} to start building a clay robot")
            spent_resources = spent_resources + self.clay_robot_cost
            new_robots.append(RobotType.CLAY)

        if inventory.can_afford(self.obsidian_robot_cost + spent_resources):
            print(
                f"Spent {self.obsidian_robot_cost} to start building an obsidian robot"
            )
            spent_resources = spent_resources + self.obsidian_robot_cost
            new_robots.append(RobotType.OBSIDIAN)

        if inventory.can_afford(self.geode_robot_cost + spent_resources):
            print(f"Spent {self.geode_robot_cost} to start building a geode robot")
            spent_resources = spent_resources + self.geode_robot_cost
            new_robots.append(RobotType.GEODE)

        return spent_resources, new_robots

    def run(self) -> None:
        robots = [RobotType.ORE]
        factory_robots = []
        inventory = Resources()
        minutes_elapsed = 1

        while minutes_elapsed < 24:
            print(Fore.WHITE + f"\nMinute {minutes_elapsed}")
            print(Fore.BLUE + f"{inventory = }")

            spent_resources, new_robots = self.build_new_robots(inventory)
            inventory = inventory - spent_resources
            factory_robots.append(new_robots)

            new_resources = self.collect_resources(robots)
            inventory = inventory + new_resources

            print(Fore.WHITE + f"\nCollected {new_resources}")

            new_robots = factory_robots.pop(0)
            if new_robots:
                robots += new_robots

                print(
                    Fore.RESET + f"The {len(new_robots)} new robots are ready: ",
                    *new_robots,
                )

            minutes_elapsed += 1
        return
