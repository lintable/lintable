"""Wrappers for assorted linters."""

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

import subprocess
from typing import List

from abc import ABC, abstractmethod

from lintable_lintball.lint_error import LintError

class LintWrapper(ABC):
    """Abstract base class for a contract for linters. No implementation."""

    @abstractmethod
    def lint(self, filename: str) -> List[LintError]:
        """Lint a given file by filename."""

        return None

class FileLintWrapper(LintWrapper):
    """Abstract base class for file-based linters.

    Hopefully a reasonable implementation for the lint(...) function.
    """

    lint_command = "/bin/echo"

    def lint_file(self, filename: str, optional_parameters: List[str] = None) -> List[LintError]:
        """Have the linter lint a given file."""

        call_parameters = [self.lint_command, filename]

        if optional_parameters is not None:
            call_parameters.extend(optional_parameters)

        lint_result = subprocess.run(call_parameters,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     universal_newlines=True)

        return self.parse_linter_output(lint_result)

    @abstractmethod
    def parse_linter_output(self, output: str) -> List[LintError]:
        """Process output from the linter."""

        return None
