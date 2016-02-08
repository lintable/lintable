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

import os
import tempfile
from typing import Iterable, Union

from git import Repo, Commit
from process_handler.process_handler import ProcessHandler


class GitHandler(object):
    """
    This is a class for interacting with a git repository.
    It should handle the following steps:
    started - Post constructor setup, this is largely to delegate to the ProcessHandler
    clone_repo - clone the repository at repo_url into the local_path/repo directory
    """

    def __init__(self, process_handler: ProcessHandler, repo_url: str, local_path: Union[None, str] = None):
        """
        :param process_handler: The ProcessHandler to delegate to for IO handling
        :param repo_url: The URL of the repository to clone
        :param local_path: The local path to store the cloned repository and the files pulled from the commits
        :return:
        """
        self.repo_url = repo_url
        self.repo = None
        self.files = []
        self.process_handler = process_handler
        self.uuid = process_handler.uuid
        self.last_merge = None
        self.previous_commit = None
        self.local_path = local_path if local_path else tempfile.mkdtemp()
        return

    @property
    def a_path(self):
        """
        The directory where files from commit a will be stored
        :return:
        """
        return os.path.join(self.local_path, 'a')

    @property
    def b_path(self):
        """
        The directory where files from commit b will be stored
        :return:
        """
        return os.path.join(self.local_path, 'b')

    @property
    def cloned_repo_path(self):
        """
        The directory where the cloned repo will be stored
        :return:
        """
        return os.path.join(self.local_path, 'repo')

    def started(self):
        """
        This is a stub function. It should be called after object creation so that any
        actual setup can be done and it allows the process handler to notify its delegates
        that the process has started.
        :return:
        """
        self.process_handler.started()
        return

    def clone_repo(self):
        """
        Clones a git repo and locates the last merge and previous commit.
        It will clone the repo into the local_path/repo.
        :return:
        """
        self.process_handler.clone_repo(self.cloned_repo_path)
        self.repo = Repo(path=self.repo_url)
        self.repo.clone(path=self.cloned_repo_path)
        self.last_merge = self.get_last_merge()
        self.previous_commit = self.repo.commit(
            '{commit}~1'.format(commit=self.last_merge))
        return

    def retrieve_changed_files_from_commit(self):
        """
        This retrieves the files that were changed during the last merge
        and its previous commit. Those files are stored into the a and b
        directories respectively.
        :return:
        """
        self.process_handler.retrieve_changed_file_set(self.last_merge,
                                                       self.previous_commit)
        os.mkdir(self.a_path)
        os.mkdir(self.b_path)
        a_files = list(self.last_merge.stats.files.keys())

        self.files = a_files
        self.pull_files_from_commit(self.last_merge, a_files, self.a_path)

        b_files = list(self.previous_commit.stats.files.keys())
        self.pull_files_from_commit(self.previous_commit, b_files, self.b_path)

        return

    def pull_files_from_commit(self, commit: Commit, files: Iterable[str],
                               path: str):
        """
        This pulls a iterable of files from a commit and stores them
        in the path.
        :param commit: The commit to pull from
        :param files: The files to pull.
        :param path: The directory path to save the pulled files to.
        :return:
        """
        for filename in files:
            # this will pull out the given filename from a commit by its sha1
            contents = self.repo.git.show(
                '{sha1}:{filename}'.format(sha1=commit.hexsha,
                                           filename=filename))
            file = os.path.join(path, filename)
            self.process_handler.retrieve_file_from_commit(filename, commit)
            dir_path = os.path.dirname(filename)

            # if the target directory doesn't exist, make it
            if dir_path and not os.path.exists(os.path.join(path, dir_path)):
                os.makedirs(os.path.join(path, dir_path))

            # save the file
            with open(file, 'w+') as output:
                output.write(contents)

        return

    def get_last_merge(self) -> Commit:
        """
        This gets the last merge in the repo.
        :return:
        """
        last_merge = self.repo.git.log('--merges', n=1, format='%H')

        return self.repo.commit(last_merge)
