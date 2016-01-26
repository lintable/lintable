import unittest

from lintball.lint_error import LintError
from linters.whitespace_file_linter import WhitespaceFileLinter


class DetectTrailingWhitespaceTestCase(unittest.TestCase):
    def setUp(self):
        self.linter = WhitespaceFileLinter()

    def test_empty_string(self):
        test_string = ""
        self.assertEqual(self.linter.has_trailing_whitespace(1, test_string),
                         None)

    def test_tab_only(self):
        test_string = '\t'
        lint_error = LintError(line_number=1,
                               column=1,  # Magic number!
                               msg="Found trailing whitespace: ''"
                               )
        self.assertEqual(self.linter.has_trailing_whitespace(1, test_string),
                         lint_error)

    def test_space_only(self):
        test_string = " "
        lint_error = LintError(line_number=1,
                               column=1,  # Magic number!
                               msg="Found trailing whitespace: ''"
                               )
        self.assertEqual(self.linter.has_trailing_whitespace(1, test_string),
                         lint_error)

    def test_no_trailing_whitespace_empty_list(self):
        test_string = "This is a test string with no whitespace."

        self.assertEqual(self.linter.has_trailing_whitespace(1, test_string),
                         None)

    def test_trailing_whitespace_lint_error(self):
        test_string = "This is a test string with whitespace.  \r\n"

        lint_error = LintError(line_number=1,
                               column=39,  # Magic number!
                               msg="Found trailing whitespace: 'This is a "
                                   "test string with whitespace.'"
                               )

        self.assertEqual(self.linter.has_trailing_whitespace(1, test_string),
                         lint_error)
