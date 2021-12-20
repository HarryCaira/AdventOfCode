import os
import statistics
import pandas as pd
from typing import Optional

OPENING_BRACKETS = "[{(<"
CLOSING_BRACKETS = "]})>"


def test_line(line: str) -> Optional[tuple[str, str]]:
    opened_stack = []
    for idx, char in enumerate(line):

        if idx == 0:
            if line[idx] in CLOSING_BRACKETS:
                return ("CORRUPTED", char)

        if char in OPENING_BRACKETS:
            opened_stack.append(char)
            continue

        elif char in CLOSING_BRACKETS:
            if opened_stack[-1] + char in ["{}", "[]", "<>", "()"]:
                opened_stack.pop()
                continue
            else:
                return ("CORRUPTED", char)

    if opened_stack:
        return ("INCOMPLETE", opened_stack)


def calc_syntax_error_score(corruptions: dict[str, int]) -> int:
    corruption_scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    total_score = sum(
        [corruptions[key] * corruption_scores[key] for key in corruptions.keys()]
    )
    return total_score


def calc_closing_sequence(stack: list[str]) -> str:
    stack.reverse()
    closing_sequence = "".join(
        [CLOSING_BRACKETS[OPENING_BRACKETS.index(char)] for char in stack]
    )
    return closing_sequence


def calc_closing_sequence_score(closing_sequence: str) -> int:
    closing_scores = {")": 1, "]": 2, "}": 3, ">": 4}
    score = 0
    for char in closing_sequence:
        score = (score * 5) + closing_scores[char]
    return score


def main():
    this_file_dir = os.path.dirname(os.path.realpath(__file__))

    df = pd.read_csv(os.path.join(this_file_dir, "input.csv"), header=None)

    corruptions = {"]": 0, "}": 0, ")": 0, ">": 0}
    closing_sequence_scores = []
    for _, row in df.iterrows():
        status, val = test_line(row[0])

        # part one
        if status == "CORRUPTED":
            corruptions[val] += 1

        # part two
        if status == "INCOMPLETE":
            closing_sequence = calc_closing_sequence(val)
            closing_sequence_score = calc_closing_sequence_score(closing_sequence)
            closing_sequence_scores.append(closing_sequence_score)

    syntax_error_score = calc_syntax_error_score(corruptions)
    middle_score = statistics.median(closing_sequence_scores)
    print(f"Total syntax error = {syntax_error_score}")
    print(f"Middle score = {middle_score}")


if __name__ == "__main__":
    main()
