#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 - Present Sepine Tam, Inc. All Rights Reserved
#
# @Author : Sepine Tam
# @Email  : sepinetam@gmail.com
# @File   : installer.py

import json
import os
import sys
from pathlib import Path

from ...core.stata import StataFinder


class Installer:
    def __init__(self, sys_os: str = None, is_env: bool = True):
        self.sys_os = sys_os or sys.platform
        self.is_env = is_env

    @property
    def STATA_CLI(self) -> str:
        return StataFinder().STATA_CLI

    @property
    def STATA_MCP_COMMON_CONFIG(self):
        command = "uvx"
        args = ["stata-mcp"]
        env = {"STATA_CLI": self.STATA_CLI} if self.is_env else {}
        return {
            "stata-mcp": {
                "command": command,
                "args": args,
                "env": env
            }
        }

    def install(self, to: str):
        client_function_mapping = {
            "claude": self.install_to_claude_desktop,
            "cc": self.install_to_claude_code,
        }
        if to in client_function_mapping.keys():
            client_function_mapping[to]()
        else:
            print(f"{to} is not a valid client.")
            print(f"Please choose a valid client from {client_function_mapping.keys()}")
            sys.exit(1)

    def install_to_json_config(self, config_path: Path, key: str = "mcpServers"):
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)

        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except json.JSONDecodeError:
                overwrite = input(
                    f"We could not open your config file {config_path.as_posix()}, "
                    "whether continue (This might overwrite your config file)\n[Y]es/[N]o"
                ).lower()
                if overwrite in ["y", "yes"]:
                    config = {key: {}}
                else:
                    sys.exit(1)
        else:
            config = {key: {}}

        servers = config.setdefault(key, {})
        if "stata-mcp" in servers:
            print("stata-mcp is already installed.")
            sys.exit(0)

        servers.update(self.STATA_MCP_COMMON_CONFIG)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def install_to_claude_code(self):
        cc_mcp_config_file = Path.home() / ".claude.json"
        self.install_to_json_config(cc_mcp_config_file)

    def install_to_claude_desktop(self):
        # Get config file path based on OS
        if self.sys_os.lower() == "darwin":
            config_file_path = os.path.expanduser(
                "~/Library/Application Support/Claude/claude_desktop_config.json"
            )
        elif self.sys_os.lower() == "linux":
            print("There is not a Linux version of Claude yet.")
            sys.exit(1)
        elif self.sys_os.lower() == "windows":
            appdata = os.getenv("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
            config_file_path = os.path.join(appdata, "Claude", "claude_desktop_config.json")
        else:
            print(f"Unsupported platform: {self.sys_os}")
            sys.exit(1)

        self.install_to_json_config(Path(config_file_path))

