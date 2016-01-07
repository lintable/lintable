from functools import reduce
from typing import List

from calc.runner import runner


@runner.task
def summation(xs: List[float]) -> float:
    return reduce(lambda a, b: a + b, xs, 0)

