from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from enum import Enum
import pandas as pd


class Operation(str, Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"


@dataclass
class MonkeyInput:
    name: str
    number: Optional[int]
    operation: Optional[Operation]
    children: list[str]

    @classmethod
    def from_row(cls, input_string: str) -> MonkeyInput:
        name, yell = input_string.split(": ")
        try:
            return cls(name=name, number=int(yell.strip()), operation=None, children=[])
        except (TypeError, ValueError):
            child1, operation, child2 = yell.strip().split(" ")
            return cls(
                name=name,
                number=None,
                operation=Operation(operation),
                children=[child1, child2],
            )


@dataclass
class MonkeyInputs:
    inputs: list[MonkeyInput]

    @classmethod
    def from_file(cls, file_name: str) -> MonkeyInputs:
        raw_df = pd.read_csv(file_name, skip_blank_lines=False)
        raw_rows = raw_df.to_dict(orient="records")
        return cls(inputs=[MonkeyInput.from_row(row["input"]) for row in raw_rows])
