from __future__ import absolute_import

import logging

from celery import Celery

runner = Celery('runner',
                broker='amqp://',
                backend='redis://',
                include=['calc.sum',
                         'calc.avg',
                         'calc.count',
                         'calc.entry'])

# Optional configuration, see the application user guide.
runner.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
        CELERY_ACCEPT_CONTENT=['json'],
        CELERY_TASK_SERIALIZER='json',
        CELERY_RESULT_SERIALIZER='json',
        CELERY_IGNORE_RESULT=False,
        CELERY_CHORD_PROPAGATES=True
)

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


if __name__ == '__main__':
    runner.start()
