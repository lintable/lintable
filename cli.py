import logging
import sys
from uuid import uuid4

from git_handler.git_handler import GitHandler
from lintball.lint_report import LintReport
from lintball.lintball import lint_process
from process_handler.log_handler import LogHandler
from process_handler.process_handler import ProcessHandler


def about():
    print('Lintable - A RESTful linting framework\nCopyright 2016 Capstone Team G')
    return -1


def parse_args():
    git_repo = sys.argv[1]

    return git_repo


def print_report(lint_report: LintReport):
    num_of_files = len(lint_report.errors)
    files_with_errors = dict((filename, errors) for filename, errors in lint_report.errors.items() if len(errors) > 0)

    print('Total number of files processed: {nof}\t Files with errors: {fwe}'.format(nof=num_of_files,
                                                                                     fwe=len(files_with_errors)))
    for f, e in lint_report.errors.items():
        if len(e) > 0:
            print('File {file} contains $errors errors.'.format(file=f, e=len(e)))
            for l, c, m in e:
                print('[{line}, {column}] - {message}'.format(line=l, column=c, message=m))
        else:
            print('{file} contained no errors.'.format(file=f))

    return 0


def entry():
    if len(sys.argv) < 2:
        return about()
    else:
        git_repo = parse_args()

        logger = logging.getLogger()
        logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        logger.setLevel('INFO')

        logger.info('hello world')
        process_handler = ProcessHandler(logger=LogHandler(logger=logger), uuid=uuid4(), repo=git_repo)

        git_handler = GitHandler(process_handler, git_repo)

        lint_process(git_handler, process_handler)

        return 0


if __name__ == '__main__':
    sys.exit(entry())
