from logging import getLogger
from typing import List, Dict

from celery import group, chord
from celery.result import AsyncResult, GroupResult

from uuid import UUID

from calc.runner import runner

from calc.sum import summation
from calc.count import count
from calc.avg import average

logger = getLogger('entry')


@runner.task(serializer='json')
def calc(xs: List[float]) -> UUID:
    callback = collect_results.s()
    tasks = [summation.s(xs),
             count.s(xs),
             average.s(xs)]

    calculations = chord(tasks, callback).apply_async(
            serializer='json')

    task_id = calculations.id

    return dict(uuid=task_id)


@runner.task(serializer='json')
def collect_results(results: List[float]) -> Dict[str, float]:
    logger.info('collect_results args: '.format(args=results))
    return dict(sum=results[0], count=results[1], avg=results[2])


def get_group_results(task_id: UUID):
    logger.info('retrieving task id: $task_id'.format(task_id=task_id))
    task = runner.AsyncResult(id=task_id)

    if task is None:
        return dict(msg='No such id')
    else:
        return task.result


def get_subtask_result(async_result: AsyncResult):
    """

    :type async_result: AsyncResult
    """
    if async_result.successful():
        return async_result.get()
    else:
        return async_result.status
