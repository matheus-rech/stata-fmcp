import os
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import tomllib


def set_config(key, value):
    with open(".env", "w+", encoding="utf-8") as f:
        f.write(f"{key}={value}")
    return {key: value}
