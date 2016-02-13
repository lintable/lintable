"""Sets up a task runner for jobs."""

# Copyright 2015-2016 Capstone Team G
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from celery import Celery

from lintable_settings.settings import LINTBALL_SETTINGS

runner = Celery('lintable_lintball.runner',
                broker=LINTBALL_SETTINGS['celery']['broker'],
                backend=LINTBALL_SETTINGS['celery']['backend'],
                include=['lintable_lintball.lintball'])

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
