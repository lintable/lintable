from uuid import UUID

from git import Commit, Repo
from lintball.lint_report import LintReport


class DoNothingHandler(object):

    def __init__(self):
        pass

    def started(self, uuid: UUID, comment_id: int = None[int]):
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
