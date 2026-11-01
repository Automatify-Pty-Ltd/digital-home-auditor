---
name: digital-home-auditor
description: Audit a website as a digital home using the collection-point framework distilled from Brave Brand's video 'Websites Are Dead. Build THIS Instead'. Use when the user wants to assess whether a website is a digital brochure or a digital home, count collection points, check the five layers (offer, copy, content, landing pages, funnels), get ranked monetization and conversion recommendations scored by effort, cost, time, resources, and dependencies, or ask questions about value ladders, lead magnets, and AI-era brand discovery. The skill grills the user's intent first and routes to audit, recommendations, or Q&A. Don't use for technical SEO, accessibility, performance, or security audits, code review, or non-website topics.
---

# Digital Home Auditor

Turns a website into evidence: digital brochure or digital home, how many
collection points it has, and what to fix first. Framework and statistics come
from one source — read `references/knowledge-base.md` when answering questions.
In chat, present every figure as "as cited in the video", never as
independently verified. report.md is different: it reaches readers with no
context, so it never mentions the video or the framework by name
(`references/report-writing-rules.md`, rules 8-9).

Scripts run from this skill directory; capture files are always written to the
**user's current working directory**, never into the skill directory.

## Step 1: Route the request (always first)

1. Identify the outcome the user wants. When intent, site, or role is unclear,
   ask via `ask_user` — batch at most 4 questions covering: the outcome
   (audit / recommendations / a question), the site URL, their role (owner /
   building for a client), and the capture opt-in ("Save this engagement's
   inputs/outputs to ./digital-home-audits/<site>-<date>/?").
2. Route by the decision tree:
   - **Audit / "review my site" / "why doesn't my site sell"** → Step 2.
   - **"What should I fix" / recommendations** → requires a prior audit from
     this engagement (`audit.json` exists or findings are in context). If none,
     say recommendations need evidence, and offer the audit. Offer generic-only
     recommendations only if the user insists — and label them generic.
   - **A question about strategy** (value ladders, funnels, lead magnets,
     AI-era discovery, "websites dead?") → Step 5.
   - **Misfit** — technical SEO audits, accessibility/performance/security
     audits, code review, "build me the site" implementation work, non-website
     topics → decline honestly: state that this skill audits monetization and
     conversion structure only, name what it does cover, offer the nearest
     covered flow (e.g. "I can audit the money side, not the SEO side"), and
     wait. Do not improvise out-of-scope advice.
   - **Partial fit** — say exactly which part is covered and which is not;
     proceed on the covered part only after the user confirms.
3. Bound the routing: at most 2 rounds of clarifying questions. If intent is
   still ambiguous, pick the best-fit flow, state the assumption in one line,
   and proceed.
4. On capture opt-in, scaffold the engagement folder now: from the user's
   working directory, run
   `python3 <skill-dir>/scripts/init_capture.py <site-or-topic>` (the folder
   `./digital-home-audits/<slug>-<date>/` is created relative to the user's
   cwd; for Q&A-only engagements pass a short topic name as the site).
5. Announce fetch capability and offer a choice (once per engagement):
   a. Run `python3 <skill-dir>/scripts/check_capabilities.py` and read the
      JSON. Announce in plain words which page-reading methods are available
      and what that means for the audit (`meaning_for_audits`). Do not name
      API keys or config files — describe methods, not plumbing.
   b. When an optional rung is missing, explain in non-technical words what
      it does — rung 2 (Ollama fetch): reads pages that block simple
      downloads; rung 3 (Lightpanda): opens pages like a real browser, the
      fix for JavaScript-built pages — then offer the user the choice:
      - **proceed as-is** — fine for simple sites; when a page cannot be
        read, the skill asks for pasted content anyway (Step 2, item 4);
      - **enable it now** — guide the user through the rung's
        `how_to_enable` text step by step, then re-run
        check_capabilities.py to confirm the rung is live;
      - **decide later** — continue; on the first unreadable page, remind
        the user of this choice.
   c. Follow the user's choice. Do not re-announce capability later in the
      engagement unless the user asks or a fetch failure makes it relevant.
   d. If capture is on, record the outcome in intake.json under
      `fetch_capabilities` (available rungs + the user's choice), per
      `references/capture-schemas.md`.

## Step 2: Gather evidence (hybrid browse + intake)

1. Require a site URL. If absent after asking, do not proceed to audit —
   offer Step 5 (Q&A) instead.
2. Build the page list: homepage first, then from its navigation pick the
   pages that matter to money: about, services/offers, pricing, product or
   checkout, contact/booking, blog/content, FAQ, any landing pages. Bounds:
   at most 10 pages, at most 2 levels deep. Fewer is fine.
3. For each page, run the fallback ladder:
   `python3 <skill-dir>/scripts/fetch_page.py <url>`
   Add `--save <engagement-folder>/pages/<n>-<name>.md` when capture is on.
   Read the JSON status: exit 0 = fetched (`method` tells the rung), exit 1 =
   gone, exit 2 = unknown (bot wall / block / timeout / refused private host).
4. Record every page in a fetch report (page, method, status, reason).
   **Disclose failures to the user as they happen**: page, exact reason, and
   one of the recovery options — paste the content, describe the page, or
   confirm skipping. When a rung that could have read the page was reported
   missing at Step 1, remind the user of the enable option (Step 1, item 5b)
   before falling back to pasted content. "Unknown" is never a verdict:
   never mark an unread page as missing; audit the rest and name what is
   unread.
5. When the ladder read at least the homepage, run the context intake — at
   most 5 questions via `ask_user`: who the site serves, what is sold (with
   price points), where else they sell, email list status, and the goal for
   the next 90 days.
6. If capture is on, write `intake.json` into the engagement folder per
   `references/capture-schemas.md` (routing answers + context intake).

## Step 3: Audit the site

1. Read `references/audit-checklist.md`.
2. Work sections A→I in order. Every finding carries evidence (page + quote or
   element) and a status from the checklist vocabulary (`present`, `missing`,
   `limited`, `unknown`).
3. Produce the audit result: compute the **Digital Home Score** per section I
   of the checklist (mechanical sum — three test questions 0–3, five layers
   0–5, reach & ownership 0–2) and lead with it everywhere the audit appears
   (chat, report, JSON): number, band, collection-point count. Then the full
   audit — inventory, layers, value ladder, AI-discoverability, ownership,
   verdict (the score's band), numbered gaps. If capture is on, write
   `audit.json` per `references/capture-schemas.md`; otherwise present the
   full audit in chat.

## Step 4: Produce ranked recommendations

1. Read `references/recommendation-rubric.md`.
2. Generate 3–8 recommendations from the numbered gaps. Score each on effort,
   cost, time, resources, and dependencies; compute priority with the rubric
   formula; rank; name the "start here" pick. Follow the rubric's honesty
   rules — every recommendation cites its gap and its knowledge-base
   principle; provisional flag whenever evidence was `unknown` or `limited`.
3. If capture is on, write `recommendations.json` per
   `references/capture-schemas.md`.

## Step 5: Answer questions (Q&A)

1. Read `references/knowledge-base.md`.
2. Answer with provenance labels on every claim: `[video]` (as cited in the
   video), `[general]` (beyond the video), `[not covered]` (the video says
   nothing about it — say so plainly instead of guessing).
3. If the question is really about a specific site, offer the audit (Step 2).
4. If capture is on, append the exchange to `qa-log.json` per
   `references/capture-schemas.md`.

## Step 6: Close the engagement

1. If capture is on: fill every section of `<engagement-folder>/report.md`
   from the JSONs — including the full what-was-read table and the sources
   section — then give the user the folder path.
2. If capture is off: present the audit and recommendations in chat only, and
   leave the filesystem untouched.

## Writing rules (all user-facing text)

Audit presentations, recommendations, Q&A answers, and report.md follow
`references/report-writing-rules.md` — read it once before the first
user-facing output of the engagement and apply it throughout. The short
version: evidence over adjectives, plain words, facts and numbers, no
chatbot closers, no em dashes.

## Error Handling

- **`fetch_page.py` exit 2 on every page** (or no readable content): disclose,
  mention the Step 1 capability choice — enabling the missing rung may
  unlock the pages (re-run check_capabilities.py after enabling) — then
  offer an intake-only audit built from the user's answers and pasted
  content; mark every such finding `limited`, never `missing`.
- **JS-only site**: plain-get returns near-empty text but the lightpanda rung
  reads it — use the lightpanda content and say which rung won.
- **Login/paywall**: audit the public pages only and state the reduced scope.
- **No URL, no pasted content**: do not fabricate an audit; stay in Q&A.
- **User declines capture mid-flow**: stop writing files immediately; the
  conversation continues chat-only.
- **Out-of-scope request mid-flow**: apply the Step 1 misfit rules — honest
  scope statement, nearest covered alternative, no improvised out-of-scope
  advice.
- **Script errors**: both scripts print actionable messages on stderr — read
  them and follow the fix; do not retry more than twice per page.

## Bounds

At most 10 pages per audit (2 levels deep); at most 4 routing questions and 2
routing rounds; at most 5 intake questions; 3–8 recommendations; fetch rung
timeouts are built into the script (15s / 20s / 25s).