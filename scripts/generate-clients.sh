#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="${ROOT_DIR}/generation.yaml"
PACKAGE_VERSION="${PACKAGE_VERSION:-0.1.0}"
SKIP_VALIDATE_SPEC="${SKIP_VALIDATE_SPEC:-1}"
USE_DOCKER="${OPENAPI_GENERATOR_DOCKER:-0}"
DOCKER_IMAGE="${OPENAPI_GENERATOR_DOCKER_IMAGE:-openapitools/openapi-generator-cli}"
GLOBAL_PROPERTIES="${OPENAPI_GENERATOR_GLOBAL_PROPERTIES:-apiDocs=false,modelDocs=false,apiTests=false,modelTests=false}"
GO_MODULE_BASE="${GO_MODULE_BASE:-}"
GO_MODULE_BASE_WARNED=0
TMP_SPECS=()

cleanup_tmp_specs() {
  local tmp
  for tmp in "${TMP_SPECS[@]:-}"; do
    if [[ -n "${tmp}" && -f "${tmp}" ]]; then
      rm -f "${tmp}"
    fi
  done
  if [[ -d "${ROOT_DIR}/.tmp-python-specs" ]]; then
    rmdir "${ROOT_DIR}/.tmp-python-specs" 2>/dev/null || true
  fi
  if [[ -d "${ROOT_DIR}/.tmp-sanitized-specs" ]]; then
    rmdir "${ROOT_DIR}/.tmp-sanitized-specs" 2>/dev/null || true
  fi
}
trap cleanup_tmp_specs EXIT

if [[ ! -f "${CONFIG_FILE}" ]]; then
  echo "Error: config not found: ${CONFIG_FILE}" >&2
  exit 1
fi

