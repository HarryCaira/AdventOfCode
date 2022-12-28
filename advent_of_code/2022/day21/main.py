from .input import MonkeyInputs
from .models import MonkeyGraph


def main():
    file = "/Users/harry/Documents/repositories/AdventOfCode/advent_of_code/2022/day21/input.csv"
    inputs = MonkeyInputs.from_file(file)
    graph = MonkeyGraph.create(inputs.inputs)
    print(graph.fill_node_numbers("root"))


if __name__ == "__main__":
    main()
