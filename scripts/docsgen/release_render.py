"""Render the release cadence chart as a docs page and as static SVGs.

Both renderers read the same :class:`~docsgen.releases.ReleaseStats`, so the
interactive page on the site and the picture in the README never disagree.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Callable, List, Optional, Tuple

from .releases import ReleaseStats

@dataclass(frozen=True)
class Locale:
    """Every word the static chart prints, for one README language."""

    months: Tuple[str, ...]
    weekdays: Tuple[str, ...]
    kpis: Tuple[str, str, str, str]
    bars_title: str
    day_unit: Callable[[float], str]
    decimal_comma: bool = True


def _plural_day_ru(count: float) -> str:
    if count != int(count):
        return "дня"
    count = int(count)
    if count % 100 in (11, 12, 13, 14):
        return "дней"
    last = count % 10
    if last == 1:
        return "день"
    if last in (2, 3, 4):
        return "дня"
    return "дней"


def _plural_day_en(count: float) -> str:
    return "day" if count == 1 else "days"


LOCALES = {
    "ru": Locale(
        months=("янв", "фев", "мар", "апр", "май", "июн",
                "июл", "авг", "сен", "окт", "ноя", "дек"),
        weekdays=("пн", "вт", "ср", "чт", "пт", "сб", "вс"),
        kpis=("Релизов за год", "Медианный интервал",
              "Релизов за 30 дней", "Самая длинная пауза"),
        bars_title="Релизы по дням недели",
        day_unit=_plural_day_ru,
    ),
    "en": Locale(
        months=("Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"),
        weekdays=("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"),
        kpis=("Releases this year", "Median interval",
              "Releases in 30 days", "Longest pause"),
        bars_title="Releases by weekday",
        day_unit=_plural_day_en,
        decimal_comma=False,
    ),
    "zh-CN": Locale(
        months=("1月", "2月", "3月", "4月", "5月", "6月",
                "7月", "8月", "9月", "10月", "11月", "12月"),
        weekdays=("周一", "周二", "周三", "周四", "周五", "周六", "周日"),
        kpis=("年度发布", "发布间隔中位数", "30 天内发布", "最长间隔"),
        bars_title="按星期统计的发布",
        day_unit=lambda count: "天",
        decimal_comma=False,
    ),
    "tr": Locale(
        months=("Oca", "Şub", "Mar", "Nis", "May", "Haz",
                "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"),
        weekdays=("Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"),
        kpis=("Yıllık sürüm", "Medyan aralık",
              "Son 30 gündeki sürüm", "En uzun ara"),
        bars_title="Haftanın günlerine göre sürümler",
        day_unit=lambda count: "gün",
    ),
    "kk": Locale(
        months=("қаң", "ақп", "нау", "сәу", "мам", "мау",
                "шіл", "там", "қыр", "қаз", "қар", "жел"),
        weekdays=("дс", "сс", "ср", "бс", "жм", "сб", "жс"),
        kpis=("Жылдағы релиздер", "Медианалық аралық",
              "30 күндегі релиздер", "Ең ұзақ үзіліс"),
        bars_title="Апта күндері бойынша релиздер",
        day_unit=lambda count: "күн",
    ),
    "uz": Locale(
        months=("yan", "fev", "mar", "apr", "may", "iyn",
                "iyl", "avg", "sen", "okt", "noy", "dek"),
        weekdays=("du", "se", "cho", "pay", "jum", "sha", "yak"),
        kpis=("Yildagi relizlar", "Median oraliq",
              "30 kundagi relizlar", "Eng uzun tanaffus"),
        bars_title="Hafta kunlari boʻyicha relizlar",
        day_unit=lambda count: "kun",
    ),
}

# The docs site is Russian, and so is every helper that feeds it.
MONTHS = list(LOCALES["ru"].months)
WEEKDAYS = list(LOCALES["ru"].weekdays)

THEMES = {
    "dark": {
        "bg": "#0d1117", "grid": "#21262d", "on": "#2f81f7",
        "text": "#e6edf3", "muted": "#8b949e", "bar": "#2f81f7",
    },
    "light": {
        "bg": "#ffffff", "grid": "#ebedf0", "on": "#1f6feb",
        "text": "#1f2328", "muted": "#59636e", "bar": "#1f6feb",
    },
}


# --- shared helpers --------------------------------------------------------

def _esc(text: str) -> str:
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _attr(text: str) -> str:
    """Escape for an HTML attribute. A raw newline there survives neither
    Markdown nor a single-line parse, so encode it as a character reference."""
    return _esc(text).replace("\n", "&#10;")


def format_days(value: Optional[float], lang: str = "ru") -> str:
    """``1.1`` -> ``1,1 дня``; ``5`` -> ``5 дней``; ``None`` -> ``—``."""
    loc = LOCALES[lang]
    if value is None:
        return "—"
    if isinstance(value, float) and not value.is_integer():
        number = f"{value:.1f}"
        if loc.decimal_comma:
            number = number.replace(".", ",")
        return f"{number} {loc.day_unit(value)}"
    return f"{int(value)} {loc.day_unit(int(value))}"


def calendar_columns(stats: ReleaseStats) -> List[List[Optional[date]]]:
    """Weeks as columns of seven days, Monday first, padded with ``None``."""
    if not stats.window_start or not stats.window_end:
        return []
    weeks: List[List[Optional[date]]] = []
    day = stats.window_start
    while day <= stats.window_end:
        week: List[Optional[date]] = []
        for offset in range(7):
            current = day + timedelta(days=offset)
            week.append(current if current <= stats.window_end else None)
        weeks.append(week)
        day += timedelta(days=7)
    return weeks


def month_labels(stats: ReleaseStats, lang: str = "ru") -> List[Tuple[int, str]]:
    """``(column index, month name)`` for each column that opens a new month."""
    months = LOCALES[lang].months
    labels = []
    previous = None
    for index, week in enumerate(calendar_columns(stats)):
        first = next((day for day in week if day), None)
        if first and first.month != previous:
            labels.append((index, months[first.month - 1]))
            previous = first.month
    return labels


# A tooltip is about five cells wide either side of the cell it points at. The
# weekday labels leave the left edge a little slack, so it needs fewer columns.
TIP_LEFT_COLUMNS = 3
TIP_RIGHT_COLUMNS = 5
TIP_LINE_PX = 17
TIP_CHROME_PX = 24


def tooltip_anchor(column: int, total: int) -> str:
    """Which side of the cell the tooltip hangs from, so it stays in view."""
    if column < TIP_LEFT_COLUMNS:
        return "left"
    if column >= total - TIP_RIGHT_COLUMNS:
        return "right"
    return "center"


def tooltip_space(stats: ReleaseStats) -> int:
    """Height in px of the tallest tooltip, which the scroll box must clear."""
    lines = 1 + max((len(day) for day in stats.by_day.values()), default=0)
    return TIP_CHROME_PX + lines * TIP_LINE_PX


def _tooltip(stats: ReleaseStats, day: date) -> str:
    releases = stats.by_day.get(day, [])
    head = f"{day.day} {MONTHS[day.month - 1]}, {WEEKDAYS[day.weekday()]}"
    lines = [f"{r.version} · {r.at:%H:%M} UTC" for r in releases]
    return "\n".join([head] + lines)


# --- interactive page ------------------------------------------------------

PAGE_CSS = """
.wb-rc{--wb-rc-grid:#ebedf0;--wb-rc-on:#1f6feb;--wb-rc-muted:#59636e;
  --wb-rc-tip-bg:#1f2328;--wb-rc-tip-fg:#ffffff;--wb-rc-tip-space:58px;
  margin:1.2rem 0;}
