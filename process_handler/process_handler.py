from uuid import UUID

from git import Repo

from git import Commit

from lintball.lint_report import LintReport
from process_handler.do_nothing_handler import DoNothingHandler
from process_handler.process_state import ProcessState


class ProcessHandler(object):
    def __init__(self, uuid: UUID, repo: Repo, logger=DoNothingHandler(),
                 commenter=DoNothingHandler(), db=DoNothingHandler()):
        self.state = ProcessState.STARTED
        self.uuid = uuid
        self.repo = repo
        self.logger = logger
        self.commenter = commenter
        self.db = db
        self.a_commit = None
        self.b_commit = None
        self.local_path = None
        self.files = []
        self.comment_id = None

    def started(self):
        self.comment_id = self.commenter.started(uuid=self.uuid)
        self.logger.started(uuid=self.uuid, comment_id=self.comment_id)
        self.db.started(uuid=self.uuid, comment_id=self.comment_id)

    def clone_repo(self, local_path: str):
        self.state = ProcessState.CLONE_REPO
        self.local_path = local_path
        self.logger.clone_repo(self.uuid, self.repo, local_path)
        self.commenter.clone_repo(self.uuid, self.repo, local_path)
        self.db.clone_repo(self.uuid, self.repo, local_path)
        return

    def retrieve_changed_file_set(self, a_commit: Commit, b_commit: Commit):
        self.state = ProcessState.RETRIEVE_FILES
        self.a_commit = a_commit
        self.b_commit = b_commit
        self.logger.retrieve_changed_file_set(self.uuid, a_commit, b_commit)
        self.commenter.retrieve_changed_file_set(self.uuid, a_commit, b_commit)
        self.db.retrieve_changed_file_set(self.uuid, a_commit, b_commit)
        return

    def retrieve_file_from_commit(self, file: str, commit: Commit):
        self.files.append(file)
        self.logger.retrieve_file_from_commit(self.uuid, file, commit)
        self.commenter.retrieve_file_from_commit(self.uuid, file, commit)
        self.db.retrieve_file_from_commit(self.uuid, file, commit)
        return

    def lint_file(self, linter: str, file: str):
        self.state = ProcessState.LINT_FILES
        self.logger.lint_file(self.uuid, linter, file)
        self.commenter.lint_file(self.uuid, linter, file)
        self.db.lint_file(self.uuid, linter, file)
        return

    def report(self, report: LintReport):
        self.state = ProcessState.REPORT
        self.logger.report(self.uuid, report)
        self.commenter.report(self.uuid, report)
        self.db.report(self.uuid, report)
        return

    def finish(self):
        self.state = ProcessState.FINISHED
        self.logger.finish(self.uuid)
        self.commenter.finish(self.uuid)
        self.db.finish(self.uuid)
        return
