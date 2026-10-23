"""End-to-end: generate the reference pages, then build the site strictly."""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest

from docsgen.extract import python_anchor
from docsgen.specs import load_operations

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "website" / "docs" / "reference"
UNAVAILABLE = "операция недоступна в этом клиенте"


@pytest.fixture(scope="module")
def generated():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build-docs-site.py")],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


def test_generator_reports_what_the_specs_hold(generated):
    ops = load_operations(str(ROOT / "specs"))
    modules = {op.module for op in ops}
    # Counts move with the upstream specs; the generator must agree with them,
    # which is the part a frozen number could never check.
    assert f"Generated {len(ops)} operations across {len(modules)} modules" in generated


def test_every_operation_got_a_page(generated):
    ops = load_operations(str(ROOT / "specs"))
    pages = {p for p in REFERENCE.rglob("*.md") if p.name != "index.md"}
    assert len(pages) == len(ops)


def test_python_examples_use_the_real_client_method(generated):
    """Regression: a fabricated method name is worse than an honest notice."""
    anchor = python_anchor("finances", str(ROOT / "clients"))
    balance = anchor[("GET", "/api/v1/account/balance")]
    page = (REFERENCE / "finances" / "get_api_v1_account_balance.md").read_text(encoding="utf-8")
    assert f"api.{balance}(" in page
    assert UNAVAILABLE not in page


def test_absent_operations_say_so_instead_of_guessing(generated):
    missing = int(re.search(r"\((\d+) without any client example\)", generated).group(1))
    pages_with_notice = [p for p in REFERENCE.rglob("*.md")
                         if UNAVAILABLE in p.read_text(encoding="utf-8")]
    if missing:
        assert pages_with_notice
    else:
        assert not pages_with_notice


@pytest.mark.skipif(importlib.util.find_spec("mkdocs") is None,
                    reason="mkdocs is not installed in this interpreter")
def test_site_builds_in_strict_mode(generated, tmp_path):
    build = subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict",
         "-f", str(ROOT / "website" / "mkdocs.yml"), "-d", str(tmp_path / "site")],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert build.returncode == 0, build.stdout + build.stderr
