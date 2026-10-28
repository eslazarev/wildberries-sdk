#!/usr/bin/env python3
"""Announce new CHANGELOG entries in the Telegram channel.

Finds the ``### Changed (YYYY.MM.DD)`` entries that a push added to
CHANGELOG.md, asks OpenAI to turn each one into a channel post, and sends it.
The model writes only the body and the hashtags: the date header and the links
are added here, so the anchor and the repository link are always right.

A post the model gets wrong — no key, an API error, tags Telegram does not
accept, too long — falls back to a plain rendering of the entry, and so does a
post Telegram rejects. A missing entry is never invented: nothing new, no post.

  python scripts/changelog_post.py --since <sha> [--dry-run]

Environment: TELEGRAM_BOT, TELEGRAM_CHAT_ID, OPENAI_API_KEY, OPENAI_MODEL.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docsgen.changelog import (  # noqa: E402
    CHANGELOG_URL, REPO_URL, Entry, human_date, inline_markdown,
    parse_entries, sections,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")

# Telegram caps a message at 4096 characters; leave room for header and footer.
MAX_MESSAGE = 4096
MAX_BODY = 3400


# What Telegram's HTML parse mode accepts, minus links: the model writes none.
ALLOWED_TAGS = {"b", "strong", "i", "em", "u", "s", "code", "pre", "blockquote"}

EXAMPLE_BODY = """\
🧪 <b>Песочницы больше нет в трёх API</b>
Sandbox-хосты убраны из <code>servers</code> у Статистики, Продвижения и Поставок FBW. Если тесты ходят туда — пора переключать.

<blockquote expandable><b>Какие хосты и методы</b>
• <code>statistics-api-sandbox</code> — <code>GET /api/v1/supplier/orders</code>, <code>/sales</code>
• <code>advert-api-sandbox</code> — 14 методов <code>/adv/…</code>: budget, start, pause, stop и др.
• <code>supplies-api-sandbox</code> — <code>POST /api/v1/acceptance/options</code>, <code>GET /api/v1/warehouses</code>
Заодно из описаний ушли лимиты песочницы и тестовый баланс.</blockquote>

⏱ <b>Новые лимиты: отчёт по возвратам продавцу</b>
• 1 запрос/мин, burst 10 — Персональный, Сервисный, Базовый с секретом
• 2 запроса/час, burst 1 — Базовый"""

PROMPT = """\
Ты ведёшь Telegram-канал об изменениях API маркетплейса Wildberries для разработчиков.
Ниже — запись из CHANGELOG за один день. Напиши по ней пост.

Правила:
- Только факты из записи. Ничего не додумывай: ни методов, ни цифр, ни причин.
- Главное — что изменилось и что это значит для того, кто пишет интеграцию.
- 1–4 блока, самые важные изменения первыми; мелкие правки объедини в один блок.
- Новое (методы, поля, лимиты) и сломанное (удалённое, переименованное) — каждое
  своим блоком, и суть видна без раскрытия цитаты.
- Блок: эмодзи, <b>заголовок</b>, одна-две короткие фразы. Перечни методов,
  полей и хостов — внутри <blockquote expandable>…</blockquote>; два-три коротких
  пункта можно оставить списком с «• ».
- Пути, поля, хосты и коды — в <code>.
- Разметка — Telegram HTML: только b, i, u, s, code, pre, blockquote. Без ссылок,
  без markdown, без заголовка с датой и без подписи — их добавят отдельно.
- Символы <, > и & вне тегов экранируй: &lt; &gt; &amp;.
- Не длиннее 2500 символов.
- Хэштеги: 3–6 слов в нижнем регистре, без «#», по разделам и сути изменений.

Образец тела поста (стиль, не содержание):
{example}

Ответь JSON-объектом: {{"body": "<тело поста>", "hashtags": ["...", "..."]}}