detect_module_base() {
  local url host path

  if ! command -v git >/dev/null 2>&1; then
    return 1
  fi

  url="$(git -C "${ROOT_DIR}" config --get remote.origin.url 2>/dev/null || true)"
  if [[ -z "${url}" ]]; then
    return 1
  fi

  if [[ "${url}" =~ ^git@([^:]+):(.+)$ ]]; then
    host="${BASH_REMATCH[1]}"
    path="${BASH_REMATCH[2]}"
  elif [[ "${url}" =~ ^https?://([^/]+)/(.+)$ ]]; then
    host="${BASH_REMATCH[1]}"
    path="${BASH_REMATCH[2]}"
  elif [[ "${url}" =~ ^ssh://git@([^/]+)/(.+)$ ]]; then
    host="${BASH_REMATCH[1]}"
    path="${BASH_REMATCH[2]}"
  else
    return 1
  fi

  path="${path%.git}"
  echo "${host}/${path}"
}

if [[ -z "${GO_MODULE_BASE}" ]]; then
  GO_MODULE_BASE="$(detect_module_base || true)"
fi
GO_MODULE_BASE="${GO_MODULE_BASE%/}"

read_specs() {
  awk '
    $1=="specs:" {inside=1; next}
    inside && $0 ~ /^[^[:space:]]/ {inside=0}
    inside && $1=="-" {print $2}
  ' "${CONFIG_FILE}"
}

read_languages() {
  awk '
    $1=="languages:" {inside=1; next}
    inside && $0 ~ /^[^[:space:]]/ {inside=0}
    inside {
      if ($1=="-" && $2=="name:") {
        if (name!="") print name "|" gen "|" out "|" prefix "|" tdir
        name=$3; gen=""; out=""; prefix=""; tdir=""
      } else if ($1=="generator:") {gen=$2}
      else if ($1=="output_dir:") {out=$2}
      else if ($1=="package_name_prefix:") {prefix=$2}
      else if ($1=="template_dir:") {tdir=$2}
    }
    END { if (name!="") print name "|" gen "|" out "|" prefix "|" tdir }
  ' "${CONFIG_FILE}"
}

sanitize_package_name() {
  local name="$1"
  name="$(echo "${name}" | tr '[:upper:]' '[:lower:]')"
  name="$(echo "${name}" | tr -c 'a-z0-9_' '_')"
  name="$(echo "${name}" | sed -E 's/_+/_/g; s/^_+//; s/_+$//')"
  echo "${name}"
}

sanitize_npm_name() {
  local name="$1"
  name="$(echo "${name}" | tr '[:upper:]' '[:lower:]')"
  name="$(echo "${name}" | tr '_' '-')"
  name="$(echo "${name}" | tr -c 'a-z0-9-' '-')"
  name="$(echo "${name}" | sed -E 's/-+/-/g; s/^-+//; s/-+$//')"
  if [[ -z "${name}" ]]; then
    name="package"
  fi
  echo "${name}"
}

is_npm_generator() {
  local generator="$1"
  if [[ "${generator}" == typescript* || "${generator}" == javascript* ]]; then
    return 0
  fi
  return 1
}

strip_numeric_prefix() {
  local name="$1"
  name="$(echo "${name}" | sed -E 's/^[0-9]+[-_]+//')"
  if [[ -z "${name}" ]]; then
    name="$1"
  fi
  echo "${name}"
}

normalize_dir_name() {
  local name="$1"
  name="$(echo "${name}" | tr '-' '_')"
  echo "${name}"
}

to_pascal_case() {
  local name="$1"
  name="${name//-/_}"
  echo "${name}" | awk -F_ '{
    out = ""
    for (i = 1; i <= NF; i++) {
      if ($i == "") continue
      out = out toupper(substr($i, 1, 1)) substr($i, 2)
    }
    printf "%s", out
  }'
}

# openapi-generator never deletes files it no longer produces. When a schema is
# renamed (e.g. 409SupplyDeliverError -> Model409SupplyDeliverError via the
# digit-name sanitizer), the old model file lingers next to the new one, which
# breaks the build (invalid identifiers, or "redeclared in this block"). The
# Python path sidesteps this with a full `rm -rf` before generation, but the
# other languages generate in place to preserve non-generated tracked files
# (notably Go's go.sum, plus Cargo.toml/composer.json/package.json). So purge
# only the always-regenerated model/api sources here; everything removed is
# recreated by the generator in the same run.
purge_regenerated_sources() {
  local generator="$1"
  local dir="$2"
  [[ -d "${dir}" ]] || return 0

  case "${generator}" in
    go)
      rm -f "${dir}"/model_*.go "${dir}"/api_*.go
      ;;
    php)
      rm -f "${dir}"/lib/Model/*.php "${dir}"/lib/Api/*.php
      ;;
    rust)
      rm -f "${dir}"/src/models/*.rs "${dir}"/src/apis/*.rs
      ;;
    typescript*|javascript*)
      rm -f "${dir}"/src/models/*.ts "${dir}"/src/apis/*.ts
      ;;
  esac
}

cleanup_output_dir() {
  local dir="$1"
  local files=(
    "README.md"
    ".gitignore"
    ".gitlab-ci.yml"
    ".openapi-generator-ignore"
    ".travis.yml"
    "git_push.sh"
    "pyproject.toml"
    "requirements.txt"
    "setup.cfg"
    "setup.py"
    "test-requirements.txt"
    "tox.ini"
  )
  local dirs=(
    ".github"
    ".openapi-generator"
    "docs"
    "test"
  )
  local f
  for f in "${files[@]}"; do
    if [[ -f "${dir}/${f}" ]]; then
      rm -f "${dir}/${f}"
    fi
  done
  rm -f "${dir}"/*_README.md
  local d
  for d in "${dirs[@]}"; do
    if [[ -d "${dir}/${d}" ]]; then
      rm -rf "${dir}/${d}"
    fi
  done
}

fix_go_module() {
  local out_path="$1"
  local go_mod
  local rel_path
  local module_path
  local tmp_file

  if [[ -z "${GO_MODULE_BASE}" ]]; then
    return
  fi

  go_mod="${out_path}/go.mod"
  if [[ ! -f "${go_mod}" ]]; then
    return
  fi

  if [[ "${out_path}" != "${ROOT_DIR}/"* ]]; then
    return
  fi

  rel_path="${out_path#${ROOT_DIR}/}"
  module_path="${GO_MODULE_BASE}/${rel_path}"

  tmp_file="$(mktemp)"
  awk -v module="${module_path}" '
    /^module[[:space:]]+/ { print "module " module; updated=1; next }
    { print }
    END { if (!updated) print "module " module }
  ' "${go_mod}" > "${tmp_file}"
  mv "${tmp_file}" "${go_mod}"
}

fix_go_large_ids() {
  local out_path="$1"
  local py_bin=""

  if command -v python3 >/dev/null 2>&1; then
    py_bin="python3"
  elif command -v python >/dev/null 2>&1; then
    py_bin="python"
  else
    echo "Warning: python not found; skipping Go large-id fix in ${out_path}" >&2
    return 0
  fi

  OUT_PATH="${out_path}" "${py_bin}" - <<'PY'
import os
import re
from pathlib import Path

root = Path(os.environ["OUT_PATH"])

replacements = [
    ("LastOrderShkId *int32", "LastOrderShkId *int64"),
    ("GetLastOrderShkId() int32", "GetLastOrderShkId() int64"),
    ("GetLastOrderShkIdOk() (*int32, bool)", "GetLastOrderShkIdOk() (*int64, bool)"),
    ("SetLastOrderShkId gets a reference to the given int32", "SetLastOrderShkId gets a reference to the given int64"),
    ("SetLastOrderShkId(v int32)", "SetLastOrderShkId(v int64)"),
]

for path in root.rglob("*.go"):
    text = path.read_text(encoding="utf-8")
    if "LastOrderShkId" not in text:
        continue

    new_text = text
    for old, new in replacements:
        new_text = new_text.replace(old, new)

    new_text = re.sub(
        r"(func \(o \*[^)]+\) GetLastOrderShkId\(\) int64 \{.*?)(var ret )int32",
        r"\g<1>\g<2>int64",
        new_text,
        flags=re.S,
    )

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
PY
}

fix_typescript_enum_keys() {
  local dir="$1"
  python3 - <<PY
from pathlib import Path

root = Path("${dir}")

def fix_file(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    in_enum = False
    counter = 1
    changed = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("export const ") and stripped.endswith("= {"):
            in_enum = True
            counter = 1
            out.append(line)
            continue
        if in_enum:
            if stripped.startswith("} as const;"):
                in_enum = False
                out.append(line)
                continue
            if stripped.startswith(":"):
                indent = line[:len(line) - len(line.lstrip())]
                rest = line.lstrip()[1:].lstrip()
                out.append(f"{indent}Value{counter}: {rest}")
                counter += 1
                changed = True
                continue
        out.append(line)

    if changed:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")

for path in root.rglob("*.ts"):
    fix_file(path)
PY
}

fix_rust_authors() {
  local out_path="$1"
  local cargo_file="${out_path}/Cargo.toml"
  if [[ ! -f "${cargo_file}" ]]; then
    return
  fi
  python3 - <<'PY' "${cargo_file}"
from pathlib import Path

path = Path(__file__ if False else __import__("sys").argv[1])
data = path.read_text(encoding="utf-8").splitlines()
out = []
replaced = False
for line in data:
    if line.strip().startswith("authors = "):
        out.append('authors = ["Evgenii Lazarev <elazarev@gmail.com>"]')
        replaced = True
    else:
        out.append(line)
if replaced:
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
PY
}

fix_rust_code() {
  local out_path="$1"
  python3 - <<'PY' "${out_path}"
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])

KNOWN_RENAMES = {
    "Принято": "Accepted",
    "Склад продавца": "SellerWarehouse",
}


def derive_variant_name(value, used, counter):
    if value in KNOWN_RENAMES:
        name = KNOWN_RENAMES[value]
    else:
        cleaned = re.sub(r"[^A-Za-z0-9]+", " ", value).strip()
        parts = [p for p in cleaned.split(" ") if p]
        name = "".join(p[:1].upper() + p[1:] for p in parts)
    if not name or name[0].isdigit():
        name = f"Value{counter}"
    if name in used:
        name = f"{name}{counter}"
    return name


def fix_empty_enum_variants(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    enum_first_variant = {}
    inside_enum = False
    current_enum = None
    used = set()
    counter = 1
    pending_rename = None
    pending_indent = ""

    for line in lines:
        enum_match = re.match(r"\s*pub enum (\w+)", line)
        if enum_match:
            inside_enum = True
            current_enum = enum_match.group(1)
            used = set()
            counter = 1
            pending_rename = None
            pending_indent = ""
            out.append(line)
            continue

        if inside_enum and line.strip() == "}":
            inside_enum = False
            pending_rename = None
            pending_indent = ""
            out.append(line)
            continue

        if inside_enum:
            rename_match = re.match(r'(\s*)#\[serde\(rename = "([^"]*)"\)\]', line)
            if rename_match:
                pending_indent = rename_match.group(1)
                pending_rename = rename_match.group(2)
                out.append(line)
                continue

            if pending_rename is not None and re.match(r"^\s*,\s*$", line):
                name = derive_variant_name(pending_rename, used, counter)
                out.append(f"{pending_indent}{name},")
                used.add(name)
                enum_first_variant.setdefault(current_enum, name)
                counter += 1
                pending_rename = None
                continue

            variant_match = re.match(r"\s*([A-Za-z][A-Za-z0-9_]*)\s*,\s*$", line)
            if variant_match:
                name = variant_match.group(1)
                used.add(name)
                enum_first_variant.setdefault(current_enum, name)

        out.append(line)

    return out, enum_first_variant


def fix_default_impls(lines, enum_first_variant):
    out = []
    current_enum = None
    in_default = False
    for line in lines:
        enum_match = re.match(r"\s*impl Default for (\w+)\s*\{", line)
        if enum_match:
            current_enum = enum_match.group(1)
            in_default = True
            out.append(line)
            continue

        if in_default and line.strip() == "}":
            in_default = False
            current_enum = None
            out.append(line)
            continue

        if in_default and re.match(r"\s*Self::\s*$", line):
            replacement = enum_first_variant.get(current_enum)
            if replacement:
                indent = re.match(r"(\s*)", line).group(1)
                out.append(f"{indent}Self::{replacement}")
                continue

        out.append(line)

    return out


def fix_multipart_vectors(path):
    text = path.read_text(encoding="utf-8")
    vec_vars = set(
        re.findall(r"([A-Za-z0-9_]+)\s*:\s*Vec\s*<\s*std::path::PathBuf\s*>", text)
    )
    option_vec_vars = set(
        re.findall(r"([A-Za-z0-9_]+)\s*:\s*Option\s*<\s*Vec\s*<\s*std::path::PathBuf\s*>\s*>", text)
    )
    for alias, target in re.findall(r"let\s+([A-Za-z0-9_]+)\s*=\s*([A-Za-z0-9_]+)\s*;", text):
        if target in vec_vars:
            vec_vars.add(alias)
        if target in option_vec_vars:
            option_vec_vars.add(alias)
    if not vec_vars and not option_vec_vars:
        vec_vars = set()

    def replace_option_vec_stream(match):
        src = match.group("src")
        if src not in option_vec_vars:
            return match.group(0)
        indent = match.group("indent")
        alias = match.group("alias")
        field = match.group("field")
        inner_indent = indent + "    "
        inner_inner_indent = inner_indent + "    "
        return (
            f"{indent}if let Some(ref {alias}) = {src} {{\n"
            f"{inner_indent}for file_path in {alias} {{\n"
            f"{inner_inner_indent}let file = TokioFile::open(file_path).await?;\n"
            f"{inner_inner_indent}let stream = FramedRead::new(file, BytesCodec::new());\n"
            f"{inner_inner_indent}let file_name = file_path.file_name().map(|n| n.to_string_lossy().to_string()).unwrap_or_default();\n"
            f"{inner_inner_indent}let file_part = reqwest::multipart::Part::stream(reqwest::Body::wrap_stream(stream)).file_name(file_name);\n"
            f"{inner_inner_indent}multipart_form = multipart_form.part(\"{field}\", file_part);\n"
            f"{inner_indent}}}\n"
            f"{indent}}}"
        )

    def replace_vec_stream(match):
        var = match.group("var")
        if var not in vec_vars:
            return match.group(0)
        indent = match.group("indent")
        field = match.group("field")
        inner_indent = indent + "    "
        return (
            f"{indent}for file_path in &{var} {{\n"
            f"{inner_indent}let file = TokioFile::open(file_path).await?;\n"
            f"{inner_indent}let stream = FramedRead::new(file, BytesCodec::new());\n"
            f"{inner_indent}let file_name = file_path.file_name().map(|n| n.to_string_lossy().to_string()).unwrap_or_default();\n"
            f"{inner_indent}let file_part = reqwest::multipart::Part::stream(reqwest::Body::wrap_stream(stream)).file_name(file_name);\n"
            f"{inner_indent}multipart_form = multipart_form.part(\"{field}\", file_part);\n"
            f"{indent}}}"
        )

    option_stream_pattern = re.compile(
        r'(?m)^(?P<indent>\s*)if let Some\(ref (?P<alias>[A-Za-z0-9_]+)\) = (?P<src>[A-Za-z0-9_]+)\s*\{\n'
        r'(?P=indent)\s+let file = TokioFile::open\((?P=alias)\)\.await\?;\n'
        r'(?P=indent)\s+let stream = FramedRead::new\(file, BytesCodec::new\(\)\);\n'
        r'(?P=indent)\s+let file_name = (?P=alias)\.file_name\(\)\.map\(\|n\| n\.to_string_lossy\(\)\.to_string\(\)\)\.unwrap_or_default\(\);\n'
        r'(?P=indent)\s+let file_part = reqwest::multipart::Part::stream\(reqwest::Body::wrap_stream\(stream\)\)\.file_name\(file_name\);\n'
        r'(?P=indent)\s+multipart_form = multipart_form\.part\("(?P<field>[^"]+)", file_part\);\n'
        r'(?P=indent)\}'
    )
    vec_stream_pattern = re.compile(
        r'(?m)^(?P<indent>\s*)let file = TokioFile::open\(&?(?P<var>[A-Za-z0-9_]+)\)\.await\?;\n'
        r'(?P=indent)let stream = FramedRead::new\(file, BytesCodec::new\(\)\);\n'
        r'(?P=indent)let file_name = (?P=var)\.file_name\(\)\.map\(\|n\| n\.to_string_lossy\(\)\.to_string\(\)\)\.unwrap_or_default\(\);\n'
        r'(?P=indent)let file_part = reqwest::multipart::Part::stream\(reqwest::Body::wrap_stream\(stream\)\)\.file_name\(file_name\);\n'
        r'(?P=indent)multipart_form = multipart_form\.part\("(?P<field>[^"]+)", file_part\);'
    )
    text = option_stream_pattern.sub(replace_option_vec_stream, text)
    text = vec_stream_pattern.sub(replace_vec_stream, text)

    lines = text.splitlines()
    out = []
    option_param_vars = {}
    depth = 0
    for line in lines:
        to_remove = [name for name, d in option_param_vars.items() if d > depth]
        for name in to_remove:
            option_param_vars.pop(name, None)

        option_match = re.match(r"\s*if let Some\(ref ([A-Za-z0-9_]+)\) = ([A-Za-z0-9_]+)\s*\{", line)
        if option_match and option_match.group(2) in option_vec_vars:
            option_param_vars[option_match.group(1)] = depth + 1
        match = re.match(r'(\s*)multipart_form\s*=\s*multipart_form\.file\("([^"]+)",\s*([A-Za-z0-9_]+)\.as_os_str\(\)\)\.await\?;', line)
        if match and (match.group(3) in vec_vars or match.group(3) in option_param_vars):
            indent, field, var = match.groups()
            out.append(f"{indent}for file_path in {var} {{")
            out.append(f"{indent}    multipart_form = multipart_form.file(\"{field}\", file_path).await?;")
            out.append(f"{indent}}}")
            continue
        out.append(line)
        depth += line.count("{") - line.count("}")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def ensure_uuid_dependency(root):
    cargo = root / "Cargo.toml"
    if not cargo.exists():
        return
    cargo_text = cargo.read_text(encoding="utf-8")
    if "uuid =" in cargo_text:
        return
    uses_uuid = any("uuid::" in p.read_text(encoding="utf-8") for p in root.rglob("src/**/*.rs"))
    if not uses_uuid:
        return

    lines = cargo_text.splitlines()
    dep_start = None
    dep_end = len(lines)
    for idx, line in enumerate(lines):
        if line.strip() == "[dependencies]":
            dep_start = idx
            continue
        if dep_start is not None and idx > dep_start and line.startswith("[") and line.endswith("]"):
            dep_end = idx
            break
    if dep_start is None:
        return

    insert_at = dep_end
    for idx in range(dep_start + 1, dep_end):
        if lines[idx].startswith("url "):
            insert_at = idx + 1
            break

    lines.insert(insert_at, 'uuid = { version = "^1.8", features = ["serde", "v4"] }')
    cargo.write_text("\n".join(lines) + "\n", encoding="utf-8")


def ensure_reqwest_stream(root):
    cargo = root / "Cargo.toml"
    if not cargo.exists():
        return
    text = cargo.read_text(encoding="utf-8")
    if "reqwest =" not in text or "features" not in text:
        return
    if "stream" in text:
        return
    uses_file = any("multipart_form.file" in p.read_text(encoding="utf-8") for p in root.rglob("src/**/*.rs"))
    if not uses_file:
        return

    lines = text.splitlines()
    out = []
    updated = False
    for line in lines:
        if line.strip().startswith("reqwest =") and "features" in line and "[" in line and "]" in line:
            prefix, rest = line.split("features = [", 1)
            features_part, suffix = rest.split("]", 1)
            features = [f.strip().strip('"') for f in features_part.split(",") if f.strip()]
            if "stream" not in features:
                features.append("stream")
                updated = True
            features_rendered = ", ".join(f"\"{f}\"" for f in features)
            line = f"{prefix}features = [{features_rendered}]{suffix}"
        out.append(line)
    if updated:
        cargo.write_text("\n".join(out) + "\n", encoding="utf-8")


def ensure_cargo_metadata(root):
    cargo = root / "Cargo.toml"
    if not cargo.exists():
        return
    lines = cargo.read_text(encoding="utf-8").splitlines()
    package_start = None
    package_end = len(lines)
    crate_name = None
    for idx, line in enumerate(lines):
        if line.strip() == "[package]":
            package_start = idx
            continue
        if package_start is not None and idx > package_start and line.startswith("[") and line.endswith("]"):
            package_end = idx
            break
        if crate_name is None:
            match = re.match(r'\s*name\s*=\s*"([^"]+)"', line)
            if match:
                crate_name = match.group(1)

    if package_start is None:
        return

    desired_description = "Wildberries OpenAPI client (generated)."
    desired_license = "MIT"
    desired_repo = "https://github.com/eslazarev/wildberries-sdk"
    desired_homepage = desired_repo
    desired_doc = f"https://docs.rs/{crate_name}" if crate_name else None

    found = {"description": False, "license": False, "repository": False, "homepage": False, "documentation": False}
    for idx in range(package_start + 1, package_end):
        line = lines[idx]
        if line.strip().startswith("description ="):
            lines[idx] = f'description = "{desired_description}"'
            found["description"] = True
        elif line.strip().startswith("license ="):
            lines[idx] = f'license = "{desired_license}"'
            found["license"] = True
        elif line.strip().startswith("repository ="):
            lines[idx] = f'repository = "{desired_repo}"'
            found["repository"] = True
        elif line.strip().startswith("homepage ="):
            lines[idx] = f'homepage = "{desired_homepage}"'
            found["homepage"] = True
        elif line.strip().startswith("documentation =") and desired_doc:
            lines[idx] = f'documentation = "{desired_doc}"'
            found["documentation"] = True

    insert_at = package_start + 1
    for idx in range(package_start + 1, package_end):
        if lines[idx].strip().startswith("description ="):
            insert_at = idx + 1
            break

    def insert_if_missing(key, line):
        nonlocal insert_at
        if not found[key]:
            lines.insert(insert_at, line)
            insert_at += 1

    insert_if_missing("description", f'description = "{desired_description}"')
    insert_if_missing("license", f'license = "{desired_license}"')
    insert_if_missing("repository", f'repository = "{desired_repo}"')
    insert_if_missing("homepage", f'homepage = "{desired_homepage}"')
    if desired_doc:
        insert_if_missing("documentation", f'documentation = "{desired_doc}"')

    cargo.write_text("\n".join(lines) + "\n", encoding="utf-8")


for model_path in root.glob("src/models/*.rs"):
    updated_lines, first_variants = fix_empty_enum_variants(model_path)
    updated_lines = fix_default_impls(updated_lines, first_variants)
    model_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")

for api_path in root.glob("src/apis/*.rs"):
    fix_multipart_vectors(api_path)
ensure_uuid_dependency(root)
ensure_reqwest_stream(root)
ensure_cargo_metadata(root)
PY
}

fix_rust_large_ids() {
  local out_path="$1"
  local py_bin=""

  if command -v python3 >/dev/null 2>&1; then
    py_bin="python3"
  elif command -v python >/dev/null 2>&1; then
    py_bin="python"
  else
    echo "Warning: python not found; skipping Rust large-id fix in ${out_path}" >&2
    return 0
  fi

  OUT_PATH="${out_path}" "${py_bin}" - <<'PY'
import os
from pathlib import Path

root = Path(os.environ["OUT_PATH"])

for path in root.rglob("*.rs"):
    text = path.read_text(encoding="utf-8")
    if "last_order_shk_id" not in text:
        continue
    new_text = text.replace("last_order_shk_id: Option<i32>", "last_order_shk_id: Option<i64>")
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
PY
}

fix_php_host_override() {
  local out_path="$1"
  python3 - <<'PY' "${out_path}"
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])

