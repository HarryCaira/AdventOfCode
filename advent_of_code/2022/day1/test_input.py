from .input import FoodInputs


class TestFoodInputs:
    def test__from_file(self) -> None:
        test_file = "advent_of_code/2022/day1/fixtures/test_input.csv"
        expected_inputs = FoodInputs(inputs=[17998, None, 7761], num_raw_rows=3)
        actual_inputs = FoodInputs.from_file(test_file)
        assert expected_inputs == actual_inputs
