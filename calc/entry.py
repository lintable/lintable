from typing import List

from calc.runner import runner

from calc.sum import summation
from calc.count import count
from calc.avg import average

# yes this is absurd
# its more about proof of concept than actually
# coding something sensible
# this should really send the results to a db
# or some other form of persistent storage
@runner.task
def calc(xs: List[float]):
    summ = summation.delay(xs).wait()
    cnt = count.delay(xs).wait()
    avg = average.delay(xs).wait()
    return dict(avg=avg,
                sum=summ,
                count=cnt)