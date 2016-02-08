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

from enum import Enum

class ProcessState(Enum):
    """
    This tracks the state of the linting process
    """
    STARTED = 1,  # process has started
    CLONE_REPO = 2,  # the repo is being cloned
    RETRIEVE_FILES = 3,  # the files are being retrieved from the repo
    LINT_FILES = 4,  # the retrieved files are being linted
    REPORT = 5,  # the report from the linting process is shown
    FINISHED = 6  # the linting process is finished
