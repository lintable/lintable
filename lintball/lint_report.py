from typing import NamedTuple, Dict, List

from lintball.lint_error import LintError

# The keys in the errors dictionary are the file names of the files linted
LintReport = NamedTuple('LintReport', [('errors', Dict[str, List[LintError]])])