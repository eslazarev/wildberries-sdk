import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "scripts"))
# The MCP server package, importable without installing it.
sys.path.insert(0, str(ROOT / "mcp-server" / "src"))