Запись за {date}:
{entry}
"""


def new_entries(before: str, after: str) -> list[Entry]:
    """Entries present after the push and absent before it, oldest first."""
    known = {e.heading for e in parse_entries(before)}
    fresh = [e for e in parse_entries(after) if e.heading not in known]
    return sorted(fresh, key=lambda e: e.date)


class _TagCheck(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.stack: list[str] = []
        self.ok = True

    def handle_starttag(self, tag, attrs):
        if tag not in ALLOWED_TAGS:
            self.ok = False
        if any(name != "expandable" for name, _ in attrs):
            self.ok = False
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack.pop() != tag:
            self.ok = False


def valid_body(body: str) -> bool:
    """True when Telegram will parse the body: known tags, balanced, short."""
    if not body.strip() or len(body) > MAX_BODY:
        return False
    if re.search(r"&(?!(?:amp|lt|gt|quot|#\d+|#x[0-9a-fA-F]+);)", body):
        return False
    check = _TagCheck()
    check.feed(body)
    check.close()
    return check.ok and not check.stack


def clean_hashtags(tags) -> list[str]:
    result: list[str] = []
    for tag in tags if isinstance(tags, list) else []:
        word = re.sub(r"[^\w]", "", str(tag).lstrip("#").lower())
        if word and word not in result:
            result.append(word)
    return result[:6]


def fallback_body(entry: Entry) -> str:
    """The entry itself, grouped by API section, when the model is not usable."""
    blocks: list[str] = []
    for section, items in sections(entry).items():
        lines = [f"• {inline_markdown(item)}" for item in items]
        blocks.append(f"🔹 <b>{html.escape(section)}</b>\n"
                      f"<blockquote expandable>{chr(10).join(lines)}</blockquote>")

    body = ""
    for i, block in enumerate(blocks):
        candidate = f"{body}\n\n{block}" if body else block
        if len(candidate) > MAX_BODY:
            body += f"\n\n…и ещё разделов: {len(blocks) - i}"
            break
        body = candidate
    return body


def ask_openai(entry: Entry, api_key: str, model: str) -> tuple[str, list[str]] | None:
    prompt = PROMPT.format(example=EXAMPLE_BODY, date=human_date(entry.date),
                           entry=entry.text)
    request = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "response_format": {"type": "json_object"},
        }).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            content = json.load(response)["choices"][0]["message"]["content"]
        data = json.loads(content)
    except (urllib.error.URLError, KeyError, IndexError, ValueError, TimeoutError) as exc:
        print(f"OpenAI failed: {exc}", file=sys.stderr)
        return None
    body = str(data.get("body", "")).strip()
    if not valid_body(body):
        print("OpenAI post rejected: bad markup or too long", file=sys.stderr)
        return None
    return body, clean_hashtags(data.get("hashtags"))


def compose(entry: Entry, body: str, hashtags: list[str]) -> str:
    parts = [
        f"📡 <b>WB API · {human_date(entry.date)}</b>",
        body,
        f'🔗 <a href="{CHANGELOG_URL}#{entry.anchor}">Все изменения за день</a>\n'
        f'🧰 <a href="{REPO_URL}">wildberries-sdk</a> — Python · Node.js · Go · PHP · Rust',
    ]
    if hashtags:
        parts.append(" ".join(f"#{tag}" for tag in hashtags))
    return "\n\n".join(parts)


def send(token: str, chat_id: str, text: str) -> tuple[bool, str]:
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=json.dumps({
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "link_preview_options": {"is_disabled": True},
        }).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            json.load(response)
        return True, ""
    except urllib.error.HTTPError as exc:
        return False, json.load(exc).get("description", str(exc.code))
    except urllib.error.URLError as exc:
        return False, str(exc.reason)


def changelog_at(ref: str) -> str | None:
    result = subprocess.run(["git", "show", f"{ref}:CHANGELOG.md"], cwd=ROOT,
                            capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--since", required=True,
                        help="commit before the push (github.event.before)")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the posts instead of sending them")
    args = parser.parse_args()

    before = changelog_at(args.since)
    if before is None:
        # A new branch or a force push: no base to diff against, and posting
        # the whole history would flood the channel.
        print(f"No CHANGELOG.md at {args.since}; nothing to announce.")
        return 0
    with open(CHANGELOG, encoding="utf-8") as fh:
        after = fh.read()

    entries = new_entries(before, after)
    if not entries:
        print("No new CHANGELOG entries.")
        return 0

    token = os.environ.get("TELEGRAM_BOT", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not args.dry_run and not (token and chat_id):
        print("TELEGRAM_BOT or TELEGRAM_CHAT_ID not set; skipping.", file=sys.stderr)
        return 0
    api_key = os.environ.get("OPENAI_API_KEY", "")
    model = os.environ.get("OPENAI_MODEL") or "gpt-4o-mini"

    failed = 0
    for entry in entries:
        written = ask_openai(entry, api_key, model) if api_key else None
        body, hashtags = written or (fallback_body(entry), [])
        text = compose(entry, body, hashtags)
        if len(text) > MAX_MESSAGE:
            text = compose(entry, fallback_body(entry), hashtags)

        if args.dry_run:
            print(f"--- {entry.heading} ({len(text)} chars)\n{text}\n")
            continue
        ok, error = send(token, chat_id, text)
        if not ok and written is not None:
            print(f"Telegram rejected the post ({error}); sending the plain one.",
                  file=sys.stderr)
            ok, error = send(token, chat_id, compose(entry, fallback_body(entry), hashtags))
        if ok:
            print(f"Posted {entry.heading}.")
        else:
            print(f"Failed to post {entry.heading}: {error}", file=sys.stderr)
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
