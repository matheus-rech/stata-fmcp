import os
import platform
import tomllib


class Config:
    """Simple configuration manager for Stata-MCP."""

    CONFIG_FILE_PATH = os.path.expanduser("~/.stata-mcp/config.toml")

    def __init__(self) -> None:
        os.makedirs(os.path.dirname(self.CONFIG_FILE_PATH), exist_ok=True)
        if not os.path.exists(self.CONFIG_FILE_PATH):
            self.config: dict = self._default_config()
            self._save()
        else:
            self.config = self.load_config()

    def _default_config(self) -> dict:
        sys_os = platform.system()
        if sys_os in ["Darwin", "Linux"]:
            documents_path = os.path.expanduser("~/Documents")
        elif sys_os == "Windows":
            documents_path = os.path.join(os.environ.get("USERPROFILE", "~"), "Documents")
        else:
            documents_path = os.path.expanduser("~/Documents")
        return {
            "stata_cli": "",
            "output_base_path": os.path.join(documents_path, "stata-mcp-folder"),
        }

    def _save(self) -> None:
        """Write the current config to the TOML file."""
        with open(self.CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
            for key, value in self.config.items():
                escaped = str(value).replace('"', '\\"')
                f.write(f"{key} = \"{escaped}\"\n")

    def load_config(self) -> dict:
        with open(self.CONFIG_FILE_PATH, "rb") as f:
            return tomllib.load(f)

    def get(self, key: str, default: str | None = None):
        return self.config.get(key, default)

    def set(self, key: str, value: str) -> None:
        self.config[key] = value
        self._save()

    def delete(self, key: str) -> None:
        if key in self.config:
            del self.config[key]
            self._save()
