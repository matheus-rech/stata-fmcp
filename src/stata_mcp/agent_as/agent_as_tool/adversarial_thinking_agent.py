#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 - Present Sepine Tam, Inc. All Rights Reserved
#
# @Author : Sepine Tam (谭淞)
# @Email  : sepinetam@gmail.com
# @File   : adversarial_thinking_agent.py

import os
from abc import ABC, abstractmethod
from agents import Model, Runner
from agents.tool import function_tool

from ..agent_base import AgentBase
from ..set_model import set_model


class AdviceBase(AgentBase, ABC):
    NAME = "Advice Agent"
    agent_instructions = None

    def __init__(self, model: Model, *args, **kwargs):
        super().__init__(
            model=model,
            instructions=self._system_instructions(),
            *args,
            **kwargs
        )

    @abstractmethod
    def _system_instructions(self) -> str: ...

    def get_run_result(self, task: str) -> str:
        """
        Execute evaluation task using OpenAI Agents SDK Runner

        Args:
            task: The task or viewpoint to evaluate

        Returns:
            str: The evaluation result from AI model
        """
        # Use Runner.run to execute the agent
        result = Runner.run_sync(
            self.agent,
            context=task,
            max_turns=self.max_turns
        )

        return result.final_output


class PositiveAdvice(AdviceBase):
    def _system_instructions(self) -> str:
        instructions = """
        """
        return instructions


class NegativeAdvice(AdviceBase):
    def _system_instructions(self) -> str:
        instructions = """
        """
        return instructions

@function_tool()
def advice_positive() -> str: ...


class AdversarialThinkingAgent(AgentBase):
    NAME = "Adversarial Thinking Agent"
    agent_instructions = """
    You are a deeply adversarial thinking agent. 
    """

    _default_tool_description: str = """
    
    """

    def __init__(self,
                 name: str = None,
                 instructions: str = None,
                 model: Model = None,
                 mcp_servers: list = None,
                 tools: list = None,
                 tool_description: str = None,
                 max_turns: int = 30,  # If the task is not easy, set larger number
                 DISABLE_TRACING: bool = False,
                 *args,
                 **kwargs):
        if not model:  # if there is no model, set default model as deepseek-reasoner
            model = set_model(
                model_name=os.getenv("OPENAI_MODEL", "deepseek-reasoner"),
                api_key=os.getenv("OPENAI_API_KEY") or os.getenv("DEEPSEEK_API_KEY"),
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

        self.tool_description = tool_description or self._default_tool_description

    @property
    def as_tool(self):
        return self.agent.as_tool(
            tool_name="Adversarial Thinking Agent",
            tool_description=self.tool_description,
            max_turns=self.max_turns
        )

