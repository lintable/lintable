import json
from functools import partial
from typing import List
from uuid import uuid4, UUID

from calc.runner import runner
from git.github import github_pull_hook


@runner.task(serializer='json')
def lint_github(payload: json, task_id=uuid4()):
    github = github_pull_hook(task_id, payload)

    lintball(github, task_id)

    return


def lintball(git: (partial, partial, partial), task_id: UUID):
    retrieve_files, ab_files, process_results = git

    retrieve_files()

    ab_results = {}

    for filename, a, b in ab_files:
        a_results = lint(a)
        b_results = lint(b)
        ab_results[filename] = [results for results in b_results if results not in a_results]

    return process_results(results=ab_results)


def lint(file: str)-> List[(int, int, str)]:
    return []