import typing

LintError = typing.NamedTuple('LintError', [('line_number', int), ('column', int), ('msg', str)])