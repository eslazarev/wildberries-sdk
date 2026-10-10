from datetime import datetime, timedelta, timezone

import pytest

from docsgen.releases import Release, ReleaseStats, build_stats, parse_tag_lines

UTC = timezone.utc


def _r(version, *args):
    return Release(version=version, at=datetime(*args, tzinfo=UTC))


# --- parse_tag_lines -------------------------------------------------------

def test_parse_tag_lines_reads_name_and_date():
    lines = [
        "v0.1.13\t2026-01-02T13:33:33+00:00",
        "v0.1.14\t2026-01-02T16:15:53+00:00",
    ]
    releases = parse_tag_lines(lines)
    assert [r.version for r in releases] == ["v0.1.13", "v0.1.14"]
    assert releases[0].at == datetime(2026, 1, 2, 13, 33, 33, tzinfo=UTC)


def test_parse_tag_lines_accepts_the_z_suffix_git_emits():
    # git's iso-strict prints "Z", which fromisoformat rejects before 3.11.
    releases = parse_tag_lines(["v0.1.100\t2026-06-03T07:18:49Z"])
    assert releases[0].at == datetime(2026, 6, 3, 7, 18, 49, tzinfo=UTC)


def test_parse_tag_lines_normalises_to_utc():
    releases = parse_tag_lines(["v1.0.0\t2026-01-02T16:00:00+03:00"])
    assert releases[0].at == datetime(2026, 1, 2, 13, 0, 0, tzinfo=UTC)


def test_parse_tag_lines_sorts_chronologically():
    lines = [
        "v0.1.20\t2026-03-01T00:00:00+00:00",
        "v0.1.10\t2026-01-01T00:00:00+00:00",
    ]
    assert [r.version for r in parse_tag_lines(lines)] == ["v0.1.10", "v0.1.20"]


def test_parse_tag_lines_skips_go_module_tags():
    lines = [
        "v0.1.13\t2026-01-02T13:33:33+00:00",
        "clients/go/dbs/v0.1.13\t2026-01-02T13:33:33+00:00",
    ]
    assert [r.version for r in parse_tag_lines(lines)] == ["v0.1.13"]


def test_parse_tag_lines_skips_blank_and_malformed():
    lines = ["", "   ", "v0.1.13\t2026-01-02T13:33:33+00:00", "garbage-without-date"]
    assert [r.version for r in parse_tag_lines(lines)] == ["v0.1.13"]


# --- window ----------------------------------------------------------------

def test_window_keeps_last_12_months_only():
    today = datetime(2026, 10, 8, tzinfo=UTC)
    releases = [
        _r("v0.0.1", 2025, 9, 1),    # 13 months back, dropped
        _r("v0.0.2", 2025, 10, 9),   # just inside
        _r("v0.0.3", 2026, 10, 8),
    ]
    stats = build_stats(releases, today=today)
    assert [r.version for r in stats.releases] == ["v0.0.2", "v0.0.3"]


def test_window_start_is_first_day_of_the_week():
    today = datetime(2026, 10, 8, tzinfo=UTC)  # Thursday
    stats = build_stats([_r("v1", 2026, 10, 8)], today=today)
    assert stats.window_start.weekday() == 0


def test_window_end_is_today():
    today = datetime(2026, 10, 8, tzinfo=UTC)
    stats = build_stats([_r("v1", 2026, 10, 8)], today=today)
    assert stats.window_end == today.date()


# --- totals ----------------------------------------------------------------

def test_total_counts_only_windowed_releases():
    today = datetime(2026, 10, 8, tzinfo=UTC)
    releases = [_r("v0", 2024, 1, 1), _r("v1", 2026, 5, 1), _r("v2", 2026, 6, 1)]
    assert build_stats(releases, today=today).total == 2


def test_last_30_days_counts_releases_in_trailing_month():
    today = datetime(2026, 10, 8, tzinfo=UTC)
    releases = [
        _r("v1", 2026, 8, 1),    # outside
        _r("v2", 2026, 9, 20),   # inside
        _r("v3", 2026, 10, 8),   # inside
    ]
    assert build_stats(releases, today=today).last_30_days == 2


# --- median interval -------------------------------------------------------

def test_median_interval_odd_number_of_gaps():
    today = datetime(2026, 10, 8, tzinfo=UTC)
    # gaps of 1, 2 and 10 days -> median 2
    releases = [
        _r("v1", 2026, 6, 1), _r("v2", 2026, 6, 2),
        _r("v3", 2026, 6, 4), _r("v4", 2026, 6, 14),
    ]
    assert build_stats(releases, today=today).median_interval_days == pytest.approx(2.0)


def test_median_interval_even_number_of_gaps_averages_middle_pair():
    today = datetime(2026, 10, 8, tzinfo=UTC)
    # gaps of 1, 2, 4 and 8 days -> median (2+4)/2 = 3
    releases = [
        _r("v1", 2026, 6, 1), _r("v2", 2026, 6, 2), _r("v3", 2026, 6, 4),
        _r("v4", 2026, 6, 8), _r("v5", 2026, 6, 16),
    ]
    assert build_stats(releases, today=today).median_interval_days == pytest.approx(3.0)


