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

import unittest

from lintable_lintball.lint_error import LintError
from lintable_linters.whitespace_file_linter import WhitespaceFileLinter

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
