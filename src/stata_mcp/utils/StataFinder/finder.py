#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 - Present Sepine Tam, Inc. All Rights Reserved
#
# @Author : Sepine Tam
# @Email  : sepinetam@gmail.com
# @File   : finder.py

import os
import glob
import dotenv

import platform
from typing import Dict, Callable, Any, Optional

from .windows import *

dotenv.load_dotenv()


def _stata_version_windows(driver: str = "C:\\"):
    stata_paths = []
    common_patterns = [
        os.path.join(driver, "Program Files", "Stata*", "*.exe"),
        os.path.join(driver, "Program Files(x86)", "Stata*", "*.exe")
    ]
    for pattern in common_patterns:
        try:
            matches = glob.glob(pattern)
            for match in matches:
                if "stata" in match.lower() and match.lower().endswith(".exe"):
                    stata_paths.append(match)

            if not stata_paths:
                for root, dirs, files in os.walk(driver):
                    if root.count(os.sep) - driver.count(os.sep) > 3:
                        dirs.clear()
                        continue

                    for file in files:
                        if file.lower().endswith(".exe") and "stata" in file.lower():
                            stata_paths.append(os.path.join(root, file))

        except Exception as e:
            pass

    return stata_paths


def _find_stata_macos() -> str | None:
    """Locate the Stata CLI on macOS systems.

    This implementation searches ``/usr/local/bin`` for common Stata binary
    names in order of preference. If ``is_env`` is ``True`` the environment
    variable ``stata_cli`` will be consulted with the discovered path as the
    fallback value.
    """
    search_dir = "/usr/local/bin"
    variants = ["stata-mp", "stata-se", "stata-be"]

    found_cli = None
    for variant in variants:
        candidate = os.path.join(search_dir, variant)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            found_cli = candidate
            break
        return os.getenv("stata_cli", found_cli)

    return found_cli


def __default_stata_cli_path_windows() -> Any | None:
    drives: list = get_available_drives()
    stata_cli_path_list: list = []
    for drive in drives:
        stata_cli_path_list += _stata_version_windows(drive)
    if len(stata_cli_path_list) == 0:
        return None
    elif len(stata_cli_path_list) == 1:
        return stata_cli_path_list[0]
    else:
        for path in stata_cli_path_list:
            if windows_stata_match(path):
                return path
            else:
                pass
        return stata_cli_path_list[0]


def _find_stata_windows() -> str:
    _stata_cli_path = None
    __default_cli_path = __default_stata_cli_path_windows()
    _stata_cli_path = __default_cli_path
    return _stata_cli_path

def __default_stata_cli_path_linux() -> Any | None:
    pass


def _find_stata_linux() -> str:
    """
    Find the Stata CLI path on Linux systems.
    For Linux users, this function attempts to locate the Stata CLI executable.

    Returns:
        The path to the Stata CLI executable, or None if not found.
    """
    default_path = __default_stata_cli_path_linux()
    return os.getenv("stata_cli", default_path)


_OS_FINDERS: dict[str, Callable[[], str]] = {
    "Darwin": _find_stata_macos,
    "Windows": _find_stata_windows,
    "Linux": _find_stata_linux,
}


def find_stata(os_name: Optional[str] = None, is_env: bool = True):
    if is_env:
        stata_cli = os.getenv("stata_cli", None)
        if stata_cli:
            return stata_cli

    current_os = os_name or platform.system()
    finder = _OS_FINDERS.get(current_os)
    if not finder:
        raise RuntimeError(f"Unsupported OS: {current_os!r}")

    return finder()


if __name__ == "__main__":
    sys_os = platform.system()
    if sys_os == "Darwin":
        stata_cli = _find_stata_macos()
        print(stata_cli)
    elif sys_os == "Windows":
        _stata_version_windows()
    else:
        print("Hello Stata-MCP, Install it please~")
