# Stata-MCP

**Let LLM help you achieve your regression with Stata.**

## Quickly Start

> Requirements: [uv](https://docs.astral.sh/uv/getting-started/installation/) or python 3.11+  
> If you don't have `uv` but `python`, you can install it with `pip install uv`.  

First, you should check whether your device is supported by stata-mcp.  
```bash
uvx stata-mcp --usable
```
If each check is passed, you can start using stata-mcp.  
If remind not found STATA_CLI, you can see [StataFinder](core/stata/finder.md#not-found) to solve it.

The common configuration file (json)
```json
{
  "mcpServers":{
    "stata-mcp": {
      "command": "uvx",
      "args": ["stata-mcp"]
    }
  }
}
```

If you want to explore more [clients](clients.md) or [agents](agents/index.md), visit their respective documentation.

