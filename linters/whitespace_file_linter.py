from typing import List
import re

from lintball.lint_error import LintError
from lintball.lint_wrapper import BaseLintWrapper

"""
This linter is a special case of the lint wrapper where we are attempting to detect whitespace at the end of a line.
Because we're not wrapping a linter provided by a third party it makes just as much sense to implement it directly in
python as a subclass of the wrapper.
"""


class WhitespaceFileLinter(BaseLintWrapper):
    ws_regex = re.compile("(\.)*(\s+)")

    # see this for the gory details, I'm going to cover the most probable
    # https://en.wikipedia.org/wiki/Newline
    # UNIX style line breaks, only a newline
    lf_regex = re.compile("(\.*)\n")
    # Windows style line breaks, carraige return followed by a newline
    cr_lf_regex = re.compile("(\.*)\r\n")
    # MacOS 9 and earlier
    cr_regex = re.compile("(\.*)\r")

    # TODO: Can this be reasonably replaced with re.compile(".*(\r|\n|\r\n)") ?

    def lint_file(self, filename: str, optional_parameters: List[str] = None)-> List[LintError]:
        total_matches = []

        # TODO: Open the file, read contents, split that instead of the filename.
        lines = self.lf_regex.split(filename)[1:]

        line_number = 1

        for line in lines:
            total_matches.append(self.has_trailing_whitespace(line_number, line))
            line_number += 1

        return total_matches

    def has_trailing_whitespace(self, line_number: int, line: str)-> List[LintError]:
        split = self.ws_regex.split(line)

        if len(split) > 1:
            return [LintError(line_number=line_number,
                              column=len(split[0]),
                              msg='Found trailing whitespace \'$ws\''.format(ws=split[-2]))]
        else:
            return []
