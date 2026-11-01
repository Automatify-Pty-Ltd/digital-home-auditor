# Usage

How a digital-home-audit engagement runs end to end.

## The three flows

| You want | The skill does | Needs |
|----------|---------------|-------|
| An audit ("review my site") | Route, gather, checklist audit, score | A site URL |
| A fix list ("what should I fix") | Ranked recommendations from existing audit evidence | A prior audit in this engagement; otherwise it offers the audit first |
| An answer ("do I need a value ladder?") | Q&A from the knowledge base with provenance labels | Nothing |

Routing happens first, in at most 2 rounds of clarifying questions. If intent
stays ambiguous after that, the skill picks the best fit, states the
assumption in one line, and proceeds. Requests the skill cannot cover honestly
(technical SEO, accessibility, performance, security, code review, "build the
site") get a plain scope statement and the nearest covered flow. The skill
never improvises out-of-scope advice.

## Fetch ladder

Each page descends the ladder; the first rung that reads the page wins.

| Rung | Method | Reads | Needs | Timeout |
|------|--------|-------|-------|---------|
| 1 | plain download with browser-like user agents | static HTML pages | nothing | 15s |
| 2 | Ollama Cloud web fetch | pages that block simple downloads | Ollama Cloud key | 20s |
| 3 | Lightpanda render | JavaScript-built pages (the fix for SPA sites) | local Lightpanda | 25s |

`fetch_page.py` prints JSON and exits 0 (fetched), 1 (page gone, a 404/410
the ladder trusts), or 2 (unreadable: bot wall, block, timeout, refused
private host).

At engagement start the skill runs `check_capabilities.py` and tells you in
plain words which methods are available. If rung 2 or 3 is missing, you can
proceed as-is, enable it now with step-by-step guidance, or decide later
(the skill reminds you at the first unreadable page). Bot walls do not fool a
404 verdict: "unknown" is never recorded as "missing".

## Intake (at most 5 questions)

Before the audit, the skill asks: who the site serves, what is sold (with
price points), where else you sell, email list status, and your goal for the
next 90 days. Answering takes two minutes and separates a scored audit from
a guess.

## Capture mode

When you opt in, the skill scaffolds
`./digital-home-audits/<site-slug>-<YYYY-MM-DD>/` in your current working
directory (never inside the skill folder) and fills it as the engagement
progresses:

- `intake.json`: routing answers and the five context answers
- `audit.json`: checklist findings, Digital Home Score, collection points
- `recommendations.json`: ranked fixes with priority math
- `qa-log.json`: appended Q&A exchanges
- `pages/`: captured page content, one file per page
- `report.md`: filled at close. Written for readers with no context, so it
  never mentions the video or the framework by name

You can decline capture mid-flow; the skill stops writing files immediately
and continues chat-only. Schemas: `references/capture-schemas.md`.

## Example dialogues

Resume after a break:

> **You:** where were we with the audit?
>
> **Assistant:** Capture folder intact, `audit.json` complete, score 4/10,
> provisional: two pages unread. Recommendations are next; I can rank fixes
> now, or you paste the blocked page and I firm up the score first.

Q&A routing:

> **You:** do I need a value ladder?
>
> **Assistant:** Provenance first: [video] the ladder concept and its layers
> are covered; [general] sequencing advice beyond the source is labeled as
> such. Want me to audit your site so the answer reflects your setup rather
> than the general case?