# --- Fix Configuration.php ---
for cfg in root.glob("lib/Configuration.php"):
    text = cfg.read_text(encoding="utf-8")
    if "hostOverridden" in text:
        continue

    # Add property after the existing $host property block
    text = text.replace(
        "protected $host = 'http://localhost';",
        "protected $host = 'http://localhost';\n\n"
        "    /**\n"
        "     * Whether setHost() has been called\n"
        "     *\n"
        "     * @var bool\n"
        "     */\n"
        "    protected $hostOverridden = false;",
    )

    # Update setHost to track override
    text = text.replace(
        "    public function setHost($host)\n"
        "    {\n"
        "        $this->host = $host;\n"
        "        return $this;\n"
        "    }",
        "    public function setHost($host)\n"
        "    {\n"
        "        $this->host = $host;\n"
        "        $this->hostOverridden = true;\n"
        "        return $this;\n"
        "    }",
    )

    # Add isHostOverridden() after getHost()
    text = text.replace(
        "    public function getHost()\n"
        "    {\n"
        "        return $this->host;\n"
        "    }",
        "    public function getHost()\n"
        "    {\n"
        "        return $this->host;\n"
        "    }\n"
        "\n"
        "    /**\n"
        "     * Returns whether setHost() has been explicitly called\n"
        "     *\n"
        "     * @return bool\n"
        "     */\n"
        "    public function isHostOverridden()\n"
        "    {\n"
        "        return $this->hostOverridden;\n"
        "    }",
    )

    cfg.write_text(text, encoding="utf-8")

