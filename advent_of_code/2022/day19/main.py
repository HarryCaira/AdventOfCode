from .models import RobotFleet, Resources


def main():
    fleet = RobotFleet(
        ore_robot_cost=Resources(4, 0, 0, 0),
        clay_robot_cost=Resources(0, 2, 0, 0),
        obsidian_robot_cost=Resources(3, 14, 0, 0),
        geode_robot_cost=Resources(2, 0, 7, 0),
    )
    fleet.run()


if __name__ == "__main__":
    main()
