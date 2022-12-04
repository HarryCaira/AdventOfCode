from .helpers import chunks
from .input import RucksackInputs
from .models import PrioritiesMap, Rucksacks
import click


@click.command()
@click.option(
    "--file-name",
    type=click.Path(exists=True),
    default="/Users/harry/Documents/coding/repos/AdventOfCode/advent_of_code/2022/day3/input.csv",
)
def main(file_name: str):
    rucksack_inputs = RucksackInputs.from_file(file_name)
    priorities_map = PrioritiesMap.build()

    all_rucksacks = Rucksacks.from_rucksack_inputs(
        rucksack_inputs.inputs, priorities_map
    )
    print(
        f"The sum of item type priorities that appear in both compartments for each rucksack is: {all_rucksacks.common_rucksack_compartment_item_priorities_sum}"
    )

    grouped_rucksacks = [
        Rucksacks.from_rucksack_inputs(rucksack_inputs, priorities_map)
        for rucksack_inputs in chunks(rucksack_inputs.inputs, 3)
    ]
    total_elf_group_priorities = sum(
        [
            rucksacks.common_rucksack_items_priorities_sum
            for rucksacks in grouped_rucksacks
        ]
    )
    print(f"{total_elf_group_priorities = }")


if __name__ == "__main__":
    main()
