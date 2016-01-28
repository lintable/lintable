from uuid import UUID

from git import Commit

from lintball.lint_report import LintReport
from process_handler.do_nothing_handler import DoNothingHandler
from process_handler.process_state import ProcessState


class ProcessHandler(object):
    def __init__(self, uuid: UUID, repo: str, logger=DoNothingHandler(),
                 commenter=DoNothingHandler(), db=DoNothingHandler()):
        self.state = ProcessState.STARTED
        self.uuid = uuid
        self.repo = repo
        self.logger = logger
        self.commenter = commenter
        self.db = db
        self.a_commit = None[str]
        self.b_commit = None[str]
        self.path = None[str]
        self.files = []
        self.comment_id = self.commenter.started(uuid=self.uuid)
        self.logger.started(uuid=self.uuid, comment_id=self.comment_id)
        self.db.started(uuid=self.uuid, comment_id=self.comment_id)

    def clone_repo(self, local_path: str):
        self.state = ProcessState.CLONE_REPO
        self.path = local_path
        self.logger.clone_repo(self.uuid, self.repo, local_path)
        self.commenter.clone_repo(self.uuid, self.repo, local_path)
        self.db.clone_repo(self.uuid, self.repo, local_path)
        return

    def retrieve_files(self, a_commit: str, b_commit: str):
        self.state = ProcessState.RETRIEVE_FILES
        self.a_commit = a_commit
        self.b_commit = b_commit
        self.logger.retrieve_files(self.uuid, a_commit, b_commit)
        self.commenter.retrieve_file(self.uuid, a_commit, b_commit)
        self.db.retrieve_files(self.uuid, a_commit, b_commit)
        return

    def retrieve_file(self, file: str, commit: Commit):
        self.files.append(file)
        self.logger.retrieve_file(self.uuid, file, commit)
        self.commenter.retrieve_file(self.uuid, file, commit)
        self.db.retrieve_file(self.uuid, file, commit)
        return

    def lint_file(self, linter: str, file: str = None):
        self.state = ProcessState.LINT_FILES
        self.logger.lint_file(self.uuid, linter, file)
        self.commenter.lint_file(self.uuid, linter, file)
        self.db.lint_file(self.uuid, linter, file)
        return

    def report(self, report: LintReport):
        self.state = ProcessState.REPORT
        self.logger.report(report)
        self.commenter.report(report)
        self.db.report(self.uuid, report)
        return

    def finish(self):
        self.state = ProcessState.FINISHED
        self.logger.finish(self.uuid)
        self.commenter.finish(self.uuid)
        self.db.finish(self.uuid)
        return
