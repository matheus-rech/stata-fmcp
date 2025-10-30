#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 - Present Sepine Tam, Inc. All Rights Reserved
#
# @Author : Sepine Tam (谭淞)
# @Email  : sepinetam@gmail.com
# @File   : base.py

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union


@dataclass
class StataEditionConfig:
    """
    StataEditionConfig class for comparing Stata versions with sorting support.

    Attributes:
        edition (str): Edition type (mp > se > be > ic > default)
        version (Union[int, float]): Version number (e.g., 18, 19.5)
        path (str): Full path to Stata executable

    Comparison Rules:
        1. First compare edition priority: mp > se > be > ic > default
        2. Then compare numeric version: higher > lower
        3. Support float versions like 19.5 > 19

    Example:
        >>> p1 = StataEditionConfig("mp", 18, "/usr/local/bin/stata-mp")
        >>> p2 = StataEditionConfig("se", 19, "/usr/local/bin/stata-se")
        >>> p1 > p2  # True (mp has priority over se even with smaller version)
    """

    edition: str
    version: Union[int, float]
    path: str

    # Edition priority mapping
    _EDITION_PRIORITY = {
        "mp": 5,
        "se": 4,
        "be": 3,
        "ic": 2,
        "default": 1,
        "unknown": 0,
    }

    def __post_init__(self):
        """Validation and processing after initialization."""
        # Normalize edition type to lowercase
        self.edition = self.edition.lower()

        # If edition type is not in priority mapping, mark as unknown
        if self.edition not in self._EDITION_PRIORITY:
            self.edition = "unknown"

    @property
    def edition_priority(self) -> int:
        """Get the priority value of the edition type."""
        return self._EDITION_PRIORITY[self.edition]

    def __lt__(self, other) -> bool:
        """Less than comparison for sorting."""
        if not isinstance(other, StataEditionConfig):
            return NotImplemented

        # First compare edition priority
        if self.edition_priority != other.edition_priority:
            return self.edition_priority < other.edition_priority

        # Same edition, compare version number
        return self.version < other.version

    def __le__(self, other) -> bool:
        """Less than or equal comparison."""
        return self < other or self == other

    def __gt__(self, other) -> bool:
        """Greater than comparison."""
        if not isinstance(other, StataEditionConfig):
            return NotImplemented

        # First compare edition priority
        if self.edition_priority != other.edition_priority:
            return self.edition_priority > other.edition_priority

        # Same edition, compare version number
        return self.version > other.version

    def __ge__(self, other) -> bool:
        """Greater than or equal comparison."""
        return self > other or self == other

    def __eq__(self, other) -> bool:
        """Equality comparison."""
        if not isinstance(other, StataEditionConfig):
            return NotImplemented

        return (self.edition_priority == other.edition_priority and
                self.version == other.version)

    def __str__(self) -> str:
        """String representation - returns the path."""
        return self.path

    def __repr__(self) -> str:
        """Detailed string representation - returns the path."""
        return self.path

    def __int__(self) -> int:
        """Integer conversion - returns the version number."""
        return int(self.version)

    def __float__(self) -> float:
        """Float conversion - returns the version number."""
        return float(self.version)

    @property
    def stata_cli_path(self) -> str:
        """Get the Stata CLI path."""
        return self.path


class FinderBase(ABC):
    stata_cli: str = None

    def __init__(self, stata_cli: str = None):
        if stata_cli:
            self.stata_cli = stata_cli
        self.load_default_cli_path()

    def find_stata(self) -> str | None:
        if self.stata_cli:
            return self.stata_cli
        return self.finder()

    @abstractmethod
    def finder(self) -> str: ...

    @abstractmethod
    def find_path_base(self) -> Dict[str, List[str]]: ...

    @staticmethod
    def priority() -> Dict[str, List[str]]:
        name_priority = {
            "mp": ["stata-mp"],
            "se": ["stata-se"],
            "be": ["stata-be"],
            "default": ["stata"],
        }
        return name_priority

    @staticmethod
    def _is_executable(p: Path) -> bool:
        try:
            return p.is_file() and os.access(p, os.X_OK)
        except OSError:
            return False

    def load_cli_from_env(self) -> Optional[str]:
        self.stata_cli = os.getenv("stata_cli") or os.getenv("STATA_CLI")
        return self.stata_cli

    def load_default_cli_path(self) -> str | None:
        if self.stata_cli is not None:
            # try to load from env
            self.load_cli_from_env()
        return self.stata_cli

    def find_from_bin(self,
                      *,
                      priority: Optional[Iterable[str]] = None) -> str | None:
        pr = list(priority) if priority else ["mp", "se", "be", "default"]
        name_priority = self.priority()
        bins = self.find_path_base().get("bin")

        ordered_names: List[str] = []
        for key in pr:
            ordered_names.extend(name_priority.get(key, []))

        for b in bins:
            base = Path(b)
            for name in ordered_names:
                p = base / name
                if self._is_executable(p):
                    return str(p)
        return None
