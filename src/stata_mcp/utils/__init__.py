import os
import tomllib
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError


def set_config(key, value):
    with open(".env", "w+", encoding="utf-8") as f:
        f.write(f"{key}={value}")
    return {key: value}


def get_local_version() -> str:
    """
    Retrieve the current version of the 'stata-mcp' package.

    1. Traverse up from this file to find a 'pyproject.toml' file.
       If found, load its 'project.version' field.
    2. If that fails, fall back to the installed package metadata.
    3. Return 'unknown' if neither method succeeds.
    """
    # 1) Try to read version from pyproject.toml
    for directory in Path(__file__).resolve().parents:
        pyproject_file = directory / "pyproject.toml"
        if pyproject_file.is_file():
            try:
                with pyproject_file.open("rb") as f:
                    data = tomllib.load(f)
                    return data["project"]["version"]
            except (tomllib.TOMLDecodeError, KeyError):
                # invalid TOML or missing field: break to fallback
                break

    # 2) Fallback: read version from installed package metadata
    try:
        return version("stata-mcp")
    except PackageNotFoundError:
        # package not installed
        return "unknown"
