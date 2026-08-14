#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="${ROOT_DIR}/generation.yaml"
SPECS_DIR="${ROOT_DIR}/specs"

if [[ ! -f "${CONFIG_FILE}" ]]; then
  echo "Error: config not found: ${CONFIG_FILE}" >&2
  exit 1
fi

# Specs are fetched ONLY from the public S3 mirror populated out-of-band by the
# wb-spec-downloader (which runs headful Chrome from a non-flagged IP and uploads
# the YAMLs to S3). Direct download from Wildberries is not attempted here — its
# WBAAS anti-bot blocks CI. generation.yaml stays the source of truth for the
# filenames: the downloader names each object by basename(url), so
# <S3_URL>/<basename> lines up with what it uploaded.
if [[ -z "${S3_URL:-}" ]]; then
  echo "Error: S3_URL is not set; specs are served only from the S3 mirror." >&2
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

specs=()
while IFS= read -r spec; do
  [[ -n "${spec}" ]] && specs+=("${spec}")
done < <(read_specs)

if [[ "${#specs[@]}" -eq 0 ]]; then
  echo "Error: no specs found in ${CONFIG_FILE}" >&2
  exit 1
fi

base="${S3_URL%/}"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "${tmp_dir}"' EXIT

echo "Downloading specs from S3 mirror: ${base}"
for spec in "${specs[@]}"; do
  if [[ ! "${spec}" =~ ^https?:// ]]; then
    echo "Skipping non-URL spec: ${spec}"
    continue
  fi
  filename="$(basename "${spec%%\?*}")"
  tmp_file="${tmp_dir}/${filename}"
  url="${base}/${filename}"
  if ! curl -fsSL --max-time 60 -o "${tmp_file}" "${url}"; then
    echo "Error: failed to fetch ${url}" >&2
    exit 1
  fi
  if ! head -c 16 "${tmp_file}" | grep -q '^openapi:'; then
    echo "Error: ${url} did not return OpenAPI YAML" >&2
    exit 1
  fi
  mv "${tmp_file}" "${SPECS_DIR}/${filename}"
  echo "s3: ${filename}"
done

echo "All specs downloaded from S3."
