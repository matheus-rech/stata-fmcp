#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 - Present Sepine Tam, Inc. All Rights Reserved
#
# @Author : Sepine Tam (谭淞)
# @Email  : sepinetam@gmail.com
# @File   : _command.py

from typing import List, Set

# Commands that are forbidden to execute unless dangerous mode is enabled in environment variables
DENY_COMMAND: Set[str] = {
    "!", "shell"
}

# Dangerous pattern matching strings - used for regular expressions
DANGEROUS_PATTERNS: List[str] = []

# Suspicious file extensions
SUSPICIOUS_EXTENSIONS: Set[str] = {
    '.exe', '.bat', '.cmd', '.com', '.pif', '.scr',
    '.vbs', '.vbe', '.js', '.jse', '.wsf', '.wsh',
    '.msc', '.jar', '.app', '.deb', '.rpm', '.dmg',
}

# Commands that require confirmation before execution
ASK_COMMANDS: Set[str] = {
    "rm"
}

# Commands that are always allowed
ALLOWED_COMMANDS: Set[str] = {
    "reg", "gen"
}
