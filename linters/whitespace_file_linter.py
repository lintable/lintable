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


from typing import List

import re
from lintball.lint_error import LintError
from lintball.lint_wrapper import LintWrapper
import logging


"""
The core MVP linter, attempting to detect whitespace on modified lines.
"""


class WhitespaceFileLinter(LintWrapper):
    ws_regex = re.compile("^(.*?)(\s+)$")
    logger = logging.getLogger(__name__)

    def lint(self, filename: str) -> List[LintError]:
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
        match = self.ws_regex.match(line)

        if match:
            return LintError(line_number=line_number,
                             column=match.start(2) + 1,
                             msg="Found trailing whitespace: '{}'".format(match.group(1)))
        else:
            return None

    def get_lines(self, filename: str) -> List[str]:
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
        except Exception as e:
            self.logger.error(
                'File processing failed.\nException: \n{}'.format(e))
            lines = []
        return lines
