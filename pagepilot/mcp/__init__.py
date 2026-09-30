"""MCP (Model Context Protocol) support for pagepilot.

This module provides integration with MCP servers and clients for browser automation.
"""

from pagepilot.mcp.client import MCPClient
from pagepilot.mcp.controller import MCPToolWrapper

__all__ = ['MCPClient', 'MCPToolWrapper', 'PagePilotServer']  # type: ignore


def __getattr__(name):
	"""Lazy import to avoid importing server module when only client is needed."""
	if name == 'PagePilotServer':
		from pagepilot.mcp.server import PagePilotServer

		return PagePilotServer
	raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
