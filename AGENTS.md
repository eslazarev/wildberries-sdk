# AGENTS.md

Notes for coding agents working in this repository. Humans: see [README.md](README.md).

## What this repo is

Five SDK clients — Python, Node.js, Go, PHP, Rust — for the Wildberries
marketplace API. They are **generated** from the OpenAPI specs in `specs/` by
openapi-generator and republished whenever Wildberries changes a spec, which
happens a few times a week.

## The one rule that matters

**Never hand-edit anything under `clients/`.** Every file there is regenerated
on the next spec change and your edit disappears without a trace. A bug in a
client is a bug in one of these, in order of likelihood:

1. `specs/*.yaml` — the upstream contract (fix upstream, or patch in `generation.yaml`)
2. `generation.yaml` — generator settings, per-language options, template overrides
3. `scripts/generate-clients.sh` — the generation pipeline itself

`generation.yaml` points template overrides at `tools/templates/`, which is not
checked in: the generator falls back to its built-in Mustache templates. Create
the directory only if you really mean to override them.

## Generated vs hand-written

| Generated — do not edit | Written by hand |
| --- | --- |
| `clients/**` | `specs/**` (downloaded, see below) |
| `docs/*/README.md` **between** `<!-- *_METHODS_LIST_START/END -->` | the rest of `docs/*/README.md` |
| `website/docs/reference/**`, `SUMMARY.md`, `releases.md`, `llms.txt`, `llms-full.txt` | `website/docs/index.md`, `getting-started.md` |
| `.github/images/release-cadence-*.svg`, `data/releases.json` | `README.md`, `docs/i18n/README.*.md`, root `llms.txt` |
| `CHANGELOG.md` | `scripts/**`, `tests/**` |

Generated files under `website/docs/` are gitignored and rebuilt in CI; the rest
are committed so the README renders on GitHub and the registries.

## Commands

```bash
python -m pytest                                  # tests (conftest.py puts scripts/ on sys.path)
python scripts/build-docs-site.py                 # generate reference pages + llms.txt + llms-full.txt
mkdocs build --strict -f website/mkdocs.yml       # build the site (pip install -r website/requirements.txt)
python scripts/generate-release-chart.py          # 12 release-cadence SVGs + data/releases.json
bash scripts/generate-python-methods-list.sh      # refresh one README's method list (same for npm/go/php/rust)
```

The suite is green on a clean tree — a failure is your change, not background
noise. It stays that way because no test spells out an operation count or a
generated method name: both are read from `specs/` and from the clients at run
time. Write new tests the same way, or they will rot at the next spec update.

## What you cannot run locally

- **Downloading specs.** `scripts/download-specs-from-config.sh` pulls only from
  an S3 mirror and needs `S3_URL`. Wildberries' anti-bot blocks direct and
  headless fetching, so there is no "just curl the spec" path.
- **Generating clients** without Docker. `scripts/generate-clients.sh` runs
  openapi-generator from a pinned Docker image (`OPENAPI_GENERATOR_DOCKER=1`),
  not from a locally installed generator — a different local version produces a
  different diff across thousands of files.

## Pipelines

- `update-specs.yml` — nightly spec download; writes the `CHANGELOG.md` entry
  from an LLM summary of the diff and opens a PR when something changed.
- `generate-clients.yml` — on push to `main`: regenerate clients, bump version,
  update method lists, commit, tag, publish to PyPI, npm, Packagist and
  crates.io, cut a GitHub Release, refresh the release chart.
- `deploy-docs.yml` — builds and deploys the MkDocs site to GitHub Pages.

Jobs are guarded by `if: github.actor != 'github-actions[bot]'` so the bot's own
commits do not retrigger them. Keep that guard in mind when adding steps that commit.

## Writing docs in this repo

- The docs site is Russian. README exists in six languages: `README.md` plus
  `docs/i18n/README.{en,zh-CN,tr,kk,uz}.md` — change all of them together.
- The release-cadence chart has one SVG per language and theme; regenerate with
  the script above rather than editing the XML.
- Do not describe how API tokens are supplied or stored. The SDK does not manage
  the token source — it passes through whatever the caller provides.
