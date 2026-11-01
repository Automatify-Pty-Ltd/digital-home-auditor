#!/usr/bin/env python3
"""Fetch one public web page through a fallback ladder, honestly.

Rung 1: plain GET with browser-like User-Agents (free, no key needed).
Rung 2: Ollama Cloud web_fetch API (key from env OLLAMA_API_KEY or
        ~/.pi/agent/ollama_cloud.json).
Rung 3: local Lightpanda render (lightpanda fetch --dump markdown).

The first rung that reads the page wins. A 404/410 from a rung that really
reached the origin is a verdict ("gone"). A bot wall is not a verdict — it
wears any status, so the next rung takes over. If every rung fails, the
status is "unknown", which is not the same as gone.

Usage:
    python3 fetch_page.py <url> [--max-chars 12000] [--save <path>]

Exit codes:
    0  fetched  — content retrieved; JSON status on stdout
    1  gone     — origin answered 404/410
    2  unknown  — no rung could read the page (reasons in attempts[])
"""

import ipaddress
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import urllib.parse
import urllib.request

WALL = re.compile(
    r"challenges\.cloudflare|just a moment|attention required|verify you are human", re.I
)
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (docpull/2.0)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
]
TIME_LINES = re.compile(r"^\$time=.*$", re.M)

CONFIG_PATH = os.path.expanduser("~/.pi/agent/ollama_cloud.json")


def strip_html(html):
    """HTML to readable text: drop scripts/styles/tags, keep words, cap length."""
    text = re.sub(r"<(script|style|noscript|svg)[\s\S]*?</\1>", " ", str(html or ""), flags=re.I)
    text = re.sub(r"<!--[\s\S]*?-->", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = (
        text.replace("&amp;", "&")
        .replace("&#x27;", "'")
        .replace("&quot;", '"')
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&nbsp;", " ")
    )
    return re.sub(r"\s+", " ", text).strip()


def is_public_url(url):
    """True only for http(s) URLs whose host resolves to public network space.

    Refuses loopback, link-local, private, CGNAT, unspecified, multicast and
    reserved addresses, so the audit ladder never points at internal hosts.
    Unresolvable hosts count as private (refused).
    """
    try:
        parts = urllib.parse.urlsplit(url)
        if parts.scheme not in ("http", "https") or not parts.hostname:
            return False
        infos = socket.getaddrinfo(parts.hostname, None)
    except Exception:
        return False
    for info in infos:
        try:
            ip = ipaddress.ip_address(info[4][0])
        except ValueError:
            return False
        if not ip.is_global:
            return False
    return True


def plain_get(url, attempt):
    """Rung 1: free plain GET. Two UAs, 15s timeout. Bot walls pass the torch."""
    for ua in USER_AGENTS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "text/html"})
            with urllib.request.urlopen(req, timeout=15) as r:
                body = r.read().decode("utf-8", "replace")
                if WALL.search(body):
                    attempt.append({"rung": "plain-get", "outcome": "bot-wall", "http_status": r.status})
                    continue
                attempt.append({"rung": "plain-get", "outcome": "read", "http_status": r.status})
                return {"ok": True, "method": "plain-get", "http_status": r.status, "content": strip_html(body)}
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                attempt.append({"rung": "plain-get", "outcome": "gone", "http_status": e.code})
                return {"ok": False, "gone": True, "http_status": e.code}
            attempt.append({"rung": "plain-get", "outcome": "blocked", "http_status": e.code})
            continue
        except Exception as e:
            attempt.append({"rung": "plain-get", "outcome": "error", "detail": str(e)[:120]})
            continue
    return None


def ollama_config():
    """Ollama Cloud endpoint + key: env first, then the pi config file."""
    key = os.environ.get("OLLAMA_API_KEY", "")
    base, path = "https://ollama.com", "/api/web_fetch"
    if os.path.exists(CONFIG_PATH):
        try:
            cfg = json.load(open(CONFIG_PATH))
            key = key or str(cfg.get("account", {}).get("apiKey", ""))
            base = str(cfg.get("baseUrl", base)).rstrip("/") or base
            path = str(cfg.get("webFetchPath", path))
        except Exception:
            pass
    return (base + path, key) if key else (None, None)


