import logging
import os
from typing import Iterable

from flask import json

from git import Repo, Commit
from process_handler.process_handler import ProcessHandler

join = os.path.join

temp_path = '/tmp/{uuid}'

logger = logging.getLogger(__name__)


class GitHandler(object):
    def __init__(self, handler: ProcessHandler, repo_url: str,
                 branch: str = 'master'):
        self.repo_url = repo_url
        self.repo = None[str]
        self.files = []
        self.branch = branch
        self.publisher = handler
        self.uuid = handler.uuid
        self.last_merge = None[Repo]
        self.previous_commit = None[Repo]
        self.local_path = temp_path.format(self.uuid)
        return

    def clone_repo(self):
        self.publisher.clone_repo(self.local_path)
        self.repo = Repo(path=self.repo_url)
        self.repo.clone(path=join(self.local_path, 'repo'))
        self.last_merge = self.get_last_merge()
        self.previous_commit = self.repo.commit(
            '{commit}~1'.format(commit=self.last_merge))
        return

    def retrieve_files(self):
        self.publisher.retrieve_files(str(self.last_merge),
                                      str(self.previous_commit))
        os.mkdir(join(self.local_path, 'a'))
        os.mkdir(join(self.local_path, 'b'))
        a_files = list(self.last_merge.stats.files.keys())
        self.files = a_files
        self.pull_files_from_commit(self.last_merge, a_files,
                                    join(self.local_path, 'a'))
        b_files = list(self.previous_commit.stats.files.keys())
        self.pull_files_from_commit(self.previous_commit, b_files,
                                    join(self.local_path, 'b'))

        return

    def pull_files_from_commit(self, commit: Commit, files: Iterable[str],
                               path: str):
        for filename in files:
            contents = self.repo.git.show(
                '{sha1}:{filename}'.format(sha1=commit.hexsha,
                                           filename=filename))
            file = join(path, filename)
            self.publisher.retrieve_file(filename, commit)
            dir_path = os.path.dirname(filename)

            if dir_path and not os.path.exists(join(path, dir_path)):
                os.makedirs(join(path, dir_path))

            with open(file, 'w+') as output:
                output.write(contents)

        return

    def get_last_merge(self) -> Commit:
        last_merge = self.repo.git.log('--merges', n=1, format='%H')

        return self.repo.commit(last_merge)

