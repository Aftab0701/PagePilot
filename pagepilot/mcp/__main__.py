"""Entry point for running MCP server as a module.

Usage:
    python -m pagepilot.mcp
"""

import asyncio

from pagepilot.mcp.server import main

if __name__ == '__main__':
	asyncio.run(main())
