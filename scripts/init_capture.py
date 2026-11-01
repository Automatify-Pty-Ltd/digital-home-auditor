#!/usr/bin/env python3
"""Create the capture folder for one digital-home-audit engagement.

Usage:
    python3 init_capture.py <site> [--root <dir>] [--date YYYY-MM-DD]

Creates <root>/<slug>-<date>/ containing report.md (copied from the skill's
assets/report-template.md). The four capture JSONs (intake.json, audit.json,
recommendations.json, qa-log.json) are written by the agent as each flow
completes, per references/capture-schemas.md.

Prints JSON {"path", "site", "date", "files", "to_write"} on success.
"""

import json
import os
import re
import sys
from datetime import date

TEMPLATE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "assets", "report-template.md"
)


def slugify(site):
    """example.com -> 'example-com'; strips protocol, www and path."""
    s = re.sub(r"^https?://", "", str(site).strip().lower())
    s = s.split("/")[0]
    s = re.sub(r"^www\.", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "site"


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        print("usage: init_capture.py <site> [--root <dir>] [--date YYYY-MM-DD]", file=sys.stderr)
        print("error: no site given — pass the site domain as the first argument", file=sys.stderr)
        return 1
    site = args[0]
    root = "./digital-home-audits"
    day = date.today().isoformat()
    for i, a in enumerate(args[1:], 1):
        if a == "--root" and i + 1 < len(args):
            root = args[i + 1]
        elif a == "--date" and i + 1 < len(args):
            day = args[i + 1]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
        print(f"error: --date must be YYYY-MM-DD, got '{day}'", file=sys.stderr)
        return 1

    if not os.path.exists(TEMPLATE):
        print(
            f"error: report template not found at {TEMPLATE} — the skill install is "
            f"incomplete; reinstall the skill so assets/report-template.md exists",
            file=sys.stderr,
        )
        return 1

    slug = slugify(site)
    base = os.path.join(root, f"{slug}-{day}")
    path, n = base, 1
    while os.path.exists(path):
        n += 1
        path = f"{base}-{n}"

    os.makedirs(path, exist_ok=True)
    with open(TEMPLATE, encoding="utf-8") as f:
        report = f.read()
    with open(os.path.join(path, "report.md"), "w", encoding="utf-8") as f:
        f.write(report.replace("{{SITE}}", slug).replace("{{DATE}}", day))

    print(json.dumps({
        "path": path,
        "site": slug,
        "date": day,
        "files": ["report.md"],
        "to_write": ["intake.json", "audit.json", "recommendations.json", "qa-log.json"],
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())