from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class RockPaperScissorsMove(str, Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


@dataclass
class RockPaperScissors:
    move: RockPaperScissorsMove
    points: int

    @classmethod
    def from_input(cls) -> RockPaperScissors:
        ...


@dataclass
class Strategy:
    stategy: list[RockPaperScissors]

    @classmethod
    def from_inputs(cls, inputs: list[str]) -> Strategy:
        ...


@dataclass
class Score:
    ...


@dataclass
class Player:
    strategy: Strategy
    score: Score
