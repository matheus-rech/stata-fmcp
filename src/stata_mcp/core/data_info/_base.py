#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 - Present Sepine Tam, Inc. All Rights Reserved
#
# @Author : Sepine Tam (谭淞)
# @Email  : sepinetam@gmail.com
# @File   : _base.py

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd


class DataInfoBase(ABC):
    def __init__(self,
                 data_path: str | Path,
                 vars_list: List[str] | str = None,
                 *,
                 encoding: str = "utf-8",):
        self.data_path = data_path
        self.encoding = encoding
        self._pre_vars_list = vars_list

    # Properties
    @property
    def df(self) -> pd.DataFrame:
        """Get the data as a pandas DataFrame."""
        return self._read_data()

    @property
    def vars_list(self) -> List[str]:
        """Get the list of selected variables."""
        return self._get_selected_vars(self._pre_vars_list)

    @property
    def info(self) -> Dict[str, Any]:
        """Get comprehensive information about the data."""
        return {
            "summary": self.summary(),
            "describe": self.describe(),
        }

    # Abstract methods (must be implemented by subclasses)
    @abstractmethod
    def _read_data(self) -> pd.DataFrame:
        """Read data from the source file. Must be implemented by subclasses."""
        ...

    # Public methods
    def summary(self) -> Dict[str, Any]:
        """
        Provide a summary of the data.

        Returns:
            Dict[str, Any]: the summary of provided data (vars)

        Examples:
            >>> from stata_mcp.core.data_info import DtaDataInfo
            >>> data_info = DtaDataInfo(...)
            >>> summary_data = data_info.summary()
            >>> print(summary_data)
            {
                "overview": {
                    "obs": 1314,  # Observed numbers
                    "var_numbers": 10  # equal to the length of `vars_detail`.
                },
                "vars_detail": {
                    "name": {
                        "type": "str",
                        "obs": 1314,
                        "value_list": ["Jack", "Rose", ...]  # list 10 random unique value
                    },
                    "age": {
                        "type": "float",  # it signed as float no matter the value type is int or float
                        "obs": 1314,
                        "summary": {
                            "mean": 52.1,
                            "se": 10.3386,
                            "min": 18,
                            "max": 100
                        }
                    },
                    "male": {
                        "type": "float",  # Note: no bool type! It is signed with 0 and 1.
                        "obs": 1111,  # Note: maybe some obs do not have value (NA), this is not be counted.
                        "summary": {
                            "mean": 0.49955,
                            "se": 0.500225,
                            "min": 0,
                            "max": 1
                        }
                    }
                    "var_name": {}
                }
            }
        """
        ...

    def describe(self) -> str:
        """Provide a text description of the data."""
        ...

    # Private helper methods
    def _get_selected_vars(self, vars: List[str] | str = None) -> List[str]:
        """
        Get the list of selected variables.

        If vars is None, return all variables from self.data.
        If vars is a string, convert it to a list.
        Check if all variables exist in self.data, if not raise an error and return all available variables.

        Args:
            vars: List of variable names, single variable name, or None.

        Returns:
            List[str]: List of selected variable names.

        Raises:
            ValueError: If specified variables don't exist in the dataset.
        """
        # Get all available variables from the data
        all_vars = list(self.df.columns)

        if vars is None:
            return all_vars

        # Convert string to list if needed
        if isinstance(vars, str):
            vars = [vars]

        # Check if all specified variables exist in the dataset
        missing_vars = [var for var in vars if var not in all_vars]

        if missing_vars:
            raise ValueError(f"Variables {missing_vars} not found in dataset. "
                             f"Available variables are: {all_vars}")

        return vars
