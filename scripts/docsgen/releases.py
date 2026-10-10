"""Collect release cadence data from the repository's ``v*`` git tags.

One root tag marks one release. The per-module Go tags (``clients/go/<mod>/v*``)
mirror the same releases thirteen times over and are ignored here.
"""
from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from statistics import median
from typing import Dict, List, Optional, Sequence

UTC = timezone.utc

WINDOW_MONTHS = 12
RECENT_DAYS = 30

# ``%(creatordate)`` on a lightweight tag is the commit date, which is what we
# want: the moment the release was cut.
TAG_FORMAT = "%(refname:short)\t%(creatordate:iso-strict)"


@dataclass(frozen=True)
class Release:
    version: str
    at: datetime


@dataclass
class ReleaseStats:
    """Everything the chart renderers need, in display order."""

    releases: List[Release] = field(default_factory=list)
    window_start: Optional[date] = None
    window_end: Optional[date] = None
    total: int = 0
    last_30_days: int = 0
    median_interval_days: Optional[float] = None
    longest_gap_days: Optional[int] = None
    weekday_counts: List[int] = field(default_factory=lambda: [0] * 7)
    by_day: Dict[date, List[Release]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "releases": [
                {"version": r.version, "at": r.at.isoformat()} for r in self.releases
            ],
            "window_start": self.window_start.isoformat() if self.window_start else None,
            "window_end": self.window_end.isoformat() if self.window_end else None,
            "total": self.total,
            "last_30_days": self.last_30_days,
            "median_interval_days": self.median_interval_days,
            "longest_gap_days": self.longest_gap_days,
            "weekday_counts": list(self.weekday_counts),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ReleaseStats":
        releases = [
            Release(version=item["version"], at=_to_utc(datetime.fromisoformat(item["at"])))
            for item in data.get("releases", [])
        ]
        return cls(
            releases=releases,
            window_start=_opt_date(data.get("window_start")),
            window_end=_opt_date(data.get("window_end")),
            total=data.get("total", 0),
            last_30_days=data.get("last_30_days", 0),
            median_interval_days=data.get("median_interval_days"),
            longest_gap_days=data.get("longest_gap_days"),
            weekday_counts=list(data.get("weekday_counts", [0] * 7)),
            by_day=_group_by_day(releases),
        )


def _opt_date(value: Optional[str]) -> Optional[date]:
    return date.fromisoformat(value) if value else None


def _to_utc(moment: datetime) -> datetime:
    """Naive timestamps are read as UTC; aware ones are converted to it."""
    if moment.tzinfo is None:
        return moment.replace(tzinfo=UTC)
    return moment.astimezone(UTC)


def _group_by_day(releases: Sequence[Release]) -> Dict[date, List[Release]]:
    grouped: Dict[date, List[Release]] = {}
    for release in releases:
        grouped.setdefault(release.at.date(), []).append(release)
    return grouped


def parse_tag_lines(lines: Sequence[str]) -> List[Release]:
    """Turn ``<tag>\\t<iso date>`` lines into chronologically sorted releases."""
    releases = []
    for line in lines:
        if "\t" not in line:
            continue
        name, _, raw_date = line.partition("\t")
        name, raw_date = name.strip(), raw_date.strip()
        # Root release tags only: "clients/go/dbs/v0.1.13" is the same release.
        if "/" in name or not name.startswith("v"):
            continue
        # git prints "...Z"; fromisoformat only learned that spelling in 3.11.
        if raw_date.endswith("Z"):
            raw_date = raw_date[:-1] + "+00:00"
        try:
            moment = datetime.fromisoformat(raw_date)
        except ValueError:
            continue
        releases.append(Release(version=name, at=_to_utc(moment)))
    releases.sort(key=lambda r: (r.at, r.version))
    return releases


def read_tags(repo_root: str) -> List[Release]:
    """Read ``v*`` tags out of the git repository at ``repo_root``."""
    result = subprocess.run(
        ["git", "for-each-ref", f"--format={TAG_FORMAT}", "refs/tags/v*"],
        cwd=repo_root, capture_output=True, text=True, check=True,
    )
    return parse_tag_lines(result.stdout.splitlines())


def load_stats(data_file: str, repo_root: str) -> ReleaseStats:
    """Prefer the committed data file; fall back to reading git tags directly.

    CI commits ``data/releases.json`` when it cuts a release, which keeps the
    docs build independent of clone depth. Locally the file may be stale or
    missing, so git is the backstop, and an empty result is still renderable.
    """
    if os.path.isfile(data_file):
        with open(data_file, encoding="utf-8") as fh:
            return ReleaseStats.from_dict(json.load(fh))
    try:
        return build_stats(read_tags(repo_root))
    except (subprocess.CalledProcessError, OSError):
        return build_stats([])


def build_stats(releases: Sequence[Release], today: Optional[datetime] = None) -> ReleaseStats:
    """Reduce releases to the rolling 12-month window the chart draws."""
    now = _to_utc(today or datetime.now(UTC))
    end = now.date()
    # 12 months back, then rounded down to Monday so the calendar grid starts
    # on a full week column.
    cutoff = _months_back(end, WINDOW_MONTHS)
    start = cutoff - timedelta(days=cutoff.weekday())

    windowed = [r for r in releases if cutoff <= r.at.date() <= end]

    weekday_counts = [0] * 7
    for release in windowed:
        weekday_counts[release.at.weekday()] += 1

    recent_cutoff = now - timedelta(days=RECENT_DAYS)

    return ReleaseStats(
        releases=windowed,
        window_start=start,
        window_end=end,
        total=len(windowed),
        last_30_days=sum(1 for r in windowed if r.at > recent_cutoff),
        median_interval_days=_median_interval(windowed),
        longest_gap_days=_longest_gap(windowed),
        weekday_counts=weekday_counts,
        by_day=_group_by_day(windowed),
    )


def _months_back(day: date, months: int) -> date:
    year, month = day.year, day.month - months
    while month <= 0:
        month += 12
        year -= 1
    # Clamp for short months, e.g. 31 March minus 12 months is fine but
    # 29 February in a leap year is not.
    return date(year, month, min(day.day, _days_in_month(year, month)))


def _days_in_month(year: int, month: int) -> int:
    if month == 12:
        return 31
    return (date(year, month + 1, 1) - timedelta(days=1)).day


def _gaps_in_days(releases: Sequence[Release]) -> List[float]:
    return [
        (later.at - earlier.at).total_seconds() / 86400.0
        for earlier, later in zip(releases, releases[1:])
    ]


def _median_interval(releases: Sequence[Release]) -> Optional[float]:
    gaps = _gaps_in_days(releases)
    return round(median(gaps), 2) if gaps else None


def _longest_gap(releases: Sequence[Release]) -> Optional[int]:
    gaps = _gaps_in_days(releases)
    return round(max(gaps)) if gaps else None
