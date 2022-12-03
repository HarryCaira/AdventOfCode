from .input import FoodInputs
from .models import Elves
import click


@click.command()
@click.option(
    "--file-name",
    type=click.Path(exists=True),
    default="/Users/harry/Documents/coding/repos/AdventOfCode/advent_of_code/2022/day1/input.csv",
)
def main(file_name: str):
    food_inputs = FoodInputs.from_file(file_name)
    elves = Elves.from_food_inputs(food_inputs.inputs)

    print(f"Total calories carried: {elves.total_calories_carried}")
    print(f"Maximum calories carried by the top elf: {elves.top_elf_calories_carried}")
    print(
        f"Maximum calories carried by the top three elves: {elves.top_three_elves_calories_carried}"
    )


if __name__ == "__main__":
    main()
