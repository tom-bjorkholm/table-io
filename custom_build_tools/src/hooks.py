#! /usr/bin/env python3
"""Thin build hook wrappers for this repository.

These wrappers stay in a separate module because ``custom_spec.py`` is loaded
early in the build flow, before the project virtual environment exists and
before its extra packages have been installed. The real hook scripts therefore
need to be launched later with the venv Python instead of being imported
directly from ``custom_spec.py``.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import os
from pathlib import Path
import subprocess
import sys

COMMON_BUILD_TOOLS_SRC = (
    Path(__file__).resolve().parents[2] / 'common_build_tools' / 'src'
)
sys.path.insert(0, str(COMMON_BUILD_TOOLS_SRC))
# pylint: disable=wrong-import-position,import-error
from build_spec import (  # noqa: E402
    BuildInformation,
    BuildSpec,
)


def _venv_python(project_root: Path) -> Path:
    """Return venv Python path for current platform."""
    if os.name == 'nt':
        return project_root / 'venv' / 'Scripts' / 'python.exe'
    return project_root / 'venv' / 'bin' / 'python'


# custom_spec.py is imported before the project venv exists and before its
# extra packages are installed, so the real hook modules must be executed later
# with the venv interpreter instead of being imported directly there.
def _run_script_with_venv(script_file: Path, project_root: Path) -> None:
    """Run one script file with venv Python and fail on non-zero exit."""
    command = [str(_venv_python(project_root)), str(script_file)]
    process = subprocess.run(command, check=False, cwd=project_root)
    if process.returncode == 0:
        return
    raise RuntimeError(
        f'Custom hook script failed: {script_file} '
        f'(exit code {process.returncode}).')


def _run_custom_script(build_information: BuildInformation,
                       script_name: str) -> None:
    """Run one script from custom_build_tools/src with the venv Python."""
    project_root = Path(build_information['project_root'])
    script_file = project_root / 'custom_build_tools' / 'src' / script_name
    _run_script_with_venv(script_file, project_root)


def run_examples_hook(build_spec: BuildSpec,
                      build_information: BuildInformation) -> None:
    """Run all example programs."""
    _ = build_spec
    _run_custom_script(build_information, 'run_examples.py')
