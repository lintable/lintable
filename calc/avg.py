from typing import List

from calc.runner import runner
from calc.sum import summation
from calc.count import count

@runner.task
def average(xs: List[float]) -> float:
    return summation(xs) / count(xs)  # .delay(xs) / count.delay(xs)
