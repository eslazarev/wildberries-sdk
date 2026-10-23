#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="${ROOT_DIR}/generation.yaml"
CLIENTS_DIR="${ROOT_DIR}/clients/rust"
README_FILE="${ROOT_DIR}/docs/rust/README.md"

START_MARKER="<!-- RUST_METHODS_LIST_START -->"
END_MARKER="<!-- RUST_METHODS_LIST_END -->"

if [[ ! -f "${CONFIG_FILE}" ]]; then
  echo "Error: config not found: ${CONFIG_FILE}" >&2
  exit 1
fi

if [[ ! -d "${CLIENTS_DIR}" ]]; then
  echo "Error: rust clients directory not found: ${CLIENTS_DIR}" >&2
  exit 1
fi

if [[ ! -f "${README_FILE}" ]]; then
  echo "Error: README not found: ${README_FILE}" >&2
  exit 1
fi

PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Error: python is required to parse client files." >&2
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
  echo "Error: no rust client modules found in ${CLIENTS_DIR}" >&2
  exit 1
fi

render_module_section() {
  local module="$1"
  local api_dir="${CLIENTS_DIR}/${module}/src/apis"

  if [[ ! -d "${api_dir}" ]]; then
    return
  fi

  local api_files=()
  while IFS= read -r file; do
    case "$(basename "${file}")" in
      mod.rs) continue ;;
    esac
    api_files+=("${file}")
  done < <(ls -1 "${api_dir}"/*.rs 2>/dev/null | sort)

  if [[ "${#api_files[@]}" -eq 0 ]]; then
    return
  fi

  "${PYTHON_BIN}" - <<'PY' "${ROOT_DIR}" "${module}" "${api_files[@]}"
import re
import sys
from pathlib import Path

root = sys.argv[1]
module = sys.argv[2]
files = sys.argv[3:]

# The Rust client keeps the whole WB description in one doc comment; shared with
# the docs site so both trim it the same way.
sys.path.insert(0, str(Path(root) / "scripts"))
from docsgen.summary import clean_summary

FUNC_RE = re.compile(r"^pub\s+(?:async\s+)?fn\s+([A-Za-z0-9_]+)\s*\(")
DOC_RE = re.compile(r"^\s*///\s?(.*)")
METHOD_RE = re.compile(r"\bMethod::([A-Z]+)\b")
FORMAT_RE = re.compile(r'format!\(\s*"([^"]+)"')


def extract_block(lines, start_idx):
    block = []
    brace_count = 0
    in_block = False
    for i in range(start_idx, len(lines)):
        line = lines[i]
        if "{" in line:
            brace_count += line.count("{")
            in_block = True
        if in_block:
            block.append(line)
        if "}" in line and in_block:
            brace_count -= line.count("}")
            if brace_count == 0:
                break
    return block


def extract_summary(lines, idx):
    doc_lines = []
    i = idx - 1
    while i >= 0:
        line = lines[i].rstrip("\n")
        stripped = line.strip()
        if stripped == "":
            i -= 1
            continue
        match = DOC_RE.match(line)
        if match:
            doc_lines.append(match.group(1).strip())
            i -= 1
            continue
        break
    if not doc_lines:
        return ""
    doc_lines.reverse()
    for line in doc_lines:
        if line:
            return line
    return ""


def normalize_path(fmt):
    if fmt.startswith("{}/"):
        fmt = fmt[3:]
    elif fmt.startswith("{}"):
        fmt = fmt[2:]
        if fmt.startswith("/"):
            fmt = fmt[1:]
    fmt = fmt.lstrip("/")
    if not fmt:
        return "/"
    return "/" + fmt


def parse_method_path(block):
    method = None
    path = None
    for line in block:
        if method is None:
            match = METHOD_RE.search(line)
            if match:
                method = match.group(1)
        if path is None:
            match = FORMAT_RE.search(line)
            if match:
                path = normalize_path(match.group(1))
        if method and path:
            break
    return method, path


methods = []
for api_file in files:
    api_name = Path(api_file).stem
    with open(api_file, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    for idx, line in enumerate(lines):
        match = FUNC_RE.match(line)
        if not match:
            continue
        name = match.group(1)
        block = extract_block(lines, idx)
        method, path = parse_method_path(block)
        summary = clean_summary(extract_summary(lines, idx))
        if not method or not path:
            continue
        methods.append((api_name, name, method, path, summary))

print(f"### {module} (`{module}`)")
for api_name, name, method, path, summary in methods:
    line = f"- `{module}::{api_name}::{name}` — `{method} {path}`"
    if summary:
        line += f" — {summary}"
    print(line)
PY
}

methods_list="## Методы API"
for module in "${module_names[@]}"; do
  section="$(render_module_section "${module}")"
  if [[ -n "${section}" ]]; then
    methods_list+=$'\n\n'
    methods_list+="${section}"
  fi
done

ensure_markers() {
  if ! grep -Fq "${START_MARKER}" "${README_FILE}" || ! grep -Fq "${END_MARKER}" "${README_FILE}"; then
    printf "\n%s\n%s\n" "${START_MARKER}" "${END_MARKER}" >> "${README_FILE}"
  fi
}

update_readme() {
  local tmp_file methods_file
  methods_file="$(mktemp)"
  printf "%s\n" "${methods_list}" > "${methods_file}"

  tmp_file="$(mktemp)"
  awk -v start="${START_MARKER}" -v end="${END_MARKER}" -v block_file="${methods_file}" '
    function print_block() {
      while ((getline line < block_file) > 0) { print line }
      close(block_file)
    }
    $0 == start { print start; print_block(); skipping=1; next }
    skipping && $0 == end { print end; skipping=0; next }
    !skipping { print }
  ' "${README_FILE}" > "${tmp_file}"
  mv "${tmp_file}" "${README_FILE}"
  rm -f "${methods_file}"
}

ensure_markers
update_readme