def ollama_fetch(url, attempt):
    """Rung 2: Ollama Cloud web_fetch. Skips itself when no key is configured."""
    endpoint, key = ollama_config()
    if not endpoint:
        attempt.append({"rung": "ollama-fetch", "outcome": "skipped", "detail": "no API key configured"})
        return None
    try:
        req = urllib.request.Request(
            endpoint,
            data=json.dumps({"url": url}).encode(),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            content = str(json.loads(r.read().decode("utf-8", "replace") or "{}").get("content", "")).strip()
            if WALL.search(content):
                attempt.append({"rung": "ollama-fetch", "outcome": "bot-wall"})
                return None
            if len(content) > 40:
                attempt.append({"rung": "ollama-fetch", "outcome": "read"})
                return {"ok": True, "method": "ollama-fetch", "http_status": r.status, "content": content}
            attempt.append({"rung": "ollama-fetch", "outcome": "empty", "http_status": r.status})
            return {"ok": False, "http_status": r.status}
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            attempt.append({"rung": "ollama-fetch", "outcome": "gone", "http_status": e.code})
            return {"ok": False, "gone": True, "http_status": e.code}
        attempt.append({"rung": "ollama-fetch", "outcome": "blocked", "http_status": e.code})
    except Exception as e:
        attempt.append({"rung": "ollama-fetch", "outcome": "error", "detail": str(e)[:120]})
    return None


def lightpanda_fetch(url, attempt):
    """Rung 3: local Lightpanda render. Skips itself when not installed."""
    if not shutil.which("lightpanda"):
        attempt.append({"rung": "lightpanda", "outcome": "skipped", "detail": "lightpanda not installed"})
        return None
    try:
        r = subprocess.run(
            ["lightpanda", "fetch", "--dump", "markdown", "--log-level", "error", url],
            capture_output=True, text=True, timeout=25,
        )
        content = TIME_LINES.sub("", r.stdout or "").strip()
        if WALL.search(content):
            attempt.append({"rung": "lightpanda", "outcome": "bot-wall"})
            return None
        if content:
            attempt.append({"rung": "lightpanda", "outcome": "read"})
            return {"ok": True, "method": "lightpanda", "http_status": None, "content": content}
        attempt.append({"rung": "lightpanda", "outcome": "empty", "detail": (r.stderr or "")[:120]})
    except Exception as e:
        attempt.append({"rung": "lightpanda", "outcome": "error", "detail": str(e)[:120]})
    return None


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        print("usage: fetch_page.py <url> [--max-chars N] [--save PATH]", file=sys.stderr)
        print("error: no URL given — pass the page URL as the first argument", file=sys.stderr)
        return 2
    url = args[0]
    max_chars = 12000
    save_path = None
    for i, a in enumerate(args[1:], 1):
        if a == "--max-chars" and i + 1 < len(args):
            max_chars = int(args[i + 1])
        elif a == "--save" and i + 1 < len(args):
            save_path = args[i + 1]

    if not is_public_url(url):
        result = {"ok": False, "gone": False, "url": url,
                  "reason": "refused: URL is not http(s) or resolves to a private/unresolvable host",
                  "attempts": []}
        print(json.dumps(result))
        print("error: refused non-public host — pass a public website URL", file=sys.stderr)
        return 2

    attempts = []
    saw_gone = False
    result = None
    for rung in (plain_get, ollama_fetch, lightpanda_fetch):
        r = rung(url, attempts)
        if r is None:
            continue
        if r.get("ok"):
            result = r
            break
        if r.get("gone"):
            saw_gone = True

    if result:
        content = result.pop("content")
        # The origin answered 404/410 earlier in the ladder AND the rendered
        # page itself reads as a not-found page: the honest verdict is gone.
        # (A page that 404s for curl but renders real content still counts as fetched.)
        if saw_gone and re.search(r"(?i)\b404\b|\b410\b|not found|page (does not|doesn't|could not|couldn't) (be )?(exist|found)", content[:2000]):
            print(json.dumps({"ok": False, "gone": True, "url": url,
                              "reason": "origin answered 404/410 and the rendered content is a not-found page",
                              "attempts": attempts}))
            print("gone: origin answered 404/410 and the content confirms a not-found page", file=sys.stderr)
            return 1
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(content)
            result["saved_to"] = save_path
        result["url"] = url
        result["content"] = content[:max_chars]
        result["ok"] = True
        print(json.dumps(result))
        return 0
    if saw_gone:
        print(json.dumps({"ok": False, "gone": True, "url": url,
                          "reason": "origin answered 404/410 — page not there",
                          "attempts": attempts}))
        print("gone: the origin answered 404/410 — the page is not there", file=sys.stderr)
        return 1
    print(json.dumps({"ok": False, "gone": False, "url": url,
                      "reason": "unknown: no rung could read the page (bot wall, block or timeout) — this is not a verdict",
                      "attempts": attempts}))
    print("error: unknown — every rung failed; see attempts in the JSON status", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())