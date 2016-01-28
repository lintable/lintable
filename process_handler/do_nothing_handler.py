from uuid import UUID

from git import Repo
from lintball.lint_report import LintReport


class DoNothingHandler(object):

    def __init__(self):
        pass

    def started(self, uuid: UUID, comment_id: int = None[int]):
        return

    def clone_repo(self, uuid: UUID, repo: Repo, local_path: str):
        return

    def retrieve_files(self, a_commit: str, b_commit: str):
        return

    def retrieve_file(self, file: str, commit: str):
        return

    def lint_file(self, linter: str, file: str):
        return

    def report(self, report: LintReport):
        return

    def finish(self):
        return
