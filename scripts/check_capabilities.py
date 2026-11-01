#!/usr/bin/env python3
"""Report which fetch-ladder rungs are available on this machine.

Usage:
    python3 check_capabilities.py

Prints JSON with per-rung availability, where each capability was found, a
non-technical how-to-enable line for missing rungs, and what the current
combination means for website audits. The agent announces this at the start
of an engagement (SKILL.md Step 1) and offers the user a choice.

Exit codes:
    0  all rungs available
    1  some optional rungs missing (see JSON)
"""

import json
import os
import shutil
import sys

CONFIG_PATH = os.path.expanduser("~/.pi/agent/ollama_cloud.json")

HOW_TO_ENABLE_OLLAMA = (
    "Connect your agent to Ollama Cloud: run /ollama-setup in pi and sign in "
    "(or paste your Ollama Cloud API key there). pi stores the key in its own "
    "config and this skill picks it up automatically — no separate setup. "
    "Technical alternative: export OLLAMA_API_KEY in the shell profile pi is "
    "started from."
)
HOW_TO_ENABLE_LIGHTPANDA = (
    "Install the Lightpanda browser: on macOS run "
    "`brew install lightpanda-io/browser/lightpanda` in a terminal. It lets "
    "the skill open pages the way a real browser does — the fix for pages "
    "that look empty because JavaScript builds them."
)


def ollama_rung():
    """Rung 2: Ollama Cloud fetch. Key from env or pi's config file."""
    if os.environ.get("OLLAMA_API_KEY"):
        return {"available": True, "source": "env OLLAMA_API_KEY", "how_to_enable": None}
    try:
        cfg = json.load(open(CONFIG_PATH))
        if str(cfg.get("account", {}).get("apiKey", "")):
            return {"available": True, "source": CONFIG_PATH, "how_to_enable": None}
    except (OSError, ValueError):
        pass
    return {"available": False, "source": None, "how_to_enable": HOW_TO_ENABLE_OLLAMA}


def lightpanda_rung():
    """Rung 3: local Lightpanda render. Needs the binary on PATH."""
    path = shutil.which("lightpanda")
    if path:
        return {"available": True, "source": path, "how_to_enable": None}
    return {"available": False, "source": None, "how_to_enable": HOW_TO_ENABLE_LIGHTPANDA}


# (ollama, lightpanda) -> what the combination means for audits
MEANINGS = {
    (True, True): (
        "Full ladder. Nearly any public page can be read — pages that block "
        "simple downloads, and pages built by JavaScript."
    ),
    (True, False): (
        "Strong. Pages that block simple downloads can usually be read through "
        "Ollama's fetch service. Pages built by JavaScript may come back empty "
        "— installing Lightpanda would close that gap."
    ),
    (False, True): (
        "Strong. Pages built by JavaScript can be opened in a local browser. "
        "Pages that actively block automated access may be unreadable — "
        "connecting Ollama Cloud (/ollama-setup) would close that gap."
    ),
    (False, False): (
        "Basic. Only simple public pages can be read. Pages that block "
        "automated access or build themselves with JavaScript may be "
        "unreadable — the audit will say so and ask for pasted content instead."
    ),
}


def main():
    ollama = ollama_rung()
    lightpanda = lightpanda_rung()
    rungs = {
        "plain-get": {"available": True, "source": "built-in",
                      "how_to_enable": None,
                      "note": "always available; needs only internet"},
        "ollama-fetch": ollama,
        "lightpanda": lightpanda,
    }
    all_available = all(r["available"] for r in rungs.values())
    print(json.dumps({
        "rungs": rungs,
        "meaning_for_audits": MEANINGS[(ollama["available"], lightpanda["available"])],
        "typical_issues": [
            {"issue": "page blocks simple downloads ('verify you are human' wall)",
             "resolved_by": "ollama-fetch, then lightpanda"},
            {"issue": "page reads empty because JavaScript builds it",
             "resolved_by": "lightpanda (renders like a real browser)"},
        ],
    }))
    return 0 if all_available else 1


if __name__ == "__main__":
    sys.exit(main())