#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="${ROOT_DIR}/generation.yaml"
PACKAGE_VERSION="${PACKAGE_VERSION:-0.1.0}"
SKIP_VALIDATE_SPEC="${SKIP_VALIDATE_SPEC:-1}"
USE_DOCKER="${OPENAPI_GENERATOR_DOCKER:-0}"
DOCKER_IMAGE="${OPENAPI_GENERATOR_DOCKER_IMAGE:-openapitools/openapi-generator-cli}"
GLOBAL_PROPERTIES="${OPENAPI_GENERATOR_GLOBAL_PROPERTIES:-apiDocs=false,modelDocs=false,apiTests=false,modelTests=false}"

if [[ ! -f "${CONFIG_FILE}" ]]; then
  echo "Error: config not found: ${CONFIG_FILE}" >&2
  exit 1
fi

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
    local_path="${ROOT_DIR}/specs/$(basename "${spec}")"
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

    echo "Generating ${name} for ${filename}"
    if [[ "${USE_DOCKER}" == "1" ]]; then
      in_container="$(to_container_path "${input}")"
      out_container="$(to_container_path "${out_path}")"
      cmd=(
        docker run --rm
        -v "${ROOT_DIR}:/local"
        -w /local
        "${DOCKER_IMAGE}"
        generate
        -g "${generator}"
        -i "${in_container}"
        -o "${out_container}"
        --additional-properties "packageName=${pkg},packageVersion=${PACKAGE_VERSION}"
      )
    else
      cmd=(
        "${GENERATOR_BIN}" generate
        -g "${generator}"
        -i "${input}"
        -o "${out_path}"
        --additional-properties "packageName=${pkg},packageVersion=${PACKAGE_VERSION}"
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
    cleanup_output_dir "${out_path}"
  done
done
