from typing import List

from calc.runner import runner


@runner.task
def count(xs: List[float]) -> float:
        return len(xs)
