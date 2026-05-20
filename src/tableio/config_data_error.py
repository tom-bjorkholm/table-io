#! /usr/local/bin/python3
"""Structured errors for framework-neutral TableIO configuration."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from dataclasses import dataclass
from typing import Optional


@dataclass
class ConfigIssue:
    """One validation issue for a TableIO configuration.

    The issue name is the dotted user-facing configuration parameter name.
    This lets applications and adapter libraries point diagnostics at the
    same names that appear in configuration files and documentation.
    """

    name: str
    """The dotted configuration parameter name, for example ``csv.quoting``."""

    message: str
    """The human-readable validation message for this parameter."""


class ConfigError(ValueError):
    """Raised when TableIO configuration validation fails.

    The ``issues`` attribute contains all validation issues that could be
    found in one pass. ``str(error)`` is intended to be suitable as a compact
    user-facing summary, while ``issues`` is intended for applications and
    adapter libraries that want to attach messages to individual
    configuration fields.
    """

    issues: tuple[ConfigIssue, ...]
    """The validation issues that caused the exception."""

    def __init__(self, issues: tuple[ConfigIssue, ...],
                 message: Optional[str] = None) -> None:
        """Initialize the configuration validation error.

        Args:
            issues: One or more structured validation issues.
            message: Optional summary message for the whole configuration.
        """
        self.issues = issues
        if message is None:
            message = 'Invalid TableIO configuration'
        if issues:
            issue_text = '; '.join(
                f'{issue.name}: {issue.message}' for issue in issues)
            message = f'{message}: {issue_text}'
        super().__init__(message)
