from logging import Logger
from uuid import UUID

from git import Commit, Repo

from lintball.lint_report import LintReport
from process_handler.do_nothing_handler import DoNothingHandler


class LogHandler(DoNothingHandler):

    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger

    def lint_file(self, uuid: UUID, linter: str, file: str):
        super().lint_file(uuid, linter, file)
        self.logger.info('Linting {file} with linter {linter}'.format(file=file, linter=linter))

    def retrieve_changed_file_set(self, uuid: UUID, a_commit: Commit, b_commit: Commit):
        super().retrieve_changed_file_set(uuid, a_commit, b_commit)
        self.logger.info('Retrieving files from {a_commit} and {b_commit}'.format(a_commit=a_commit, b_commit=b_commit))

    def report(self, uuid: UUID, report: LintReport):
        super().report(uuid, report)
        num_of_files = len(report.errors)
        files_with_errors = dict((filename, errors) for filename, errors in report.errors.items() if len(errors) > 0)

        self.logger.info('Total number of files processed: {nof}\t Files with errors: {fwe}'.format(nof=num_of_files,
                                                                                     fwe=len(files_with_errors)))
        for f, e in report.errors.items():
            if len(e) > 0:
                self.logger.info('File {file} contains $errors errors.'.format(file=f, e=len(e)))
                for l, c, m in e:
                    self.logger.info('[{line}, {column}] - {message}'.format(line=l, column=c, message=m))
            else:
                self.logger.info('{file} contained no errors.'.format(file=f))

    def started(self, uuid: UUID, comment_id: int = None):
        super().started(uuid, comment_id)
        self.logger.info('Starting linting process with id: {uuid}'.format(uuid=uuid))
        if type(comment_id) is int and comment_id >= 0:
            self.logger.debug('Comment id is {comment_id}'.format(comment_id=comment_id))

    def clone_repo(self, uuid: UUID, repo: Repo, local_path: str):
        super().clone_repo(uuid, repo, local_path)
        self.logger.info('Cloning repo {repo}'.format(repo=str(repo)))

    def retrieve_file_from_commit(self, uuid: UUID, file: str, commit: Commit):
        super().retrieve_file_from_commit(uuid, file, commit)
        self.logger.info('Retrieving {file} from {commit}'.format(file=file, commit=commit))
