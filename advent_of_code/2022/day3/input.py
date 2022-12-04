from __future__ import annotations
from dataclasses import dataclass
from typing import Union
import pandas as pd


@dataclass
class InputRowSchema:
    RUCKSACK_INPUT = "rucksack_input"


class InvalidRucksackInput(Exception):
    ...


@dataclass
class RucksackInput:
    value: str

    @property
    def length(self) -> int:
        return len(self.value)

    @property
    def compartment_length(self) -> int:
        return self.length // 2

    @classmethod
    def from_row(cls, row: dict) -> RucksackInput:
        def convert_alphabetic_string(value: Union[float, str]) -> str:
            if isinstance(value, float):
                raise InvalidRucksackInput(f"Expected string, got float: {value}")
            if not value.isalpha():
                raise InvalidRucksackInput(
                    f"Expected an alphabetic string, got: {value}"
                )
            if len(value) % 2 != 0:
                raise InvalidRucksackInput(f"Expected an even length string")
            return value

        try:
            return cls(
                value=convert_alphabetic_string(row[InputRowSchema.RUCKSACK_INPUT])
            )
        except KeyError as exception:
            raise InvalidRucksackInput(f"Error creating rucksack input: \n{exception}")


@dataclass
class RucksackInputs:
    inputs: list[RucksackInput]

    @classmethod
    def from_file(cls, file_name: str) -> RucksackInputs:
        raw_df = pd.read_csv(file_name)
        raw_rows = raw_df.to_dict(orient="records")
        inputs = [RucksackInput.from_row(row) for row in raw_rows]
        return cls(inputs=inputs)
