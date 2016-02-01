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

"""
The core MVP linter, attempting to detect whitespace on modified lines.
"""


class WhitespaceFileLinter(LintWrapper):
    ws_regex = re.compile("^(.*?)(\s+)$")

    # see this for the gory details, I'm going to cover the most probable
    # https://en.wikipedia.org/wiki/Newline
    # UNIX style line breaks, only a newline
    lf_regex = re.compile("(\.*)\n")
    # Windows style line breaks, carriage return followed by a newline
    cr_lf_regex = re.compile("(\.*)\r\n")
    # MacOS 9 and earlier
    cr_regex = re.compile("(\.*)\r")

    # TODO: Can this be reasonably replaced with re.compile(".*(\r|\n|\r\n)") ?

    def lint(self, filename: str) -> List[LintError]:
        total_matches = []

        # TODO: Open the file, read contents, split that instead of the filename.
        lines = self.lf_regex.split(filename)[1:]

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
