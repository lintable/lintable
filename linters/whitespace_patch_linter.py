from typing import List

from lintball.lint_error import LintError
from linters.whitespace_file_linter import WhitespaceFileLinter

"""
This linter is a special case of the lint wrapper where we are attempting to detect whitespace at the end of a line.
Because we're not wrapping a linter provided by a third party it makes just as much sense to implement it directly in
python as a subclass of the wrapper.

This linter expects to operate on a patch file calculated by the "diff" command or similar. (Python diff library?)
"""


class WhitespacePatchLinter(WhitespaceFileLinter):
    def lint(self, filename: str) -> List[LintError]:
        total_matches = []

        lines = [None]  # TODO: Open the file and diff it python diff library. Do the thing.
        for line_number, line in lines:
            assert isinstance(line, str)
            total_matches.append(self.has_trailing_whitespace(line_number, line))

        return total_matches
