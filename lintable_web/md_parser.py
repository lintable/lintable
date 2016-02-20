"""Provides utility methods for handling the different database Models."""

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

import markdown
import codecs

class MarkDownParser(object):
    """Provides utility method for parsing markdown files for use in html templates."""

    @staticmethod
    def parse_md_file(filename: str):
        input_file = codecs.open(filename, mode="r", encoding="utf-8")
        text = input_file.read()
        html = markdown.markdown(text)
        return html
