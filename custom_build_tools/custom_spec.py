
"""Repository-specific build specification for common_build_tools."""

from typing import Optional
import sys
from pathlib import Path
from build_spec import BuildSpec
CUSTOM_BUILD_TOOLS_SRC = Path(__file__).resolve().parent / 'src'

sys.path.insert(0, str(CUSTOM_BUILD_TOOLS_SRC))
# pylint: disable=wrong-import-position,import-error
from hooks import run_examples_hook  # noqa: E402


def custom_spec() -> Optional[BuildSpec]:
    """Return custom build spec for this repository."""
    # The example tests import shared test helpers from test/test_tableio
    # (as package test_tableio), see example/test/conftest.py.
    return BuildSpec(additional_venv_packages=['openxml-audit >= 0.8.0',
                                               'python-calamine >= 0.8.2',
                                               'odfpy >= 1.4.1'],
                     custom_after_test=[run_examples_hook],
                     mypy_paths=[Path('test')])
