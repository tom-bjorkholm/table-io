#! /usr/bin/env python3
"""Run all example programs and generate files in example/result."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import os
from pathlib import Path
import shutil
import subprocess
import sys


def _project_root() -> Path:
    """Return project root path from custom_build_tools/src folder."""
    return Path(__file__).resolve().parents[2]


def _example_env(project_root: Path) -> dict[str, str]:
    """Build env with example/src on PYTHONPATH."""
    env = dict(os.environ)
    example_src = str(project_root / 'example' / 'src')
    existing = env.get('PYTHONPATH', '')
    if existing:
        env['PYTHONPATH'] = example_src + os.pathsep + existing
    else:
        env['PYTHONPATH'] = example_src
    return env


def run_examples() -> None:
    """Run every python example script with all supported output formats."""
    project_root = _project_root()
    source_dir = project_root / 'example' / 'src' / 'example'
    result_dir = project_root / 'example' / 'result'
    shutil.rmtree(result_dir, ignore_errors=True)
    result_dir.mkdir(parents=True, exist_ok=True)
    env = _example_env(project_root)
    for source_file in sorted(source_dir.glob('e*.py')):
        output_base = result_dir / source_file.stem
        command = [
            sys.executable,
            '-m', f'example.{source_file.stem}',
            '-f',
            'all',
            '--implementation', 'all',
            '-o',
            str(output_base)]
        process = subprocess.run(
            command, check=False, cwd=project_root,
            env=env)
        if process.returncode == 0:
            continue
        raise RuntimeError(
            f'Example failed: {source_file} exit code {process.returncode}'
        )


if __name__ == '__main__':
    run_examples()
