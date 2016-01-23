import subprocess
from typing import List

from abc import ABC, abstractmethod
from lintball.lint_error import LintError

""" An abstract base class defining a simple contract for linters and no implementation. """


class LintWrapper(ABC):
    @abstractmethod
    def lint(self, filename: str) -> List[LintError]:
        return None


"""
An implementation of LintWrapper which is itself also an abstract base class with what is hopefully a
reasonable implementation for the lint(...) function.
"""


class FileLintWrapper(LintWrapper):
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

    @abstractmethod
    def parse_linter_output(self, output: str) -> List[LintError]:
        return None
