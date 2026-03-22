
"""Repository-specific build specification for common_build_tools."""

from typing import Optional
import sys
from pathlib import Path
from build_spec import BuildSpec
CUSTOM_BUILD_TOOLS_SRC = Path(__file__).resolve().parent / 'src'

sys.path.insert(0, str(CUSTOM_BUILD_TOOLS_SRC))
# pylint: disable=wrong-import-position,import-error
from hooks import run_examples_hook

def custom_spec() -> Optional[BuildSpec]:
    """Return custom build spec for this repository."""
    return BuildSpec(
        additional_venv_packages=[],
        custom_after_test=[run_examples_hook],
    )
