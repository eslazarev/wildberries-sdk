#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="${ROOT_DIR}/generation.yaml"
SPECS_DIR="${ROOT_DIR}/specs"

if [[ ! -f "${CONFIG_FILE}" ]]; then
  echo "Error: config not found: ${CONFIG_FILE}" >&2
  exit 1
fi

mkdir -p "${SPECS_DIR}"

read_specs() {
  awk '
    $1=="specs:" {inside=1; next}
    inside && $0 ~ /^[^[:space:]]/ {inside=0}
    inside && $1=="-" {print $2}
  ' "${CONFIG_FILE}"
}

download_spec() {
  local url="$1"
  local dest="$2"

  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "${url}" -o "${dest}"
    return
  fi

  if command -v wget >/dev/null 2>&1; then
    wget -qO "${dest}" "${url}"
    return
  fi

  echo "Error: need curl or wget to download specs." >&2
  exit 1
}

specs=()
while IFS= read -r spec; do
  [[ -n "${spec}" ]] && specs+=("${spec}")
done < <(read_specs)

if [[ "${#specs[@]}" -eq 0 ]]; then
  echo "Error: no specs found in ${CONFIG_FILE}" >&2
  exit 1
fi

for spec in "${specs[@]}"; do
  if [[ "${spec}" =~ ^https?:// ]]; then
    dest="${SPECS_DIR}/$(basename "${spec}")"
    echo "Downloading $(basename "${spec}")"
    download_spec "${spec}" "${dest}"
  else
    echo "Skipping non-URL spec: ${spec}"
  fi
done
