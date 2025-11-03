#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 - Present Sepine Tam, Inc. All Rights Reserved
#
# @Author : Sepine Tam (谭淞)
# @Email  : sepinetam@gmail.com
# @File   : _base.py

from agents import Model, handoff
from agents.handoffs import Handoff

from ..agent_base import AgentBase


class KnowledgeBase(AgentBase):
    NAME = "Knowledge Agent"
    agent_instructions: str = """
    You are a professional researcher on the area of ACADEMIC RESEARCH
    """

    def __init__(self,
                 name: str = None,
                 instructions: str = None,
                 model: Model = None,
                 mcp_servers: list = None,
                 tools: list = None,
                 max_turns: int = 30,  # If the task is not easy, set larger number
                 DISABLE_TRACING: bool = False,
                 *args,
                 **kwargs):
        super().__init__(
            name=name or self.NAME,
            instructions=instructions,
            model=model,
            mcp_servers=mcp_servers,
            tools=tools,
            max_turns=max_turns,
            DISABLE_TRACING=DISABLE_TRACING,
            *args,
            **kwargs
        )

    @property
    def TO_HANDOFF_AGENT(self) -> Handoff:
        return handoff(
            agent=self.agent,
        )