# --- Fix Api files ---
for api in root.glob("lib/Api/*Api.php"):
    text = api.read_text(encoding="utf-8")
    if "$this->config->isHostOverridden()" in text:
        continue
    text = text.replace(
        "$operationHost = Configuration::getHostString($hostSettings, $hostIndex, $variables);",
        "$operationHost = $this->config->isHostOverridden()\n"
        "            ? $this->config->getHost()\n"
        "            : Configuration::getHostString($hostSettings, $hostIndex, $variables);",
    )
    api.write_text(text, encoding="utf-8")
PY
}

rewrite_typescript_index() {
  local out_path="$1"
  local index_file="${out_path}/src/index.ts"
  if [[ ! -f "${index_file}" ]]; then
    return
  fi
  cat > "${index_file}" <<'TS'
/* tslint:disable */
/* eslint-disable */
export * from './apis/index';
export * from './models/index';
export {
  BASE_PATH,
  Configuration,
  ConfigurationParameters,
  DefaultConfig,
  BaseAPI,
  FetchError,
  RequiredError,
  COLLECTION_FORMATS,
  FetchAPI,
  Json,
  HTTPMethod,
  HTTPHeaders,
  HTTPQuery,
  HTTPBody,
  HTTPRequestInit,
  ModelPropertyNaming,
  InitOverrideFunction,
  FetchParams,
  RequestOpts,
  Consume,
  RequestContext,
  ResponseContext,
  ErrorContext,
  Middleware,
  ApiResponse,
  ResponseTransformer,
  JSONApiResponse,
  VoidApiResponse,
  BlobApiResponse,
  TextApiResponse,
  querystring,
  exists,
  mapValues,
  canConsumeForm,
} from './runtime';
export { ResponseError as RuntimeResponseError } from './runtime';
TS
}

