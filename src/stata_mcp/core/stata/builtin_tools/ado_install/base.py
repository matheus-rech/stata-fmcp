#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 - Present Sepine Tam, Inc. All Rights Reserved
#
# @Author : Sepine Tam (谭淞)
# @Email  : sepinetam@gmail.com
# @File   : base.py

from abc import ABC, abstractmethod

from ...stata_controller import StataController


class AdoInstallBase(ABC):
    def __init__(self,
                 stata_cli,
                 is_replace: bool = True):
        self.stata_cli = stata_cli
        self.is_replace = is_replace
        self.__post_initialization()

    def __post_initialization(self):
        """
        Post-initialization hook for subclasses to override.

        This method is called automatically after __init__ completes.
        Subclasses can override this method to perform additional initialization
        without having to override the entire __init__ method.

        Examples:
            >>> class MyInstaller(AdoInstallBase):
            ...     def __post_initialization(self):
            ...         self.github_mirror = "https://github.com"  # Fake var
            ...
            ...     def install(self, package: str):
            ...         return f"Installing {package} with {self.custom_setting}"
        """
        pass

    @property
    def controller(self) -> StataController:
        return StataController(self.stata_cli)

    @property
    def REPLACE_MESSAGE(self) -> str:
        if self.is_replace:
            return ", replace"
        else:
            return ""

    @abstractmethod
    def install(self, package: str) -> str: pass

    @staticmethod
    @abstractmethod
    def check_install(message: str) -> bool:
        ...
