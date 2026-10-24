"""DeepWiki rejects a malformed `.devin/wiki.json` outright.

There is no partial failure and no fallback: without a usable `pages` array
DeepWiki does not fall back to its own planning, it refuses the file. The only
signal is a wiki that silently keeps its old, unsteered shape, so the limits
are worth asserting here rather than discovering on the next re-index.
"""
import json
from pathlib import Path

import pytest

MANIFEST = Path(__file__).resolve().parent.parent / ".devin" / "wiki.json"

MAX_PAGES = 30          # 80 on enterprise plans; stay inside the lower bound
MAX_NOTES = 100         # repo_notes plus every page_notes entry
MAX_NOTE_CHARS = 10_000


@pytest.fixture(scope="module")
def wiki():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _notes(wiki):
    yield from wiki["repo_notes"]
    for page in wiki["pages"]:
        yield from page.get("page_notes", [])


def test_both_required_keys_are_present(wiki):
    # repo_notes may be empty, pages may not.
    assert isinstance(wiki["repo_notes"], list)
    assert wiki["pages"], "a wiki.json without pages is rejected, not ignored"


def test_page_count_stays_within_the_limit(wiki):
    assert len(wiki["pages"]) <= MAX_PAGES


def test_every_page_has_a_unique_non_empty_title_and_a_purpose(wiki):
    titles = [page["title"] for page in wiki["pages"]]
    assert all(title.strip() for title in titles)
    assert len(titles) == len(set(titles)), "titles are the page identity"
    assert all(page["purpose"].strip() for page in wiki["pages"])


def test_every_parent_names_a_page_that_exists(wiki):
    titles = {page["title"] for page in wiki["pages"]}
    for page in wiki["pages"]:
        parent = page.get("parent")
        if parent is not None:
            assert parent in titles, f"{page['title']} hangs off a missing {parent!r}"


def test_no_page_is_its_own_parent(wiki):
    for page in wiki["pages"]:
        assert page.get("parent") != page["title"]


def test_notes_stay_within_their_budget(wiki):
    notes = list(_notes(wiki))
    assert len(notes) <= MAX_NOTES
    for note in notes:
        assert note["content"].strip()
        assert len(note["content"]) <= MAX_NOTE_CHARS


def test_the_wiki_is_told_not_to_document_generated_clients(wiki):
    """The whole point of steering this repo's wiki: clients/ is machine output."""
    notes = " ".join(note["content"] for note in _notes(wiki))
    assert "clients/" in notes
