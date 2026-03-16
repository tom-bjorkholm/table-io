#! /usr/local/bin/python3
"""Check that the captured stdout and stderr are as expected."""

from typing import Optional
from pytest import CaptureFixture


def check_capsys(capsys: CaptureFixture[str],
                 stdout: Optional[list[str]] = None,
                 stderr: Optional[list[str]] = None) -> None:
    """Check that the captured stdout and stderr are as expected.

    Args:
        capsys: The captured stdout and stderr.
        stdout: The expected stdout. If None, the stdout must be empty.
        stderr: The expected stderr. If None, the stderr must be empty.
    """
    out, err = capsys.readouterr()
    if not stdout:
        assert out == ''
    else:
        for line in stdout:
            assert line in out
    if not stderr:
        assert err == ''
    else:
        for line in stderr:
            assert line in err
