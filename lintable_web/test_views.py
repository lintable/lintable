"""Tests for the lintable_web views."""

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

import unittest

from lintable_settings.settings import LINTWEB_SETTINGS
from lintable_web import app

class ViewsTests(unittest.TestCase):
    """Tests for the lintable_web views."""

    def setUp(self):
        """Set up the tests."""

        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        """Finish the tests."""

        pass

    def test_index_status_code(self):
        """Make sure that the homepage returns status 200."""

        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_register_status_code(self):
        """Make sure that the register page returns status 302 or 404."""

        result = self.app.get('/register')

        if not LINTWEB_SETTINGS['DEBUG']:
            self.assertEqual(result.status_code, 302)
        else:
            self.assertEqual(result.status_code, 404)

    def test_callback_status_code(self):
        """Make sure that the callback page returns status 302 or 404."""

        result = self.app.get('/callback')

        if not LINTWEB_SETTINGS['DEBUG']:
            self.assertEqual(result.status_code, 200)
        else:
            self.assertEqual(result.status_code, 404)
