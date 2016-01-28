from enum import Enum


class ProcessState(Enum):
    STARTED = 1,
    CLONE_REPO = 2,
    RETRIEVE_FILES = 3,
    LINT_FILES = 4,
    REPORT = 5,
    FINISHED = 6
