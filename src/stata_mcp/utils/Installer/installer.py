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
    def __init__(self, sys_os, is_env=True):
        self.config_file_path: str = None
        self.is_env = is_env
        if sys_os == "Darwin":
            self.config_file_path = os.path.expanduser(
                "~/Library/Application Support/Claude/claude_desktop_config.json"
            )
        elif sys_os == "Linux":
            print(
                "There is not a Linux version of Claude yet, please use the Windows or macOS version."
            )
        elif sys_os == "Windows":
            appdata = os.getenv(
                "APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
            self.config_file_path = os.path.join(
                appdata, "Claude", "claude_desktop_config.json"
            )

        os.makedirs(os.path.dirname(self.config_file_path), exist_ok=True)

        # Create an empty file if it does not already exist
        if not os.path.exists(self.config_file_path):
            with open(self.config_file_path, "w", encoding="utf-8") as f:
                # Or write the default configuration
                f.write('{"mcpServers": {}}')

    @property
    def STATA_CLI(self) -> str:
        cli = None
        if self.is_env:
            cli = os.getenv("STATA_CLI", None)
        if cli is None:
            cli = StataFinder().STATA_CLI
        return cli

    @property
    def STATA_MCP_COMMON_CONFIG(self):
        return {
            "stata-mcp": {
                "command": "uvx",
                "args": ["stata-mcp"],
                "env": {
                    "STATA_CLI": self.STATA_CLI
                },
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
        server_cfg = self.STATA_MCP_COMMON_CONFIG["stata-mcp"]
        stata_cli_path = server_cfg["env"]["STATA_CLI"]
        print("About to install the following MCP server into your Claude config:\n")
        print("  Server name:    stata-mcp")
        print(f"  Command:        {server_cfg['command']}")
        print(f"  Args:           {server_cfg['args']}")
        print(f"  STATA_CLI path: {stata_cli_path}\n")
        print(f"Configuration file to modify:\n  {self.config_file_path}\n")

        # Ask the user for confirmation
        choice = input(
            "Do you want to proceed and add this configuration? [y/N]: ")
        if choice.strip().lower() != "y":
            print("Installation aborted.")
            return

        # Read the now config
        try:
            with open(self.config_file_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {"mcpServers": {}}

        # Update MCP_Config
        servers = config.setdefault("mcpServers", {})
        servers.update(self.STATA_MCP_COMMON_CONFIG)

        # Write it
        with open(self.config_file_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        print(
            f"✅ Successfully wrote 'stata-mcp' configuration to: {self.config_file_path}"
        )
