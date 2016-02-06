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
from lintball.lint_report import LintReport


class DoNothingHandler(object):
    """
    This is a do nothing handler.
    The process handler delegates to a subclass of this.
    """
    def __init__(self):
        pass

    def started(self, uuid: UUID, comment_id: int = None):
        return

    def clone_repo(self, uuid: UUID, repo: Repo, local_path: str):
        return

    def retrieve_changed_file_set(self, uuid: UUID, a_commit: Commit, b_commit: Commit):
        return

    def retrieve_file_from_commit(self, uuid: UUID, file: str, commit: Commit):
        return

    def lint_file(self, uuid: UUID, linter: str, file: str):
        return

    def report(self, uuid: UUID, report: LintReport):
        return

    def finish(self, uuid: UUID):
        return
