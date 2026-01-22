#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 - Present Sepine Tam, Inc. All Rights Reserved
#
# @Author : Sepine Tam (谭淞)
# @Email  : sepinetam@gmail.com
# @File   : config.py

import os
import platform
import sys
import tomllib
from pathlib import Path
from typing import Dict

from .core.stata import StataFinder


class Config:
    def __init__(self, config_file: Path = None):
        self.config_file = config_file or self.STATA_MCP_DIRECTORY / "config.toml"

    @property
    def config(self) -> Dict:
        try:
            with open(self.config_file, "rb") as f:
                config = tomllib.load(f)
        except Exception:
            config = {}
        return config

    def _get_config_value(self, config_keys: list, env_var: str, default, converter=None, validator=None):
        """
        Generic configuration reading method with priority: environment variable > toml config file > default value

        Args:
            config_keys: Key path in config file, e.g. ["DEBUG", "logging", "MAX_BYTES"]
            env_var: Environment variable name
            default: Default value
            converter: Value conversion function, e.g. bool, int, Path, etc.
            validator: Validation function that accepts the converted value, returns True if valid

        Returns:
            Configuration value (processed by converter and validator)
        """
        # 1. Read from environment variable first
        value = os.getenv(env_var, None)  # str | None

        # 2. If no environment variable, read from config file
        if value is None:
            config_dict = self.config
            for key in config_keys[:-1]:
                config_dict = config_dict.get(key, {})
                if not isinstance(config_dict, dict):
                    config_dict = {}
                    break

            if isinstance(config_dict, dict):
                value = config_dict.get(config_keys[-1], None)  # str | bool | dict | list | int | float | None

        # 3. If still no value, return default
        if value is None:
            return default

        # 4. Convert value
        if converter is not None:
            try:
                value = converter(value)
            except (ValueError, TypeError):
                return default

        # 5. Validate value
        if validator is not None and not validator(value):
            return default

        return value

    @staticmethod
    def _to_bool(value):
        """Convert value to boolean."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() == "true"
        return bool(value)

    @staticmethod
    def _to_int(value):
        """Convert value to integer."""
        return int(value)

    @staticmethod
    def _to_path(value):
        """Convert value to Path object."""
        return Path(value).expanduser().absolute()

    @property
    def STATA_MCP_DIRECTORY(self) -> Path:
        base_dir = Path.home() / ".statamcp"
        base_dir.mkdir(parents=True, exist_ok=True)
        return base_dir

    @property
    def IS_DEBUG(self) -> bool:
        return self._get_config_value(
            config_keys=["DEBUG", "IS_DEBUG"],
            env_var="STATA_MCP__IS_DEBUG",
            default=False,
            converter=self._to_bool,
            validator=lambda x: isinstance(x, bool)
        )

    @property
    def LOGGING_ON(self) -> bool:
        return self._get_config_value(
            config_keys=["DEBUG", "logging", "LOGGING_ON"],
            env_var="STATA_MCP__LOGGING_ON",
            default=True,
            converter=self._to_bool,
            validator=lambda x: isinstance(x, bool)
        )

    @property
    def LOGGING_CONSOLE_HANDLER_ON(self) -> bool:
        return self._get_config_value(
            config_keys=["DEBUG", "logging", "LOGGING_CONSOLE_HANDLER_ON"],
            env_var="STATA_MCP__LOGGING_CONSOLE_HANDLER_ON",
            default=False,
            converter=self._to_bool,
            validator=lambda x: isinstance(x, bool)
        )

    @property
    def LOGGING_FILE_HANDLER_ON(self) -> bool:
        return self._get_config_value(
            config_keys=["DEBUG", "logging", "LOGGING_FILE_HANDLER_ON"],
            env_var="STATA_MCP__LOGGING_FILE_HANDLER_ON",
            default=True,
            converter=self._to_bool,
            validator=lambda x: isinstance(x, bool)
        )

    @property
    def LOG_FILE(self) -> Path:
        log_file = self._get_config_value(
            config_keys=["DEBUG", "logging", "LOG_FILE"],
            env_var="STATA_MCP__LOG_FILE",
            default=self.STATA_MCP_DIRECTORY / "stata_mcp_debug.log",
            converter=self._to_path,
            validator=lambda x: isinstance(x, Path)
        )

        log_file.parent.mkdir(parents=True, exist_ok=True)
        return log_file

    @property
    def MAX_BYTES(self) -> int:
        return self._get_config_value(
            config_keys=["DEBUG", "logging", "MAX_BYTES"],
            env_var="STATA_MCP__LOGGING__MAX_BYTES",
            default=10_000_000,
            converter=self._to_int,
            validator=lambda x: isinstance(x, int) and x > 0
        )

    @property
    def BACKUP_COUNT(self) -> int:
        return self._get_config_value(
            config_keys=["DEBUG", "logging", "BACKUP_COUNT"],
            env_var="STATA_MCP__LOGGING__BACKUP_COUNT",
            default=5,
            converter=self._to_int,
            validator=lambda x: isinstance(x, int) and x >= 0
        )

    @property
    def SYSTEM_OS(self) -> str:
        system_os = platform.system()
        if system_os not in ["Darwin", "Linux", "Windows"]:
            # Here, if unknown system -> exit.
            sys.exit(f"Unknown System: {system_os}")
        return system_os

    @property
    def IS_UNIX(self) -> bool:
        return self.SYSTEM_OS.lower() in ["darwin", "linux"]

    @property
    def STATA_CLI(self) -> str:
        try:
            finder = StataFinder(self.config.get("STATA", {}).get("STATA_CLI", None))
            return finder.STATA_CLI
        except FileNotFoundError as e:
            sys.exit(str(e))


if __name__ == "__main__":
    cfg = Config("./config.example.toml")
    print(cfg.IS_DEBUG)
    print(type(cfg.config))
