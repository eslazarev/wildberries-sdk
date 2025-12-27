#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLIENTS_DIR="${ROOT_DIR}/clients/npm"
NPM_DIR="${ROOT_DIR}/npm"
SRC_DIR="${NPM_DIR}/src"
PACKAGE_VERSION="${PACKAGE_VERSION:-0.1.0}"

if [[ ! -d "${CLIENTS_DIR}" ]]; then
  echo "Error: npm clients not found: ${CLIENTS_DIR}" >&2
  exit 1
fi

rm -rf "${NPM_DIR}"
mkdir -p "${SRC_DIR}"

specs=()
for spec_dir in "${CLIENTS_DIR}"/*; do
  [[ -d "${spec_dir}" ]] || continue
  spec_name="$(basename "${spec_dir}")"
  if [[ ! -d "${spec_dir}/src" ]]; then
    echo "Warning: missing src for ${spec_name}, skipping" >&2
    continue
  fi
  echo "Copying ${spec_name}"
  mkdir -p "${SRC_DIR}/${spec_name}"
  cp -a "${spec_dir}/src/." "${SRC_DIR}/${spec_name}/"
  specs+=("${spec_name}")
done

if [[ "${#specs[@]}" -eq 0 ]]; then
  echo "Error: no npm clients found in ${CLIENTS_DIR}" >&2
  exit 1
fi

IFS=$'\n' specs=($(printf "%s\n" "${specs[@]}" | sort))
unset IFS

{
  echo "// Auto-generated. Do not edit."
  for spec in "${specs[@]}"; do
    echo "export * as ${spec} from \"./${spec}\";"
  done
} > "${SRC_DIR}/index.ts"

cat > "${NPM_DIR}/tsconfig.json" <<'JSON'
{
  "compilerOptions": {
    "declaration": true,
    "target": "es5",
    "module": "commonjs",
    "moduleResolution": "node",
    "rootDir": "src",
    "outDir": "dist",
    "lib": [
      "es6",
      "dom"
    ],
    "typeRoots": [
      "node_modules/@types"
    ]
  },
  "exclude": [
    "dist",
    "node_modules"
  ]
}
JSON

if [[ -f "${ROOT_DIR}/docs/npm/README.md" ]]; then
  cp -f "${ROOT_DIR}/docs/npm/README.md" "${NPM_DIR}/README.md"
fi

if [[ -f "${ROOT_DIR}/LICENSE" ]]; then
  cp -f "${ROOT_DIR}/LICENSE" "${NPM_DIR}/LICENSE"
fi

NPM_DIR_ENV="${NPM_DIR}" PACKAGE_VERSION_ENV="${PACKAGE_VERSION}" python3 - <<'PY'
import json
import os
from pathlib import Path

root = Path(os.environ["NPM_DIR_ENV"])
version = os.environ["PACKAGE_VERSION_ENV"]
src_dir = root / "src"
specs = sorted([p.name for p in src_dir.iterdir() if p.is_dir()])

def fix_enum_keys(path: Path) -> None:
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

for ts_file in src_dir.rglob("*.ts"):
    fix_enum_keys(ts_file)

index_template = """/* tslint:disable */
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
"""

for spec in specs:
    index_file = src_dir / spec / "index.ts"
    if index_file.exists():
        index_file.write_text(index_template + "\n", encoding="utf-8")

exports = {
    ".": {
        "types": "./dist/index.d.ts",
        "default": "./dist/index.js",
    },
    "./package.json": "./package.json",
}
for spec in specs:
    exports[f"./{spec}"] = {
        "types": f"./dist/{spec}/index.d.ts",
        "default": f"./dist/{spec}/index.js",
    }

package = {
    "name": "wildberries-sdk",
    "version": version,
    "description": "Wildberries OpenAPI clients (generated).",
    "license": "MIT",
    "repository": {
        "type": "git",
        "url": "https://github.com/eslazarev/wildberries-sdk.git",
    },
    "main": "./dist/index.js",
    "types": "./dist/index.d.ts",
    "exports": exports,
    "files": [
        "dist",
        "README.md",
        "LICENSE",
    ],
    "scripts": {
        "build": "tsc -p tsconfig.json",
    },
    "devDependencies": {
        "typescript": "^4.0 || ^5.0",
    },
}

(root / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
PY
