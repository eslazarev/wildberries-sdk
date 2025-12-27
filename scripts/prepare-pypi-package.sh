#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="${ROOT_DIR}/src"

rm -rf "${SRC_DIR}"
mkdir -p "${SRC_DIR}/wildberries_sdk"

shopt -s nullglob
for spec_dir in "${ROOT_DIR}"/clients/python/*; do
  spec_name="$(basename "${spec_dir}")"
  echo "Copying ${spec_name}"
  mkdir -p "${SRC_DIR}/wildberries_sdk/${spec_name}"
  cp -a "${spec_dir}/." "${SRC_DIR}/wildberries_sdk/${spec_name}/"
done

cat > "${SRC_DIR}/wildberries_sdk/__init__.py" <<'PY'
"""Wildberries SDK aggregated package."""
PY

WRAPPER_ROOT="${SRC_DIR}/wildberries_sdk"
mkdir -p "${WRAPPER_ROOT}"
cat > "${WRAPPER_ROOT}/__init__.py" <<'PY'
"""Wildberries SDK aggregated package."""
PY

for pkg_dir in "${SRC_DIR}"/wildberries_sdk_*; do
  pkg_base="$(basename "${pkg_dir}")"
  sub_name="${pkg_base#wildberries_sdk_}"
  sub_dir="${WRAPPER_ROOT}/${sub_name}"
  mkdir -p "${sub_dir}"
  cat > "${sub_dir}/__init__.py" <<PY
from ${pkg_base} import ApiClient, Configuration
from ${pkg_base} import api as _api

# Re-export API classes from the generated package.
for _name in dir(_api):
    if _name.endswith("Api") or _name == "Api":
        globals()[_name] = getattr(_api, _name)

__all__ = ["ApiClient", "Configuration"] + [
    _name for _name in dir(_api) if _name.endswith("Api") or _name == "Api"
]
PY
done