def test_median_interval_is_none_for_a_single_release():
    today = datetime(2026, 10, 8, tzinfo=UTC)
    assert build_stats([_r("v1", 2026, 6, 1)], today=today).median_interval_days is None


def test_median_interval_uses_timestamps_not_calendar_days():
    today = datetime(2026, 10, 8, tzinfo=UTC)
    releases = [_r("v1", 2026, 6, 1, 0, 0, 0), _r("v2", 2026, 6, 1, 12, 0, 0)]
    assert build_stats(releases, today=today).median_interval_days == pytest.approx(0.5)


# --- longest gap -----------------------------------------------------------

def test_longest_gap_is_the_widest_span_between_releases():
    today = datetime(2026, 10, 8, tzinfo=UTC)
    releases = [_r("v1", 2026, 6, 1), _r("v2", 2026, 6, 8), _r("v3", 2026, 6, 10)]
    assert build_stats(releases, today=today).longest_gap_days == 7


def test_longest_gap_is_none_for_a_single_release():
    today = datetime(2026, 10, 8, tzinfo=UTC)
    assert build_stats([_r("v1", 2026, 6, 1)], today=today).longest_gap_days is None


# --- weekday histogram -----------------------------------------------------

def test_weekday_counts_are_monday_first_and_always_seven_long():
    today = datetime(2026, 10, 8, tzinfo=UTC)
    # 2026-06-01 is a Monday; 2026-06-03 a Wednesday
    releases = [_r("v1", 2026, 6, 1), _r("v2", 2026, 6, 3), _r("v3", 2026, 6, 3)]
    counts = build_stats(releases, today=today).weekday_counts
    assert counts == [1, 0, 2, 0, 0, 0, 0]


# --- per-day grouping ------------------------------------------------------

def test_by_day_groups_same_day_releases_together():
    today = datetime(2026, 10, 8, tzinfo=UTC)
    releases = [
        _r("v1", 2026, 6, 1, 6, 0, 0),
        _r("v2", 2026, 6, 1, 18, 0, 0),
        _r("v3", 2026, 6, 2, 9, 0, 0),
    ]
    by_day = build_stats(releases, today=today).by_day
    assert [r.version for r in by_day[_r("x", 2026, 6, 1).at.date()]] == ["v1", "v2"]
    assert len(by_day[_r("x", 2026, 6, 2).at.date()]) == 1


# --- empty input -----------------------------------------------------------

def test_build_stats_tolerates_no_releases():
    today = datetime(2026, 10, 8, tzinfo=UTC)
    stats = build_stats([], today=today)
    assert stats.total == 0
    assert stats.median_interval_days is None
    assert stats.longest_gap_days is None
    assert stats.weekday_counts == [0] * 7
    assert stats.by_day == {}


# --- serialisation ---------------------------------------------------------

def test_stats_round_trip_through_json():
    today = datetime(2026, 10, 8, tzinfo=UTC)
    releases = [_r("v1", 2026, 6, 1, 6, 6, 0), _r("v2", 2026, 6, 3, 4, 0, 0)]
    stats = build_stats(releases, today=today)
    restored = ReleaseStats.from_dict(stats.to_dict())
    assert restored.total == stats.total
    assert restored.window_start == stats.window_start
    assert restored.window_end == stats.window_end
    assert restored.weekday_counts == stats.weekday_counts
    assert restored.median_interval_days == stats.median_interval_days
    assert restored.longest_gap_days == stats.longest_gap_days
    assert restored.by_day == stats.by_day


def test_to_dict_is_json_serialisable_and_stable():
    import json

    today = datetime(2026, 10, 8, tzinfo=UTC)
    stats = build_stats([_r("v1", 2026, 6, 1)], today=today)
    once = json.dumps(stats.to_dict(), sort_keys=True)
    twice = json.dumps(ReleaseStats.from_dict(stats.to_dict()).to_dict(), sort_keys=True)
    assert once == twice


# --- load_stats ------------------------------------------------------------

def test_load_stats_prefers_the_data_file(tmp_path):
    import json

    from docsgen.releases import load_stats

    data_file = tmp_path / "releases.json"
    stats = build_stats([_r("v9", 2026, 6, 1)], today=datetime(2026, 10, 8, tzinfo=UTC))
    data_file.write_text(json.dumps(stats.to_dict()), encoding="utf-8")

    loaded = load_stats(str(data_file), repo_root=str(tmp_path))
    assert [r.version for r in loaded.releases] == ["v9"]


def test_load_stats_falls_back_to_git_tags(tmp_path):
    from docsgen.releases import load_stats

    # tmp_path is not a git repo, and there is no data file either.
    loaded = load_stats(str(tmp_path / "missing.json"), repo_root=str(tmp_path))
    assert loaded.total == 0
    assert loaded.weekday_counts == [0] * 7


def test_load_stats_reads_real_tags_when_data_file_is_absent():
    import os

    from docsgen.releases import load_stats

    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    loaded = load_stats(os.path.join(root, "does-not-exist.json"), repo_root=root)
    assert loaded.total > 0
