#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 - Present Sepine Tam, Inc. All Rights Reserved
#
# @Author : Sepine Tam (谭淞)
# @Email  : sepinetam@gmail.com
# @File   : adversarial_thinking_agent.py

import os
from agents import Model

from ..agent_base import AgentBase
from ..set_model import set_model


class AdversarialThinkingAgent(AgentBase):
    NAME = "Adversarial Thinking Agent"
    agent_instructions = """
    You are a deeply adversarial thinking agent. 
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
        if not model:  # if there is no model, set default model as deepseek-reasoner
            model = set_model(
                model_name=os.getenv("OPENAI_MODEL", "deepseek-reasoner"),
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")
            )

        super().__init__(
            name=name or self.NAME,
            instructions=instructions or self.agent_instructions,
            model=model,
            mcp_servers=mcp_servers,
            tools=tools,
            max_turns=max_turns,
            DISABLE_TRACING=DISABLE_TRACING,
            *args,
            **kwargs
        )

