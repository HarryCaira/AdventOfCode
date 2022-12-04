from .input import RucksackInputs, RucksackInput


class TestRucksackInputs:
    def test__from_file(self) -> None:
        test_file = "advent_of_code/2022/day3/fixtures/test_input.csv"
        expected_inputs = RucksackInputs(
            inputs=[
                RucksackInput(value="vJrwpWtwJgWrhcsFMMfFFhFp"),
                RucksackInput(value="jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL"),
                RucksackInput(value="PmmdzqPrVvPwwTWBwg"),
                RucksackInput(value="wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn"),
                RucksackInput(value="ttgJtRGJQctTZtZT"),
                RucksackInput(value="CrZsJsPPZsGzwwsLwLmpwMDw"),
            ]
        )
        actual_inputs = RucksackInputs.from_file(test_file)
        assert expected_inputs == actual_inputs
