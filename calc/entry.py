from typing import List

from celery import group
from celery.result import AsyncResult

from uuid import UUID

from calc.runner import runner

from calc.sum import summation
from calc.count import count
from calc.avg import average

submitted_tasks = {}


# yes this is absurd
# its more about proof of concept than actually
# coding something sensible
# this should really send the results to a db
# or some other form of persistent storage
@runner.task
def calc(xs: List[float]) -> UUID:
    tasks = group([summation.s(xs), count.s(xs), average.s(xs)])
    calculations = tasks.apply_async()
    task_id = calculations.id

    global submitted_tasks
    submitted_tasks[task_id] = calculations

    return dict(uuid=task_id)


def get_group_results(task_id: UUID):
    global submitted_tasks
    task = submitted_tasks[task_id]

    if task is None:
        return dict(msg='No such id')
    else:
        return dict(sum=get_subtask_result(task.children[0]),
                    count=get_subtask_result(task.children[1]),
                    avg=get_subtask_result(task.children[2]))


def get_subtask_result(async_result: AsyncResult):
    """

    :type async_result: AsyncResult
    """
    if async_result.successful():
        return async_result.get()
    else:
        return async_result.status
