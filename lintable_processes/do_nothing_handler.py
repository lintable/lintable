"""Does-nothing class to be used for subclassing."""

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

from uuid import UUID

from git import Commit, Repo

from lintable_lintball.lint_report import LintReport

class DoNothingHandler(object):
    """Does-nothing class to be used for subclassing."""

    def __init__(self):
        pass

    def started(self, uuid: UUID):
        """Kicks off the process."""

        return

    def clone_repo(self, uuid: UUID, repo: Repo, local_path: str):
        """Indicates a repo has been cloned and where that clone is located."""

        return

    def retrieve_changed_file_set(self, uuid: UUID, a_commit: Commit, b_commit: Commit):
        """Indicates what files are going to be retrieved for the 2 commits."""

        return

    def retrieve_file_from_commit(self, uuid: UUID, file: str, commit: Commit):
        """Called for each file being retrieved."""

        return

    def lint_file(self, uuid: UUID, linter: str, file: str):
        """Called when each file is linted."""

        return

    def report(self, uuid: UUID, lint_report: LintReport):
        """Called when the linting process has produced a LintReport."""

        return

    def finish(self, uuid: UUID):
        """Called as a last step to clean up the linting process."""

        return
