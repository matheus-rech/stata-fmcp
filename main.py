from stata_mcp import mcp


def main(transport: str = "stdio"):
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()

"""
If you want to start it locally you can use `uv run main.py` for start stata-mcp without `uvx`
Also, if you have ever download this repo, you can run with the flowing config:
```json
{
  "mcpServers": {
    "stata-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "<THIS_FILE_DIR>",
        "main.py"
      ],
      "env": {
        "stata_cli": "stata-mp"
      }
    }
  }
}
```
This was the original approach used to launch stata-mcp. At the time,
I did not yet know how to package the code for release on PyPI or how to structure a Python package—indeed.
(In fact I am still far from proficient in these tasks)
"""

