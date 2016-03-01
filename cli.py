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

import logging
import sys
from uuid import uuid4

import click

from lintable_git.git_handler import GitHandler
from lintable_lintball.lintball import lint_process
from lintable_processes.log_handler import LogHandler
from lintable_processes.process_handler import ProcessHandler


def about():
    # TODO: Make a proper about printout, including licencing and command line options
    """
    Prints out a basic about statement.
    :return:
    """
    print('Lintable - A RESTful linting framework\nCopyright 2016 Capstone Team G')
    return -1


def parse_args():
    """
    Parse the command line arguments.
    This currently takes the first argument and assumes it's a valid git url
    :return: str - the location of the git repository
    """
    git_repo = sys.argv[1]

    return git_repo


@click.command()
@click.option('--commit_a', '-a', default='HEAD', type=str)
@click.option('--commit_b', '-b', default='HEAD~1', type=str)
@click.argument('repo', type=click.Path(file_okay=False, exists=True))
def entry(repo: sys.path, commit_a: str, commit_b: str):
    """
    This is the main entry point.
    It should be called if there is at least one command line argument
    to indicate where the git repo is.
    It then setups a log handler, a git handler and
    sends them to lint_process
    :param repo: the path of the repository to be linted
    :param commit_a: the commit to be comapred with, defaults to HEAD
    :param commit_b: the commit to be comapred against, defaults to HEAD~1
    :return: int - Should return a 0 to indicate this was a success.
    """
    if len(sys.argv) < 2:
        return about()
    else:
        # get the git repo from the command line arguments
        git_repo = repo

        # setup a logger to log the output
        logger = logging.getLogger()
        logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        logger.setLevel('INFO')

        # create a process handler that delegates to the logger
        process_handler = ProcessHandler(handlers=[LogHandler(logger=logger)], uuid=uuid4(), repo=git_repo)

        # create a git handler to clone the repo and comapre the two commits
        git_handler = GitHandler(process_handler, git_repo, commit_a, commit_b)

        # process the results from the git handler via the linters
        lint_process(git_handler, process_handler)

        return 0


if __name__ == '__main__':
    sys.exit(entry())
