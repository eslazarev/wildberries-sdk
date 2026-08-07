#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_DIR="${ROOT_DIR}/scripts"
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

specs=()
while IFS= read -r spec; do
  [[ -n "${spec}" ]] && specs+=("${spec}")
done < <(read_specs)

if [[ "${#specs[@]}" -eq 0 ]]; then
  echo "Error: no specs found in ${CONFIG_FILE}" >&2
  exit 1
fi

# Preferred source: the public S3 mirror populated out-of-band by the
# wb-spec-downloader (which runs headful Chrome from a non-flagged IP). Plain
# HTTPS, no anti-bot, no creds. The spec list in generation.yaml stays the source
# of truth for the filenames — the downloader names each object by basename(url),
# so <S3_URL>/<basename> lines up with what it uploaded.
try_s3() {
  local base="${S3_URL%/}"
  local tmp_dir
  tmp_dir="$(mktemp -d)"
  trap "rm -rf '${tmp_dir}'" RETURN

  for spec in "${specs[@]}"; do
    if [[ ! "${spec}" =~ ^https?:// ]]; then
      echo "Skipping non-URL spec: ${spec}"
      continue
    fi
    local filename tmp_file url
    filename="$(basename "${spec%%\?*}")"
    url="${base}/${filename}"
    tmp_file="${tmp_dir}/${filename}"
    if ! curl -fsSL --max-time 60 -o "${tmp_file}" "${url}"; then
      echo "Error: failed to fetch ${url}" >&2
      return 1
    fi
    if ! head -c 16 "${tmp_file}" | grep -q '^openapi:'; then
      echo "Error: ${url} did not return OpenAPI YAML" >&2
      return 1
    fi
    mv "${tmp_file}" "${SPECS_DIR}/${filename}"
    echo "s3: ${filename}"
  done
}

# Try plain curl first — it's fast and works from hosts that aren't flagged
# by Wildberries' WBAAS anti-bot (e.g. most CI runners).
try_curl() {
  local tmp_dir
  tmp_dir="$(mktemp -d)"
  trap "rm -rf '${tmp_dir}'" RETURN

  local ua="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

  for spec in "${specs[@]}"; do
    if [[ ! "${spec}" =~ ^https?:// ]]; then
      echo "Skipping non-URL spec: ${spec}"
      continue
    fi
    local filename tmp_file
    filename="$(basename "${spec%%\?*}")"
    tmp_file="${tmp_dir}/${filename}"
    if ! curl -fsSL \
        --max-time 60 \
        -A "${ua}" \
        -H 'Accept: text/yaml,application/yaml,application/x-yaml,text/plain,*/*' \
        -H 'Accept-Language: ru-RU,ru;q=0.9,en;q=0.8' \
        -o "${tmp_file}" \
        "${spec}"; then
      return 1
    fi
    # Detect anti-bot HTML response masquerading as 200.
    if ! head -c 16 "${tmp_file}" | grep -q '^openapi:'; then
      return 1
    fi
    mv "${tmp_file}" "${SPECS_DIR}/${filename}"
    echo "curl: ${filename}"
  done
}

# Fallback: drive a real headful Google Chrome via `patchright` (a Playwright
# fork with deeper CDP patches) that can complete the WBAAS JS challenge.
# WB's v2 anti-bot blocks headless browsers, so we run Chrome headful — under a
# virtual display (xvfb) on headless CI hosts.
run_patchright() {
  if ! command -v node >/dev/null 2>&1 || ! command -v npm >/dev/null 2>&1; then
    echo "Error: node and npm are required for the patchright fallback." >&2
    exit 1
  fi
  export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-${SCRIPT_DIR}/.playwright-browsers}"
  (
    cd "${SCRIPT_DIR}"
    if [[ ! -d node_modules/patchright ]]; then
      echo "Installing patchright..."
      npm install --silent --no-audit --no-fund --no-save patchright@^1.59.4
    fi
    # Install real Google Chrome (channel used by the downloader). Falls back to
    # a system Chrome if the managed install is unavailable.
    npx --no-install patchright install chrome >/dev/null 2>&1 || \
      echo "Warning: 'patchright install chrome' failed; relying on system Chrome." >&2
  )

  # Headful Chrome needs a display. Use xvfb-run when there's no DISPLAY (CI).
  local runner=(node "${SCRIPT_DIR}/download-specs.mjs")
  if [[ -z "${DISPLAY:-}" ]] && command -v xvfb-run >/dev/null 2>&1; then
    xvfb-run -a "${runner[@]}"
  else
    "${runner[@]}"
  fi
}

# When S3_URL is set (CI), use the S3 mirror only — no anti-bot fallback — and
# fail loudly if a spec is missing, so a stale/broken mirror is visible rather
# than silently falling back to the WB path that anti-bot blocks in CI.
if [[ -n "${S3_URL:-}" ]]; then
  echo "Downloading specs from S3 mirror: ${S3_URL%/}"
  if try_s3; then
    echo "All specs downloaded from S3."
    exit 0
  fi
  echo "Error: failed to download specs from S3 (${S3_URL%/})." >&2
  exit 1
fi

if try_curl; then
  echo "All specs downloaded via curl."
  exit 0
fi

echo "curl failed (likely anti-bot challenge); falling back to patchright..."
run_patchright
