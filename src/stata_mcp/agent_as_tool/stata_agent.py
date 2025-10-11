#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 - Present Sepine Tam, Inc. All Rights Reserved
#
# @Author : Sepine Tam (谭淞)
# @Email  : sepinetam@gmail.com
# @File   : stata_agent.py

import os

from agents import Agent, OpenAIChatCompletionsModel, set_tracing_disabled
from agents.mcp import MCPServerStdio


class StataAgent:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", None)
    agent_instructions: str = """
    # Role
    You are a **Stata Assistant**, you have the ability to use Stata.

    ## 工作原则
    ### 三思而后行

    """
    _default_tool_description: str = """
    能够使用Stata的Agent，能够根据给定的需求帮助写Stata代码并运行和debug
    """

    stata_cli = os.getenv("stata_cli", None)
    _mcp_env: dict = None
    if stata_cli:
        _mcp_env["stata_cli"] = stata_cli
    stata_mcp = MCPServerStdio(
        name="Stata-MCP",
        params={
            "command": "uvx",
            "args": ["stata-mcp"],
            "env": _mcp_env
        },
    )

    def __init__(self,
                 name: str = None,
                 instructions: str = None,
                 model: OpenAIChatCompletionsModel = None,
                 mcp_servers: list = None,
                 tools: list = None,
                 tool_description: str = None,
                 max_turns: int = 30,  # If the task is not easy, set larger number
                 DISABLE_TRACING: bool = False,
                 *args,
                 **kwargs):
        # Disable tracing while not found openai_api_key and set tracing disable.
        set_tracing_disabled(
            (not kwargs.get("OPENAI_API_KEY", self.OPENAI_API_KEY)) or DISABLE_TRACING
        )

        if not mcp_servers:
            mcp_servers = []
        mcp_servers.append(self.stata_mcp)

        self.agent = Agent(
            name=name or "Stata Agent",
            instructions=instructions or self.agent_instructions,
            mcp_servers=mcp_servers,
        )
        if model:
            self.agent.model = model
        if tools:
            self.agent.tools = tools

        self.tool_description = tool_description or self._default_tool_description
        self.max_turns = max_turns

    @property
    def as_tool(self):
        return self.agent.as_tool(
            tool_name="Stata Agent",
            tool_description="",
            max_turns=self.max_turns
        )
