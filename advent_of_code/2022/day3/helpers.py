from typing import Generator


def chunks(lst: list, n: int) -> Generator:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]
