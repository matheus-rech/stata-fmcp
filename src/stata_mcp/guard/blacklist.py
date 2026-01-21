#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 - Present Sepine Tam, Inc. All Rights Reserved
#
# @Author : Sepine Tam (谭淞)
# @Email  : sepinetam@gmail.com
# @File   : blacklist.py

"""Stata dofile security blacklist definitions.

This module defines dangerous commands and patterns that should be blocked
when executing Stata dofiles, unless dangerous mode is explicitly enabled.
"""

from typing import List, Set

# ============================================================================
# Dangerous Commands
# ============================================================================

#: Commands that allow execution of shell/system commands
DANGEROUS_COMMANDS: Set[str] = {
    "!",          # Unix-style shell escape: !ls
    "shell",      # Shell command execution: shell dir
    "winexec",    # Windows program execution: winexec notepad.exe
    "unixcmd",    # Unix command execution: unixcmd ls
    "macro",      # Macro manipulation (can be dangerous in certain contexts)
}


# ============================================================================
# Dangerous Patterns (Regular Expressions)
# ============================================================================

#: Patterns that may indicate dangerous operations
DANGEROUS_PATTERNS: List[str] = [
    r"!\s*\w+",           # Shell escape with command: ! ls, !dir
    r"shell\s+\w+",       # Shell command: shell dir, shell ls
    r"winexec\s+\S+",     # Windows execution: winexec program.exe
    r"unixcmd\s+\w+",     # Unix command: unixcmd ls
    r"erase\s+.*",        # File deletion: erase file.dta
    r"rm\s+.*",           # File deletion (alias): rm file.dta
]


# ============================================================================
# Metadata
# ============================================================================

__all__ = [
    "DANGEROUS_COMMANDS",
    "DANGEROUS_PATTERNS",
]
