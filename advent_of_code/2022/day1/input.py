from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Optional
import pandas as pd


@dataclass
class InputRowSchema:
    CALORIES = "calories"


class InvalidFoodInput(Exception):
    ...


@dataclass
class FoodInputs:
    inputs: list[Optional[int]]
    num_raw_rows: int

    @classmethod
    def from_file(cls, file_name: str) -> FoodInputs:
        def convert_optional_int(value: Union[float, str]) -> Optional[str]:
            if pd.isnull(value):
                return None
            try:
                return int(value)
            except (TypeError, ValueError) as exception:
                raise InvalidFoodInput(f"Failed to create input \n{exception}")

        raw_df = pd.read_csv(file_name, skip_blank_lines=False)
        raw_rows = raw_df.to_dict(orient="records")

        inputs = []
        for row in raw_rows:
            try:
                inputs.append(convert_optional_int(row[InputRowSchema.CALORIES]))
            except KeyError as exception:
                raise InvalidFoodInput(f"Failed to create input \n{exception}")
        return cls(inputs=inputs, num_raw_rows=len(raw_rows))
