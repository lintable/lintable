"""Handles interactions with a Git repo."""

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
import shutil
import tempfile

from typing import Iterable, List, Optional
from typing import Set

from urllib.parse import urlparse

from git import Repo, Commit

from lintable_processes.process_handler import ProcessHandler


class GitHandler(object):
    """Handles interactions with a Git repo.

    It should handle the following steps:
    started - Post constructor setup, this is largely to delegate to the ProcessHandler
    clone_repo - clone the repository at repo_url into the local_path/repo directory
    retrieve_files - pull the changes files from commit a and any corresponding files from commit b, storing them in path a and path b respectively
    """

    def __init__(self,
                 process_handler: ProcessHandler,
                 repo_url: str,
                 sha1_a: str,
                 sha1_b: str,
                 local_path: Optional[str] = None):
        """
        :param process_handler: The ProcessHandler to delegate to for IO handling
        :param repo_url: The URL of the repository to clone
        :param sha1_a: The sha1 in hex format of the commit to compare with
        :param sha1_b: The sha1 in hex format of the commit to compare against
        :param local_path: The local path to store the cloned repository and the files pulled from the commits
        :return:
        """

        self.process_handler = process_handler  # type: ProcessHandler
        self.repo_url = repo_url
        self.remote = urlparse(repo_url).scheme != ""  # type: bool
        self.uuid = process_handler.uuid
        self.sha1_a = sha1_a  # type: str
        self.sha1_b = sha1_b  # type: str
        self.commit_a = None  # type: Optional[Commit]
        self.commit_b = None  # type: Optional[Commit]
        self.repo = None  # type: Optional[Repo]
        self.files = []  # type: List[str]
        self.local_path = local_path if local_path else tempfile.mkdtemp()  # type: str
        return

    def __del__(self):
        shutil.rmtree(self.local_path)

    @property
    def a_path(self):
        """The directory where files from commit a will be stored.

        :return:
        """

        return os.path.join(self.local_path, 'a')

    @property
    def b_path(self):
        """The directory where files from commit b will be stored.

        :return:
        """

        return os.path.join(self.local_path, 'b')

    @property
    def cloned_repo_path(self):
        """The directory where the cloned repo will be stored.

        :return:
        """

        return os.path.join(self.local_path, 'repo')

    def started(self):
        """Stub function to handle notification of delegates.

        This is a stub function. It should be called after object creation so
        that any actual setup can be done and it allows the process handler to
        notify its delegates that the process has started.

        :return:
        """

        self.process_handler.started()
        return

    def clone_repo(self):
        """Clones a git repo and locates the last merge and previous commit.

        It will clone the repo into the local_path/repo.

        :return:
        """

        self.process_handler.clone_repo(self.local_path)

        if self.remote:
            self.repo = Repo.clone_from(url=self.repo_url, to_path=self.cloned_repo_path)
        else:
            self.repo = Repo(path=self.repo_url)
            self.repo.clone(path=self.cloned_repo_path)

        self.commit_a = self.repo.commit(self.sha1_a)
        self.commit_b = self.repo.commit(self.sha1_b)
        return

    def retrieve_changed_files_from_commit(self):
        """Gets the files changed between the last merge and previous commit.

        Those files are stored into the a and b directories respectively.

        :return:
        """

        self.process_handler.retrieve_changed_file_set(self.commit_a,
                                                       self.commit_b)
        os.mkdir(self.a_path)
        os.mkdir(self.b_path)

        # get the files that were added or modified between commit b and commit a
        a_files, b_files = self.get_files_changed_between_commits(self.commit_a, self.commit_b)

        # note which files we are checking
        self.files = a_files

        # pull the file contents out from commit a and store them in path a
        self.pull_files_from_commit(self.commit_a, a_files, self.a_path)

        # pull the file contents out from commit b and store them in path b
        self.pull_files_from_commit(self.commit_b, b_files, self.b_path)

        return

    def pull_files_from_commit(self, commit: Commit, files: Iterable[str],
                               path: str):
        """Pulls a iterable of files from a commit and stores them in the path.

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

    @staticmethod
    def get_files_changed_between_commits(commit_a: Commit, commit_b: Commit)-> (Set[str], Set[str]):
        """Determine what files have been added or modified between commits b and a
        Those files should be added to a_files and if they are present in commit b,
        added to b_files

        :param commit_a:
        :param commit_b:
        :return: a pair of sets, the first set is the files in commit a
        the second set is the files in commit b
        ":rtype (Set[str], Set[str]):
        """

        diffs = commit_b.diff(other=commit_a)

        a_files = set()  # type: Set[str]
        b_files = set()  # type: Set[str]

        for diff in diffs:
            if diff.new_file or (diff.a_blob and diff.b_blob and diff.a_blob != diff.b_blob):
                a_files.add(diff.a_path)
                if not diff.new_file:
                    b_files.add(diff.b_path)

        return a_files, b_files

    def get_last_merge(self) -> Commit:
        """Gets the last merge in the repo.

        :return Commit:
        """

        last_merge = self.repo.git.log('--merges', n=1, format='%H')

        return self.repo.commit(last_merge)
