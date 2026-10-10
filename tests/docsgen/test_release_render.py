import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

from docsgen.releases import Release, build_stats
from docsgen.release_render import (
    calendar_columns,
    format_days,
    month_labels,
    render_page,
    render_svg,
)

UTC = timezone.utc


def _r(version, *args):
    return Release(version=version, at=datetime(*args, tzinfo=UTC))


def _stats(releases, today=datetime(2026, 10, 8, tzinfo=UTC)):
    return build_stats(releases, today=today)


# --- calendar geometry -----------------------------------------------------

def test_calendar_columns_are_whole_weeks_of_seven():
    grid = calendar_columns(_stats([_r("v1", 2026, 6, 1)]))
    assert all(len(week) == 7 for week in grid)


def test_calendar_first_cell_is_the_window_start_monday():
    stats = _stats([_r("v1", 2026, 6, 1)])
    assert calendar_columns(stats)[0][0] == stats.window_start
    assert stats.window_start.weekday() == 0


def test_calendar_last_week_pads_past_today_with_none():
    today = datetime(2026, 10, 8, tzinfo=UTC)  # Thursday, weekday 3
    grid = calendar_columns(_stats([_r("v1", 2026, 6, 1)], today=today))
    last = grid[-1]
    assert last[3] == today.date()
    assert last[4] is None and last[5] is None and last[6] is None


def test_calendar_covers_every_day_in_the_window_exactly_once():
    stats = _stats([_r("v1", 2026, 6, 1)])
    days = [day for week in calendar_columns(stats) for day in week if day]
    assert days == sorted(days)
    assert len(days) == len(set(days))
    assert days[0] == stats.window_start
    assert days[-1] == stats.window_end


def test_calendar_places_a_release_on_its_own_weekday_row():
    # 2026-06-03 is a Wednesday -> row index 2
    stats = _stats([_r("v1", 2026, 6, 3)])
    hits = [
        (week_i, row_i)
        for week_i, week in enumerate(calendar_columns(stats))
        for row_i, day in enumerate(week)
        if day and day in stats.by_day
    ]
    assert len(hits) == 1
    assert hits[0][1] == 2


def test_month_labels_mark_the_column_where_each_month_starts():
    labels = month_labels(_stats([_r("v1", 2026, 6, 1)]))
    names = [name for _, name in labels]
    assert "июн" in names
    assert "окт" in names
    # Strictly increasing column indices, one label per month at most.
    columns = [col for col, _ in labels]
    assert columns == sorted(columns)
    assert len(columns) == len(set(columns))


# --- Russian day formatting ------------------------------------------------

def test_format_days_uses_genitive_singular_for_decimals():
    assert format_days(1.1) == "1,1 дня"


def test_format_days_plural_forms():
    assert format_days(1) == "1 день"
    assert format_days(2) == "2 дня"
    assert format_days(5) == "5 дней"
    assert format_days(11) == "11 дней"
    assert format_days(21) == "21 день"


def test_format_days_handles_none():
    assert format_days(None) == "—"


# --- page ------------------------------------------------------------------

def test_page_shows_the_kpi_values():
    stats = _stats([_r("v1", 2026, 6, 1), _r("v2", 2026, 6, 3), _r("v3", 2026, 10, 1)])
    page = render_page(stats)
    assert str(stats.total) in page
    assert format_days(stats.median_interval_days) in page
    assert format_days(stats.longest_gap_days) in page


def test_page_carries_tooltip_data_for_each_release_day():
    stats = _stats([_r("v1", 2026, 6, 1, 6, 6, 0)])
    page = render_page(stats)
    assert 'data-date="2026-06-01"' in page
    assert "v1" in page
    assert "06:06" in page


def test_page_groups_two_same_day_releases_into_one_cell():
    stats = _stats([_r("v1", 2026, 6, 1, 6, 0, 0), _r("v2", 2026, 6, 1, 18, 0, 0)])
    page = render_page(stats)
    assert page.count('data-date="2026-06-01"') == 1
    assert "v1" in page and "v2" in page


def test_page_lists_weekday_bars_with_counts():
    stats = _stats([_r("v1", 2026, 6, 1), _r("v2", 2026, 6, 3), _r("v3", 2026, 6, 3)])
    page = render_page(stats)
    assert "Релизы по дням недели" in page
    for label in ("пн", "вт", "ср", "чт", "пт", "сб", "вс"):
        assert f">{label}<" in page


def test_page_has_no_spec_versus_code_split():
    stats = _stats([_r("v1", 2026, 6, 1)])
    page = render_page(stats).lower()
    assert "спек" not in page.replace("спецификац", "")


def test_page_renders_without_releases():
    page = render_page(_stats([]))
    assert "0" in page
    assert "—" in page


# --- svg -------------------------------------------------------------------

def test_svg_is_well_formed_xml():
    svg = render_svg(_stats([_r("v1", 2026, 6, 1)]), theme="dark")
    root = ET.fromstring(svg)
    assert root.tag.endswith("svg")


def test_svg_declares_width_height_and_viewbox():
    root = ET.fromstring(render_svg(_stats([_r("v1", 2026, 6, 1)]), theme="dark"))
    assert root.get("viewBox")
    assert root.get("width") and root.get("height")


def test_svg_marks_every_release_day():
    releases = [_r("v1", 2026, 6, 1), _r("v2", 2026, 6, 3), _r("v3", 2026, 6, 3)]
    stats = _stats(releases)
    root = ET.fromstring(render_svg(stats, theme="dark"))
    marked = [el for el in root.iter() if el.get("class") == "on"]
    assert len(marked) == 2  # two distinct days, three releases


def test_svg_themes_use_different_backgrounds():
    stats = _stats([_r("v1", 2026, 6, 1)])
    dark = ET.fromstring(render_svg(stats, theme="dark"))
    light = ET.fromstring(render_svg(stats, theme="light"))

    def background(root):
        return next(el.get("fill") for el in root.iter() if el.get("class") == "bg")

    assert background(dark) != background(light)


def test_svg_carries_no_script():
    svg = render_svg(_stats([_r("v1", 2026, 6, 1)]), theme="dark")
    assert "<script" not in svg.lower()
    assert "onmouseover" not in svg.lower()


def test_svg_renders_without_releases():
    root = ET.fromstring(render_svg(_stats([]), theme="dark"))
    assert not [el for el in root.iter() if el.get("class") == "on"]


# --- tooltip attribute safety ----------------------------------------------

def test_tooltip_attribute_encodes_newlines():
    # A raw newline inside an attribute survives neither Markdown nor a
    # single-line HTML parse; it must be encoded.
    stats = _stats([_r("v1", 2026, 6, 1, 6, 6, 0)])
    page = render_page(stats)
    tips = re.findall(r'data-tip="([^"]*)"', page)
    assert tips
    assert all("\n" not in tip for tip in tips)
    assert "&#10;" in tips[0]


def test_page_emits_one_cell_per_release_day():
    releases = [
        _r("v1", 2026, 6, 1, 6, 0, 0),
        _r("v2", 2026, 6, 1, 18, 0, 0),
        _r("v3", 2026, 7, 4, 9, 0, 0),
    ]
    stats = _stats(releases)
    page = render_page(stats)
    assert page.count("data-date=") == len(stats.by_day) == 2


def test_every_release_cell_opens_and_closes_on_one_line():
    stats = _stats([_r("v1", 2026, 6, 1), _r("v2", 2026, 6, 3)])
    for line in render_page(stats).splitlines():
        if "wb-rc-on" in line and "data-date" in line:
            assert line.rstrip().endswith("></div>")
