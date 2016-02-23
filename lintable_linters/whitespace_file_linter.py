"""Detects lines in a given file with trailing whitespace."""

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
from typing import List

import re

from lintable_lintball.lint_error import LintError
from lintable_lintball.lint_wrapper import LintWrapper

class WhitespaceFileLinter(LintWrapper):
    """Detects lines in a given file with trailing whitespace."""

    ws_regex = re.compile(r"^(.*?)(\s+)$")
    logger = logging.getLogger(__name__)

    def __repr__(self):
        return 'Whitespace Linter'

    def lint(self, filename: str) -> List[LintError]:
        """Lint the given file, provided as a file path."""

        total_matches = []
        lines = self.get_lines(filename)
        line_number = 1

        for line in lines:
            lint_error = self.has_trailing_whitespace(line_number, line)
            if lint_error is not None:
                total_matches.append(lint_error)
            line_number += 1

        return total_matches

    def has_trailing_whitespace(self, line_number: int, line: str) -> List[LintError]:
        """Detects whether the given line has trailing whitespace."""
        LOGGER = logging.getLogger()

        match = self.ws_regex.match(line)
        LOGGER.error('line: {}'.format(line))
        if match:
            return LintError(line_number=line_number,
                             column=match.start(2) + 1,
                             msg="Found trailing whitespace: '{}'".format(match.group(1)))
        else:
            return None

    def get_lines(self, filename: str) -> List[str]:
        """Open the file at the given path and return its contents as a list."""

        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
        except Exception as e:
            self.logger.error(
                'File processing failed.\nException: \n{}'.format(e))
            lines = []
        return lines