[data-md-color-scheme="slate"] .wb-rc{--wb-rc-grid:#21262d;--wb-rc-on:#2f81f7;
  --wb-rc-muted:#8b949e;--wb-rc-tip-bg:#161b22;--wb-rc-tip-fg:#e6edf3;}
.wb-rc-kpis{display:flex;flex-wrap:wrap;gap:2.2rem;margin-bottom:1.6rem;}
.wb-rc-kpi-label{font-size:.72rem;color:var(--wb-rc-muted);margin-bottom:.25rem;}
.wb-rc-kpi-value{font-size:1.55rem;font-weight:700;line-height:1.1;}
.wb-rc-legend{display:flex;align-items:center;gap:.45rem;font-size:.72rem;
  color:var(--wb-rc-muted);margin-bottom:.9rem;}
.wb-rc-swatch{width:11px;height:11px;border-radius:2px;display:inline-block;}
/* The scroll box clips what leaves it, so it reserves the tooltip's height
   above the grid and takes the same amount back as margin. */
.wb-rc-scroll{overflow-x:auto;padding-bottom:.4rem;
  padding-top:var(--wb-rc-tip-space);
  margin-top:calc(-1 * var(--wb-rc-tip-space));}
.wb-rc-cal{display:inline-grid;grid-template-areas:"corner months" "days grid";
  gap:.3rem .45rem;}
/* 13px pitch: a full year of columns then fits the page width, so the latest
   week is hoverable without scrolling the calendar first. */
.wb-rc-months{grid-area:months;display:grid;grid-auto-flow:column;
  grid-auto-columns:13px;font-size:.68rem;color:var(--wb-rc-muted);}
.wb-rc-month{grid-row:1;white-space:nowrap;}
.wb-rc-days{grid-area:days;display:grid;grid-template-rows:repeat(7,13px);
  font-size:.68rem;color:var(--wb-rc-muted);line-height:13px;}
.wb-rc-grid{grid-area:grid;display:grid;grid-auto-flow:column;
  grid-template-rows:repeat(7,13px);grid-auto-columns:13px;}
.wb-rc-day{width:11px;height:11px;border-radius:2px;background:var(--wb-rc-grid);
  position:relative;}
.wb-rc-day.wb-rc-pad{background:none;}
.wb-rc-day.wb-rc-on{background:var(--wb-rc-on);cursor:pointer;}
.wb-rc-day.wb-rc-on:hover::after{content:attr(data-tip);white-space:pre;
  position:absolute;left:50%;bottom:calc(100% + 7px);transform:translateX(-50%);
  background:var(--wb-rc-tip-bg);color:var(--wb-rc-tip-fg);padding:.5rem .7rem;
  border-radius:6px;font-size:.72rem;line-height:1.45;z-index:5;
  box-shadow:0 2px 10px rgba(0,0,0,.35);pointer-events:none;}
.wb-rc-day.wb-rc-tip-l:hover::after{left:0;transform:none;}
.wb-rc-day.wb-rc-tip-r:hover::after{left:auto;right:0;transform:none;}
.wb-rc-bars{margin-top:1.8rem;display:grid;grid-template-columns:auto 1fr auto;
  gap:.35rem .7rem;align-items:center;max-width:620px;}
.wb-rc-bar-label{font-size:.75rem;color:var(--wb-rc-muted);}
.wb-rc-bar-track{height:11px;}
.wb-rc-bar-fill{height:11px;border-radius:2px;background:var(--wb-rc-on);
  min-width:2px;}
.wb-rc-bar-count{font-size:.75rem;font-variant-numeric:tabular-nums;}
"""


def render_page(stats: ReleaseStats) -> str:
    """The MkDocs page: KPI tiles, hoverable calendar and weekday bars."""
    period = ""
    if stats.window_start and stats.window_end:
        period = (f"С {stats.window_start.day} {MONTHS[stats.window_start.month - 1]} "
                  f"{stats.window_start.year} года.")

    kpis = [
        ("Релизов за год", str(stats.total)),
        ("Медианный интервал", format_days(stats.median_interval_days)),
        ("Релизов за 30 дней", str(stats.last_30_days)),
        ("Самая длинная пауза", format_days(stats.longest_gap_days)),
    ]

    out = [
        "# Частота релизов", "",
        "Каждый релиз SDK помечается тегом в репозитории. "
        "График строится по ним автоматически при каждой публикации. " + period, "",
        f"<style>{PAGE_CSS}</style>", "",
        '<div class="wb-rc" markdown="0">',
        '<div class="wb-rc-kpis">',
    ]
    for label, value in kpis:
        out.append(
            f'<div><div class="wb-rc-kpi-label">{_esc(label)}</div>'
            f'<div class="wb-rc-kpi-value">{_esc(value)}</div></div>'
        )
    out.append("</div>")

    out.append(
        '<div class="wb-rc-legend">'
        '<span class="wb-rc-swatch" style="background:var(--wb-rc-on)"></span>'
        f'<span>Релиз ({stats.total})</span>'
        '<span class="wb-rc-swatch" style="background:var(--wb-rc-grid);'
        'margin-left:.8rem"></span><span>Нет релиза</span></div>'
    )

    weeks = calendar_columns(stats)
    out.append(f'<div class="wb-rc-scroll" '
               f'style="--wb-rc-tip-space:{tooltip_space(stats)}px">'
               f'<div class="wb-rc-cal">')

    out.append('<div class="wb-rc-months">')
    for column, name in month_labels(stats):
        out.append(f'<div class="wb-rc-month" style="grid-column:{column + 1}">'
                   f'{_esc(name)}</div>')
    out.append("</div>")

    out.append('<div class="wb-rc-days">')
    for index, name in enumerate(WEEKDAYS):
        # Label every other row, as a full column of names is unreadable.
        out.append(f"<div>{_esc(name) if index % 2 == 0 else ''}</div>")
    out.append("</div>")

    out.append('<div class="wb-rc-grid">')
    anchors = {"left": " wb-rc-tip-l", "right": " wb-rc-tip-r", "center": ""}
    for column, week in enumerate(weeks):
        anchor = anchors[tooltip_anchor(column, len(weeks))]
        for day in week:
            if day is None:
                out.append('<div class="wb-rc-day wb-rc-pad"></div>')
            elif day in stats.by_day:
                out.append(f'<div class="wb-rc-day wb-rc-on{anchor}" '
                           f'data-date="{day.isoformat()}" '
                           f'data-tip="{_attr(_tooltip(stats, day))}"></div>')
            else:
                out.append('<div class="wb-rc-day"></div>')
    out.append("</div></div></div>")

    out.append('<div class="wb-rc-bars-title" style="margin-top:1.6rem;'
               'font-weight:600">Релизы по дням недели</div>')
    out.append('<div class="wb-rc-bars">')
    peak = max(stats.weekday_counts) or 1
    for index, name in enumerate(WEEKDAYS):
        count = stats.weekday_counts[index]
        width = round(count / peak * 100, 1)
        out.append(
            f'<div class="wb-rc-bar-label">{_esc(name)}</div>'
            f'<div class="wb-rc-bar-track"><div class="wb-rc-bar-fill" '
            f'style="width:{width}%"></div></div>'
            f'<div class="wb-rc-bar-count">{count}</div>'
        )
    out.append("</div>")
    out.append("</div>")
    return "\n".join(out) + "\n"


# --- static SVG ------------------------------------------------------------

CELL = 11
STEP = 14
PAD = 20
LABEL_W = 26


def render_svg(stats: ReleaseStats, theme: str = "dark", lang: str = "ru") -> str:
    """A self-contained picture of the same chart, for a README in ``lang``."""
    colors = THEMES[theme]
    loc = LOCALES[lang]
    weeks = calendar_columns(stats)

    grid_x = PAD + LABEL_W
    kpi_y = PAD + 16
    months_y = kpi_y + 54
    grid_y = months_y + 10
    bars_title_y = grid_y + 7 * STEP + 34
    bars_y = bars_title_y + 16

    width = max(grid_x + max(len(weeks), 1) * STEP + PAD, 560)
    height = bars_y + 7 * 18 + PAD

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="-apple-system,BlinkMacSystemFont,'
        f'Segoe UI,Helvetica,Arial,sans-serif">',
        f'<rect class="bg" width="{width}" height="{height}" fill="{colors["bg"]}"/>',
    ]

    kpis = list(zip(loc.kpis, [
        str(stats.total),
        format_days(stats.median_interval_days, lang),
        str(stats.last_30_days),
        format_days(stats.longest_gap_days, lang),
    ]))
    for index, (label, value) in enumerate(kpis):
        x = PAD + index * ((width - 2 * PAD) / 4)
        parts.append(f'<text x="{x:.0f}" y="{kpi_y}" fill="{colors["muted"]}" '
                     f'font-size="11">{_esc(label)}</text>')
        parts.append(f'<text x="{x:.0f}" y="{kpi_y + 26}" fill="{colors["text"]}" '
                     f'font-size="21" font-weight="700">{_esc(value)}</text>')

    for column, name in month_labels(stats, lang):
        parts.append(f'<text x="{grid_x + column * STEP}" y="{months_y}" '
                     f'fill="{colors["muted"]}" font-size="10">{_esc(name)}</text>')

    for row in range(0, 7, 2):
        parts.append(f'<text x="{PAD}" y="{grid_y + row * STEP + 9}" '
                     f'fill="{colors["muted"]}" font-size="10">{loc.weekdays[row]}</text>')

    for week_index, week in enumerate(weeks):
        for row, day in enumerate(week):
            if day is None:
                continue
            on = day in stats.by_day
            parts.append(
                f'<rect class="{"on" if on else "off"}" '
                f'x="{grid_x + week_index * STEP}" y="{grid_y + row * STEP}" '
                f'width="{CELL}" height="{CELL}" rx="2" '
                f'fill="{colors["on"] if on else colors["grid"]}"/>'
            )

    parts.append(f'<text x="{PAD}" y="{bars_title_y}" fill="{colors["text"]}" '
                 f'font-size="12" font-weight="600">{_esc(loc.bars_title)}</text>')
    peak = max(stats.weekday_counts) or 1
    track = width - PAD - LABEL_W - 60
    for index, name in enumerate(loc.weekdays):
        count = stats.weekday_counts[index]
        y = bars_y + index * 18
        parts.append(f'<text x="{PAD}" y="{y + 9}" fill="{colors["muted"]}" '
                     f'font-size="10">{name}</text>')
        parts.append(f'<rect x="{PAD + LABEL_W}" y="{y}" '
                     f'width="{max(count / peak * track, 2):.1f}" height="{CELL}" '
                     f'rx="2" fill="{colors["bar"]}"/>')
        parts.append(f'<text x="{width - PAD}" y="{y + 9}" fill="{colors["text"]}" '
                     f'font-size="10" text-anchor="end">{count}</text>')

    parts.append("</svg>")
    return "\n".join(parts) + "\n"
