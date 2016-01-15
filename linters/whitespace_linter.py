from typing import List, Dict

import re

ws_regex = re.compile("(\.)*(\s+)")

# see this for the gory details, I'm going to cover the most probable
# https://en.wikipedia.org/wiki/Newline
# UNIX style line breaks, only a newline
lf_regex = re.compile("(\.*)\n")
# Windows style line breaks, carraige return followed by a newline
cr_lf_regex = re.compile("(\.*)\r\n")
# MacOS 9 and earlier
cr_regex = re.compile("(\.*)\r")


def lint_file(file: str, eol: str = lf_regex)-> List[Dict]:
    total_matches = []
    lines = eol.split(file)[1:]
    line_number = 1
    for line in lines:
        total_matches.append(has_trailing_whitespace(line_number, line))
        line_number += 1

    return total_matches


def lint_patch(lines: List[(int, str)])-> List[Dict]:
    total_matches = []
    for line_number, line in lines:
        assert isinstance(line, str)
        total_matches.append(line_number, line)
    return total_matches


def has_trailing_whitespace(line_number: int, line: str)-> List[Dict]:
    split = ws_regex.split(line)
    if len(split) > 1:
        return [dict(line_number=line_number,
                     column=len(split[0]),
                     match=split[-2])]
    else:
        return []
