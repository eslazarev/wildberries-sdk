#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="${ROOT_DIR}/generation.yaml"
CLIENTS_DIR="${ROOT_DIR}/clients/php"
COMPOSER_FILE="${ROOT_DIR}/composer.json"
README_FILE="${ROOT_DIR}/docs/php/README.md"

if [[ ! -f "${CONFIG_FILE}" ]]; then
  echo "Error: config not found: ${CONFIG_FILE}" >&2
  exit 1
fi

if [[ ! -d "${CLIENTS_DIR}" ]]; then
  echo "Error: php clients directory not found: ${CLIENTS_DIR}" >&2
  exit 1
fi

read_specs() {
  awk '
    $1=="specs:" {inside=1; next}
    inside && $0 ~ /^[^[:space:]]/ {inside=0}
    inside && $1=="-" {print $2}
  ' "${CONFIG_FILE}"
}

module_names=()
while IFS= read -r spec; do
  [[ -z "${spec}" ]] && continue
  base="$(basename "${spec%%\?*}" .yaml)"
  base="${base#*-}"
  module="${base//-/_}"
  if [[ -d "${CLIENTS_DIR}/${module}" ]]; then
    module_names+=("${module}")
  fi
done < <(read_specs)

if [[ "${#module_names[@]}" -eq 0 ]]; then
  while IFS= read -r module; do
    [[ -n "${module}" ]] && module_names+=("${module}")
  done < <(ls -1 "${CLIENTS_DIR}" 2>/dev/null | sort)
fi

if [[ "${#module_names[@]}" -eq 0 ]]; then
  echo "Error: no php client modules found in ${CLIENTS_DIR}" >&2
  exit 1
fi

PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Error: python is required to build composer.json." >&2
  exit 1
fi

PHP_MODULES="$(printf "%s\n" "${module_names[@]}")" \
PHP_ROOT_DIR="${ROOT_DIR}" \
PHP_CLIENTS_DIR="${CLIENTS_DIR}" \
PHP_COMPOSER_FILE="${COMPOSER_FILE}" \
PHP_README_FILE="${README_FILE}" \
"${PYTHON_BIN}" - <<'PY'
import json
import os
import re
from pathlib import Path

modules = [line.strip() for line in os.environ["PHP_MODULES"].splitlines() if line.strip()]
root_dir = Path(os.environ["PHP_ROOT_DIR"])
clients_dir = Path(os.environ["PHP_CLIENTS_DIR"])
composer_path = Path(os.environ["PHP_COMPOSER_FILE"])
readme_path = Path(os.environ["PHP_README_FILE"])

def to_pascal(name: str) -> str:
    parts = re.split(r"[_-]+", name)
    return "".join(part[:1].upper() + part[1:] for part in parts if part)

def find_requirements() -> dict:
    for module in modules:
        composer_file = clients_dir / module / "composer.json"
        if not composer_file.exists():
            continue
        try:
            data = json.loads(composer_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        require = data.get("require")
        if isinstance(require, dict) and require:
            return require
    return {
        "php": ">=7.4",
        "ext-curl": "*",
        "ext-json": "*",
        "guzzlehttp/guzzle": "^7.0",
    }

autoload = {}
for module in modules:
    namespace = f"Wildberries\\Sdk\\{to_pascal(module)}\\"
    autoload[namespace] = f"clients/php/{module}/lib/"

composer = {
    "name": "eslazarev/wildberries-sdk",
    "description": "Wildberries API SDK for PHP: typed clients for the Wildberries seller API, regenerated from the official OpenAPI specs on every change.",
    "license": "MIT",
    "type": "library",
    "homepage": "https://eslazarev.github.io/wildberries-sdk/",
    "keywords": [
        "wildberries",
        "wildberries-api",
        "wildberries-sdk",
        "wb",
        "wb-api",
        "seller-api",
        "marketplace",
        "ecommerce",
        "api",
        "sdk",
        "openapi",
        "api-client",
        "вайлдберриз",
        "вб",
        "php",
    ],
    "require": find_requirements(),
    "autoload": {"psr-4": autoload},
    "support": {"source": "https://github.com/eslazarev/wildberries-sdk"},
}

if readme_path.exists():
    try:
        composer["readme"] = str(readme_path.relative_to(root_dir).as_posix())
    except ValueError:
        composer["readme"] = str(readme_path.as_posix())

composer_path.write_text(json.dumps(composer, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
PY
