from typing import List, Dict

import re

from lintball.lint_error import LintError

ws_regex = re.compile("(\.)*(\s+)")

# see this for the gory details, I'm going to cover the most probable
# https://en.wikipedia.org/wiki/Newline
# UNIX style line breaks, only a newline
lf_regex = re.compile("(\.*)\n")
# Windows style line breaks, carraige return followed by a newline
cr_lf_regex = re.compile("(\.*)\r\n")
# MacOS 9 and earlier
cr_regex = re.compile("(\.*)\r")

linter_name = 'Trailing WhiteSpace Linter'


def lint_file(file: str, eol: str = lf_regex)-> List[LintError]:
    total_matches = []

    lines = eol.split(file)[1:]

    line_number = 1

    for line in lines:
        total_matches.append(has_trailing_whitespace(line_number, line))
        line_number += 1

    return total_matches


def lint_patch(lines: List[(int, str)])-> List[LintError]:
    total_matches = []

    for line_number, line in lines:
        assert isinstance(line, str)
        total_matches.append(has_trailing_whitespace(line_number, line))

    return total_matches


def has_trailing_whitespace(line_number: int, line: str)-> List[LintError]:
    split = ws_regex.split(line)

    if len(split) > 1:
        return [LintError(line_number=line_number,
                          column=len(split[0]),
                          msg='Found trailing whitespace \'$ws\''.format(ws=split[-2]))]
    else:
        return []
