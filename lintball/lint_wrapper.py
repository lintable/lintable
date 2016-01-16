import subprocess
from typing import List

from lintball.lint_error import LintError

"""
This class serves as, for lack of a better term, an abstract base class for wrapping linters, providing what
is hopefully a reasonable implementation for lint_file.

The goal is that additional linters should (hopefully) only need to define lint_command and provide a parser
implementation.
"""

class BaseLintWrapper:
    lint_command = "/bin/echo"

    def lint_file(self, filename: str, optional_parameters: List[str] = None) -> List[LintError]:
        call_parameters = [self.lint_command, filename]

        if optional_parameters is not None:
            call_parameters.extend(optional_parameters)


        lint_result = subprocess.run(call_parameters,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     universal_newlines=True)

        return self.parse_linter_output(lint_result)

    def parse_linter_output(self, output: str) -> List[LintError]:
        raise Exception("parse_linter_output not implemented for " + self.__class__.__name__)