flatten_python_package() {
  local out_path="$1"
  local old_pkg="$2"
  local new_subpkg="$3"
  local pkg_dir="${out_path}/${old_pkg}"

  if [[ ! -d "${pkg_dir}" ]]; then
    return
  fi

  shopt -s dotglob
  for item in "${pkg_dir}"/*; do
    mv "${item}" "${out_path}/"
  done
  shopt -u dotglob
  rmdir "${pkg_dir}" || true

  python3 - <<PY
from pathlib import Path

root = Path("${out_path}")
old = "${old_pkg}"
new = "wildberries_sdk.${new_subpkg}"

for path in root.rglob("*.py"):
    data = path.read_text(encoding="utf-8")
    if old in data:
        path.write_text(data.replace(old, new), encoding="utf-8")
PY
}

rewrite_python_tags() {
  local input="$1"
  local output="$2"

  python3 - <<'PY' "${input}" "${output}"
from pathlib import Path
import sys

src = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
out_lines = []

in_tags = False
tags_indent = None
rewrite_items = False

for line in src:
    stripped = line.lstrip()
    indent = len(line) - len(stripped)
    if stripped == "tags:":
        in_tags = True
        tags_indent = indent
        rewrite_items = indent > 0
        out_lines.append(line)
        continue

    if in_tags:
        if stripped and indent <= tags_indent:
            in_tags = False
            rewrite_items = False
        if rewrite_items and stripped.startswith("- ") and indent > tags_indent:
            if ":" not in stripped[2:]:
                out_lines.append(" " * indent + "- Default")
                continue

    out_lines.append(line)

Path(sys.argv[2]).write_text("\n".join(out_lines) + "\n", encoding="utf-8")
PY
}

sanitize_digit_schema_names() {
  local input="$1"
  local output="$2"

  python3 - "${input}" "${output}" <<'PY'
import re
import shutil
import sys

src, dst = sys.argv[1], sys.argv[2]
with open(src, encoding="utf-8") as f:
    text = f.read()

# Collect schema names under components.schemas (keys at indent 4).
all_names = set()
digit_names = []
in_components = False
in_schemas = False
for line in text.split("\n"):
    stripped = line.strip()
    if not stripped:
        continue
    indent = len(line) - len(line.lstrip())
    if re.match(r"^components:\s*$", line):
        in_components = True
        in_schemas = False
        continue
    if in_components and indent == 0:
        in_components = False
        in_schemas = False
    elif in_components and indent == 2:
        in_schemas = bool(re.match(r"^\s*schemas:\s*$", line))
    elif in_components and in_schemas and indent == 4:
        m = re.match(r"^    ([^\s:]+):\s*$", line)
        if m:
            all_names.add(m.group(1))
            if m.group(1)[0].isdigit():
                digit_names.append(m.group(1))

if not digit_names:
    shutil.copyfile(src, dst)
    sys.exit(0)

for name in digit_names:
    new_name = f"Model{name}"
    if new_name in all_names:
        print(f"Warning: cannot rename schema {name}: {new_name} already exists", file=sys.stderr)
        continue
    text = re.sub(
        rf"^    {re.escape(name)}:\s*$",
        f"    {new_name}:",
        text,
        count=1,
        flags=re.M,
    )
    text = re.sub(
        rf"(#/components/schemas/){re.escape(name)}(['\"\s])",
        rf"\g<1>{new_name}\g<2>",
        text,
    )
    print(f"Renamed digit-leading schema: {name} -> {new_name}", file=sys.stderr)

with open(dst, "w", encoding="utf-8") as f:
    f.write(text)
PY
}

to_container_path() {
  local path="$1"
  if [[ "${path}" != "${ROOT_DIR}/"* ]]; then
    echo "Error: path not under repo for docker: ${path}" >&2
    exit 1
  fi
  echo "/local/${path#${ROOT_DIR}/}"
}

GENERATOR_BIN="${OPENAPI_GENERATOR:-}"
if [[ "${USE_DOCKER}" == "1" ]]; then
  if ! command -v docker >/dev/null 2>&1; then
    echo "Error: docker not found (OPENAPI_GENERATOR_DOCKER=1)." >&2
    exit 1
  fi
  docker_user_args=()
  if command -v id >/dev/null 2>&1; then
    uid="$(id -u)"
    gid="$(id -g)"
    if [[ -n "${uid}" && -n "${gid}" ]]; then
      docker_user_args=(--user "${uid}:${gid}")
    fi
  fi
else
  if [[ -z "${GENERATOR_BIN}" ]]; then
    if command -v openapi-generator-cli >/dev/null 2>&1; then
      GENERATOR_BIN="openapi-generator-cli"
    elif command -v openapi-generator >/dev/null 2>&1; then
      GENERATOR_BIN="openapi-generator"
    else
      echo "Error: openapi-generator-cli/openapi-generator not found." >&2
      exit 1
    fi
  fi
fi

specs=()
while IFS= read -r spec; do
  [[ -n "${spec}" ]] && specs+=("${spec}")
done < <(read_specs)

if [[ "${#specs[@]}" -eq 0 ]]; then
  echo "Error: no specs found in ${CONFIG_FILE}" >&2
  exit 1
fi

inputs=()
for spec in "${specs[@]}"; do
  if [[ "${spec}" =~ ^https?:// ]]; then
    local_path="${ROOT_DIR}/specs/$(basename "${spec%%\?*}")"
    if [[ ! -f "${local_path}" ]]; then
      echo "Error: missing downloaded spec: ${local_path}" >&2
      exit 1
    fi
    inputs+=("${local_path}")
  else
    if [[ "${spec}" = /* ]]; then
      inputs+=("${spec}")
    else
      inputs+=("${ROOT_DIR}/${spec}")
    fi
  fi
done

# Schema names starting with a digit (e.g. 409SupplyDeliverError) break the Go
# and PHP generators: the top-level model gets a Model prefix, but inline
# sub-schemas keep the digit-leading name and produce invalid identifiers.
# Renaming to Model<name> in the spec matches what the generators already emit
# for the top-level model, so no public API changes in any language.
sanitized_dir="${ROOT_DIR}/.tmp-sanitized-specs"
mkdir -p "${sanitized_dir}"
sanitized_inputs=()
for input in "${inputs[@]}"; do
  sanitized="${sanitized_dir}/$(basename "${input}")"
  sanitize_digit_schema_names "${input}" "${sanitized}"
  TMP_SPECS+=("${sanitized}")
  sanitized_inputs+=("${sanitized}")
done
inputs=("${sanitized_inputs[@]}")

langs=()
while IFS= read -r lang; do
  [[ -n "${lang}" ]] && langs+=("${lang}")
done < <(read_languages)

if [[ "${#langs[@]}" -eq 0 ]]; then
  echo "Error: no languages found in ${CONFIG_FILE}" >&2
  exit 1
fi

extra_args=()
if [[ -n "${OPENAPI_GENERATOR_EXTRA_ARGS:-}" ]]; then
  read -r -a extra_args <<< "${OPENAPI_GENERATOR_EXTRA_ARGS}"
fi

for lang in "${langs[@]}"; do
  IFS='|' read -r name generator out_dir prefix template_dir <<< "${lang}"
  if [[ -z "${generator}" || -z "${out_dir}" ]]; then
    echo "Error: invalid language entry in ${CONFIG_FILE}: ${lang}" >&2
    exit 1
  fi

  if [[ "${out_dir}" = /* ]]; then
    out_root="${out_dir}"
  else
    out_root="${ROOT_DIR}/${out_dir}"
  fi

  template_arg=""
  if [[ -n "${template_dir}" ]]; then
    if [[ "${template_dir}" != /* ]]; then
      template_dir="${ROOT_DIR}/${template_dir}"
    fi
    if [[ -d "${template_dir}" ]]; then
      template_arg="${template_dir}"
    else
      echo "Warning: template_dir not found, skipping: ${template_dir}" >&2
    fi
  fi

  for input in "${inputs[@]}"; do
    input_path="${input}"
    tmp_spec=""
    filename="$(basename "${input}")"
    base="$(basename "${filename}" .yaml)"
    base="${base%.yml}"
    base="$(strip_numeric_prefix "${base}")"
    dir_name="$(normalize_dir_name "${base}")"

    out_path="${out_root}/${dir_name}"
    pkg="${base}"
    if [[ -n "${prefix}" ]]; then
      pkg="${prefix}_${base}"
    fi
    pkg="$(sanitize_package_name "${pkg}")"
    additional_props="packageName=${pkg},packageVersion=${PACKAGE_VERSION}"
    if is_npm_generator "${generator}"; then
      npm_pkg="${base}"
      if [[ -n "${prefix}" ]]; then
        npm_pkg="${prefix}-${base}"
      fi
      npm_pkg="$(sanitize_npm_name "${npm_pkg}")"
      additional_props="${additional_props},npmName=${npm_pkg},npmVersion=${PACKAGE_VERSION}"
    fi
    if [[ "${generator}" == "python" ]]; then
      additional_props="${additional_props},useTags=false"
    fi
    if [[ "${generator}" == "php" ]]; then
      module_ns="$(to_pascal_case "${dir_name}")"
      additional_props="${additional_props},invokerPackage=Wildberries\\Sdk\\${module_ns}"
    fi

    echo "Generating ${name} for ${filename}"
    if [[ "${generator}" != "python" ]]; then
      purge_regenerated_sources "${generator}" "${out_path}"
    fi
    if [[ "${generator}" == "python" ]]; then
      rm -rf "${out_path}"
      tmp_dir="${ROOT_DIR}/.tmp-python-specs"
      mkdir -p "${tmp_dir}"
      tmp_spec="${tmp_dir}/${filename}"
      rewrite_python_tags "${input}" "${tmp_spec}"
      TMP_SPECS+=("${tmp_spec}")
      input_path="${tmp_spec}"
    fi
    if [[ "${USE_DOCKER}" == "1" ]]; then
      in_container="$(to_container_path "${input_path}")"
      out_container="$(to_container_path "${out_path}")"
      cmd=(
        docker run --rm
        "${docker_user_args[@]}"
        -v "${ROOT_DIR}:/local"
        -w /local
        "${DOCKER_IMAGE}"
        generate
        -g "${generator}"
        -i "${in_container}"
        -o "${out_container}"
        --additional-properties "${additional_props}"
      )
    else
      cmd=(
        "${GENERATOR_BIN}" generate
        -g "${generator}"
        -i "${input_path}"
        -o "${out_path}"
        --additional-properties "${additional_props}"
      )
    fi
    if [[ "${SKIP_VALIDATE_SPEC}" == "1" ]]; then
      cmd+=(--skip-validate-spec)
    fi
    if [[ -n "${GLOBAL_PROPERTIES}" ]]; then
      cmd+=(--global-property "${GLOBAL_PROPERTIES}")
    fi
    if [[ -n "${template_arg}" ]]; then
      cmd+=(-t "${template_arg}")
    fi
    if [[ "${#extra_args[@]}" -gt 0 ]]; then
      cmd+=("${extra_args[@]}")
    fi
    "${cmd[@]}"
    if [[ "${generator}" == "python" ]]; then
      new_subpkg="$(sanitize_package_name "${dir_name}")"
      flatten_python_package "${out_path}" "${pkg}" "${new_subpkg}"
    fi
    if is_npm_generator "${generator}"; then
      fix_typescript_enum_keys "${out_path}"
      rewrite_typescript_index "${out_path}"
    fi
    cleanup_output_dir "${out_path}"
    if [[ "${generator}" == "go" ]]; then
      if [[ -z "${GO_MODULE_BASE}" && "${GO_MODULE_BASE_WARNED}" -eq 0 ]]; then
        echo "Warning: GO_MODULE_BASE not set and git remote not detected; go.mod will keep default module path." >&2
        GO_MODULE_BASE_WARNED=1
      fi
      fix_go_large_ids "${out_path}"
      fix_go_module "${out_path}"
    fi
    if [[ "${generator}" == "rust" ]]; then
      fix_rust_authors "${out_path}"
      fix_rust_large_ids "${out_path}"
      fix_rust_code "${out_path}"
    fi
    if [[ "${generator}" == "php" ]]; then
      fix_php_host_override "${out_path}"
    fi
  done
done
