"""MCP server for the Wildberries seller API, built on wildberries-sdk."""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("wildberries-mcp")
except PackageNotFoundError:  # running from a source checkout
    __version__ = "0.0.0"
