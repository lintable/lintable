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
import os
import tempfile
import unittest
from uuid import uuid4

import sys

from git import Commit, Repo
import rstr

from git_handler import GitHandler
from process_handler.process_handler import ProcessHandler

logging.basicConfig(filename='./git_handler_tests.log', level=logging.DEBUG)


class GitHandlerTests(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger('test_git_handler')
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.tmp_repo = tempfile.TemporaryDirectory()

        self.logger.debug('Temporary directory for test git repo: {dir}'.format(dir=self.tmp_repo))

        self.repo = Repo.init(path=self.tmp_repo.name)

        a_file = os.path.join(self.tmp_repo.name, 'a_file.txt')
        b_file = os.path.join(self.tmp_repo.name, 'b_file.txt')

        # create files a and b

        self.create_random_text_file(a_file)
        self.create_random_text_file(b_file)

        self.logger.debug('files in dir: {files}'.format(files=os.listdir(self.tmp_repo.name)))

        # then commit them as commit b
        self.commit_b = self.commit_files(b_file, msg='commit b')

        # modify file a
        self.modify_random_text_file(a_file)

        # commit file a as commit a
        self.commit_a = self.commit_files(a_file, msg='commit a')

        self.git_handler = GitHandler(ProcessHandler(self.tmp_repo.name, uuid4()), self.tmp_repo.name)
        self.git_handler.started()

    def create_and_commit_file(self, filename: str):
        self.create_random_text_file(filename)
        self.repo.index.add(filename)
        self.repo.index.commit('commit of {filename}'.format(filename=filename))

    def commit_files(self, *args, **kwargs) -> Commit:
        msg = kwargs['msg']
        files = args

        self.logger.debug('adding {file} to commit'.format(file=files))
        self.repo.index.add(items=files)

        return self.repo.index.commit(message=msg)

    def create_random_text_file(self, filename: str):
        content = ''

        for x in range(1, 10):
            content += rstr.letters(0, 79)
            content += '\n'

        with open(filename, 'w+') as generated_file:
            generated_file.write(content)

    def modify_random_text_file(self, filename: str):
        os.remove(filename)

        self.create_random_text_file(filename)

    def test_clone_repo(self):
        self.logger.debug('Testing git_handler.clone_repo')
        self.git_handler.clone_repo()
        self.logger.debug('{dir} contains {files}'.format(dir=self.tmp_repo.name, files=os.listdir(self.tmp_repo.name)))
        self.logger.debug('{dir} contains {files}'.format(dir=os.path.join(self.git_handler.local_path, 'repo'),
                                                          files=os.listdir(
                                                              os.path.join(self.git_handler.local_path, 'repo'))))
        # assert that the original repo and the cloned repo have the same files
        self.assertListEqual(os.listdir(self.tmp_repo.name),
                             os.listdir(os.path.join(self.git_handler.local_path, 'repo')))


if __name__ == '__main__':
    unittest.main()
