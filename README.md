# Digital Home Auditor

Agent skill that audits a website as a digital home, not a digital brochure.
It counts collection points, checks the five layers (offer, copy, content,
landing pages, funnels), computes a 0-10 Digital Home Score, and ranks
monetization fixes by effort, cost, time, resources, and dependencies. It
grills your intent first, gathers evidence before judging, and declines
out-of-scope work honestly.

The framework comes from one source: Brave Brand's video "Websites Are Dead.
Build THIS Instead" (the collection-point model). Every figure in chat carries
a provenance label; every claim traces to a bundled reference file. The final
report is written for readers with no context, so it never name-drops the
framework.

## How it works

1. **Route** (always first). Up to 4 questions: outcome, site URL, your role,
   capture opt-in. Misfits (SEO, accessibility, security, code review) get an
   honest scope statement and the nearest covered alternative, never
   improvised advice.
2. **Gather.** Homepage first, then money-relevant pages (max 10, two levels
   deep), each down a fetch ladder: plain download, smart fetch, real-browser
   render, pasted content last. Unread pages stay `unknown`, never `missing`.
3. **Audit.** Checklist sections A to I (collection points, five layers,
   value ladder, AI-era discoverability, owned reach) ending in a mechanical
   Digital Home Score (0-10) with a verdict band.
4. **Recommend.** 3 to 8 ranked fixes from the numbered gaps, each citing its
   gap and principle, scored on effort, cost, time, resources, dependencies.
   The "start here" pick comes from the formula, not vibes.
5. **Close.** Capture on: one engagement folder plus `report.md`. Capture
   off: chat only, filesystem untouched.

## Example

> **You:** audit my site, https://example.com
>
> **Assistant:** Quick routing: audit, fix list, or a question? Do you own
> the site, and should I save this to `./digital-home-audits/example-com-2026-11-01/`?
>
> **You:** Audit, I own it, no files.
>
> **Assistant:** Downloads work on your host. [Pages: 8 read; 1 blocked
> (paste offered); 1 empty.] **Score: 4/10, partial digital home.** No email
> capture path anywhere, so visits stay visits...

## Skill folder

```text
digital-home-auditor/
├── SKILL.md                      # operational spec: routing, steps, bounds
├── scripts/
│   ├── check_capabilities.py    # tell which page-reading rungs work here
│   ├── fetch_page.py            # fetch a page through the ladder, JSON status
│   └── init_capture.py          # scaffold the engagement folder
├── references/
│   ├── knowledge-base.md        # the framework, definitions, cited statistics
│   ├── audit-checklist.md       # sections A to I and the score computation
│   ├── recommendation-rubric.md # effort/cost/time/resources/dependencies math
│   ├── capture-schemas.md       # JSON shapes for the engagement folder
│   └── report-writing-rules.md  # evidence over adjectives, plain words
└── assets/
    └── report-template.md       # report.md skeleton, filled at close
```

## Output

With capture on, one folder per engagement lands in your working directory:

```text
digital-home-audits/example-com-2026-11-01/
├── intake.json           # routing answers and context intake
├── audit.json            # checklist findings, score, collection points
├── recommendations.json  # ranked fixes with priority math
├── qa-log.json           # Q&A exchanges, when they happen
├── pages/                # captured page content, one file per page
└── report.md             # the reader-ready deliverable
```

The deliverable is `report.md`; the rest is traceable evidence behind it.

## Setup

```bash
ln -s ~/repos/digital-home-auditor ~/.pi/agent/skills/digital-home-auditor   # global
ln -s ~/repos/digital-home-auditor <project>/.pi/skills/digital-home-auditor # or project-local
```

Then start with "audit my site <url>" or a strategy question ("do I need a
value ladder?"). Rung 1 of the fetch ladder needs no API keys; see docs/usage.md.

## Scope

Monetization and conversion structure only. Out of scope: technical SEO,
accessibility, performance, security audits, code review, and site
implementation. The skill offers the nearest covered flow instead.

## Docs

- [docs/usage.md](docs/usage.md): walkthrough, fetch ladder, capture schemas
- [docs/design.md](docs/design.md): design decisions, provenance, bounds