#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 - Present Sepine Tam, Inc. All Rights Reserved
#
# @Author : Sepine Tam (谭淞)
# @Email  : sepinetam@gmail.com
# @File   : _cli.py

import argparse
import sys
from importlib.metadata import version


def main() -> None:
    """Entry point for the command line interface."""
    parser = argparse.ArgumentParser(
        prog="stata-mcp",
        description="Stata-MCP command line interface",
        add_help=True)

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {version('stata-mcp')}",
        help="show version information",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # MCP server options (default behavior)
    parser.add_argument(
        "-t",
        "--transport",
        choices=["stdio", "sse", "http"],
        default="stdio",
        help="MCP server transport method (default: stdio)",
    )
    parser.add_argument(
        "-u",
        "--usable",
        action="store_true",
        help="Check whether Stata-MCP can be used on this computer",
    )

    # Agent subcommand
    agent_parser = subparsers.add_parser(
        "agent",
        help="Run Stata-MCP as agent mode"
    )
    agent_subparsers = agent_parser.add_subparsers(dest="agent_action")

    agent_run_parser = agent_subparsers.add_parser("run", help="Start agent")
    agent_run_parser.add_argument(
        "--work-dir",
        default="./",
        help="Working directory for agent (default: current directory)",
    )

    # Install subcommand
    install_parser = subparsers.add_parser(
        "install",
        help="Install Stata-MCP to Claude Desktop"
    )
    install_parser.add_argument(
        "-c",
        "--client",
        choices=["claude", "cc", "cursor", "cline", "codex"],
        default="claude",
        help="Target client (default: claude)",
    )

    args = parser.parse_args()

    # Handle --usable flag
    if args.usable:
        from ..utils.usable import usable
        sys.exit(usable())

    # Handle subcommands
    if args.command == "agent":
        if args.agent_action == "run":
            from ..agent_as import REPLAgent
            agent = REPLAgent(work_dir=args.work_dir)
            agent.run()
        else:
            agent_parser.print_help()

    elif args.command == "install":
        from ..utils.Installer import Installer
        Installer(sys_os=sys.platform).install(args.client)
        print(f"Stata-MCP has been installed to {args.client}.")
        sys.exit(0)

    # Default: Start MCP server
    else:
        from ..mcp_servers import stata_mcp as mcp

        transport = args.transport
        if transport == "http":
            transport = "streamable-http"
        mcp.run(transport=transport)
