# Capture schemas — the four JSON files

Written by the agent (not by init_capture.py) as each flow completes, into the
engagement folder that `scripts/init_capture.py` created. Only written when
the user opted in to capture. Keep values honest: statuses use the audit
checklist vocabulary (`present`/`missing`/`limited`/`unknown`); never fill a
field with a guess.

Common fields on all files: `"engagement_id": "<folder name>"`, `"site"`,
`"date": "YYYY-MM-DD"`.

## intake.json — flow 1 (routing) + flow 2 (context intake)

```json
{
  "engagement_id": "example-com-2026-10-25",
  "site": "example.com",
  "date": "2026-10-25",
  "capture_opt_in": true,
  "routing": {
    "user_goal": "their words for what they wanted",
    "requested_flow": "audit+recommendations | qa | recommendations-only | declined",
    "fit": "fit | partial | declined",
    "decline_or_partial_reason": "why the skill is a bad fit, or what part is out of scope (omit when fit)",
    "fetch_capabilities": {
      "available": ["plain-get", "ollama-fetch", "lightpanda"],
      "missing": [],
      "user_choice": "all-available | proceed-as-is | enable-now | decide-later"
    }
  },
  "intake": {
    "role": "owner | building-for-client | other",
    "audience": "who the site serves",
    "offers": ["what they sell, with price points if known"],
    "sells_elsewhere": ["platforms/marketplaces they also sell on"],
    "email_list": "description of list status (size/tool) or 'none'",
    "goal_90_days": "the business goal for the next 90 days"
  }
}
```

## audit.json — flow 2 output

```json
{
  "engagement_id": "…", "site": "…", "date": "…",
  "fetch_report": [
    {"page": "https://…", "method": "plain-get | ollama-fetch | lightpanda | none",
     "status": "fetched | gone | unknown | refused", "note": "HTTP code / wall / timeout — never blank"}
  ],
  "collection_points": [
    {"name": "…", "type": "buy | free-capture | relationship",
     "page": "https://…", "evidence": "quote or element", "status": "present"}
  ],
  "collection_point_count": {"found": 3, "complete": false,
    "incomplete_because": "unread pages: /pricing (unknown)"},
  "three_question_test": {
    "buy_today": "answered or 'no path found' — with evidence",
    "free_path": "…",
    "next_offer": "…"
  },
  "layers": {
    "offer":        {"status": "present|missing|limited|unknown", "evidence": "…"},
    "copy":         {"status": "…", "evidence": "…"},
    "content":      {"status": "…", "evidence": "…"},
    "landing_pages": {"status": "…", "evidence": "…"},
    "funnel":        {"status": "…", "evidence": "…"}
  },
  "value_ladder": {"price_points_found": ["free", "$14", "…"], "gaps": "…"},
  "ai_discoverability": {"faq": "…", "public_answers": "…", "platform_signposts": "…"},
  "ownership": {"email_capture": "…", "checkout_location": "…", "notes": "owned vs rented"},
  "digital_home_score": {
    "score": 6.0,
    "band": "partial digital home",
    "provisional": false,
    "provisional_because": "named unread/limited evidence (omit when firm)",
    "breakdown": {
      "three_questions": {"points": 2, "detail": "buy-today + free path; no next offer"},
      "five_layers": {"points": 3.0, "detail": "offer, copy present; content, landing pages limited; funnel missing"},
      "reach_ownership": {"points": 1, "detail": "FAQ present; checkout on external marketplace"}
    }
  },
  "verdict": "digital brochure | partial digital home | digital home",
  "verdict_reason": "one paragraph",
  "gaps": [
    {"id": 1, "gap": "…", "severity": "critical|high|medium|low",
     "evidence": "page + quote/element", "evidence_status": "present|limited|unknown"}
  ]
}
```

## recommendations.json — flow 3 output

```json
{
  "engagement_id": "…", "site": "…", "date": "…",
  "basis": "audit.json",
  "evidence_flag": "firm | provisional",
  "provisional_because": "named unknown/limited evidence (omit when firm)",
  "start_here": "rank-1 title, or dependency-ordered override with the reason",
  "items": [
    {"rank": 1, "title": "…", "what": "…", "addresses_gap": 2,
     "principle": "collection points", "why": "…",
     "effort": 2, "cost": "<$50", "time": "S",
     "resources": ["…"], "dependencies": ["…"],
     "impact": 5, "priority": 3.0}
  ]
}
```

Shape of `items[]` matches `references/recommendation-rubric.md` exactly.

## qa-log.json — flow 4 (append-only)

```json
[
  {"ts": "2026-10-25T14:03:00", "question": "the user's question",
   "answer_summary": "2–3 sentences",
   "provenance": [{"claim": "…", "label": "video | general | not-covered"}],
   "site_context": "site this Q&A belongs to, if engagement-scoped"}
]
```

Append new entries to the array; never rewrite past entries.

## report.md

`init_capture.py` already copied the template with site/date filled. At the end
of the engagement, fill every section from the JSONs above — the report is the
human-readable mirror of the machine-readable captures, with the fetch
disclosure table copied in full.