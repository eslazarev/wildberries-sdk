#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYPROJECT="${ROOT_DIR}/pyproject.toml"

if [[ ! -f "${PYPROJECT}" ]]; then
  echo "Error: pyproject.toml not found." >&2
  exit 1
fi

current="$(awk -F\" '/^version =/ {print $2; exit}' "${PYPROJECT}")"
if [[ -z "${current}" ]]; then
  echo "Error: version not found in pyproject.toml." >&2
  exit 1
fi

IFS='.' read -r major minor patch <<< "${current}"
if [[ -z "${major}" || -z "${minor}" || -z "${patch}" ]]; then
  echo "Error: invalid version format: ${current}" >&2
  exit 1
fi

patch=$((patch + 1))
next="${major}.${minor}.${patch}"

awk -v new_version="${next}" '
  BEGIN {updated=0}
  /^version =/ {
    print "version = \"" new_version "\""
    updated=1
    next
  }
  {print}
  END {if (!updated) exit 1}
' "${PYPROJECT}" > "${PYPROJECT}.tmp"

mv "${PYPROJECT}.tmp" "${PYPROJECT}"

# The MCP server ships in lockstep: same version, pinned to this exact SDK,
# because it reads its operations from the SDK release it depends on.
MCP_PYPROJECT="${ROOT_DIR}/mcp-server/pyproject.toml"
if [[ -f "${MCP_PYPROJECT}" ]]; then
  sed -e "s/^version = \".*\"/version = \"${next}\"/" \
      -e "s/\"wildberries-sdk==[^\"]*\"/\"wildberries-sdk==${next}\"/" \
      "${MCP_PYPROJECT}" > "${MCP_PYPROJECT}.tmp"
  mv "${MCP_PYPROJECT}.tmp" "${MCP_PYPROJECT}"
fi

echo "Bumped version: ${current} -> ${next}" >&2
echo "${next}"
