from __future__ import absolute_import

import logging

from celery import Celery

runner = Celery('runner',
                broker='amqp://',
                backend='amqp://',
                include=['calc.sum',
                         'calc.avg',
                         'calc.count',
                         'calc.entry'])

# Optional configuration, see the application user guide.
runner.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


if __name__ == '__main__':
    runner.start()
