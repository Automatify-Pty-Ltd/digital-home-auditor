# Design

Why the skill is built the way it is.

## Design decisions

- **Evidence beats vibes.** Every finding carries a page plus a quote or
  element, and a status from a fixed vocabulary (`present`, `missing`,
  `limited`, `unknown`). Unread pages stay `unknown` and the score carries a
  provisional flag instead of a lowered guess.
- **One knowledge source.** The framework and its statistics come from one
  video. In chat, figures are labeled `[video]` (as cited in the video),
  `[general]` (beyond the video), or `[not covered]` (the video says nothing;
  say so, do not guess). The knowledge base, not the model's memory, answers
  questions.
- **Two audiences, two documents.** Chat audit stays labeled and
  framework-grounded. `report.md` reaches readers with no context, so it
  never mentions the video or the framework (`references/report-writing-rules.md`,
  rules 8-9).
- **Scripts do the grunt work.** Capability checks, fetching, capture
  scaffolding, and score computation are deterministic Python and cost no
  tokens. The LLM does routing, judgment, and writing.
- **Capture is opt-in.** No consent, no files: chat-only mode leaves the
  filesystem untouched. Mid-flow decline stops writing immediately.
- **Honest declines.** Out-of-scope requests get a scope statement and the
  nearest covered alternative. This is deliberate: an SEO audit from a
  monetization checklist would be fabrication with extra steps.

## Score mechanics

The Digital Home Score is a mechanical sum, no judgment calls, computed per
Section I of `references/audit-checklist.md`:

| Block | Points | Rule |
|-------|--------|------|
| Three test questions | 0-3 | buy-today path (B), free path with email capture (C), next offer for buyers (D) |
| Five layers | 0-5 | 1 per `present` layer, 0.5 per `limited`, 0 for `missing` or `unknown` |
| Reach & ownership | 0-2 | FAQ or public Q&A (G); owned email capture plus checkout on the owned domain (H) |

Verdict bands: below 4 = `digital brochure`, 4 to below 8 = `partial digital
home`, 8 and up = `digital home`. The number leads everywhere the audit
appears: chat, JSON, and report.

## Recommendation rubric

Fixes are generated only from numbered gaps, 3 to 8 per audit. Each carries
effort, cost, time, resources, and dependencies; a rubric formula computes
priority and names the "start here" pick. Every recommendation cites its gap
and its knowledge-base principle. Recommendations built on `unknown` or
`limited` evidence carry a provisional flag.

## Hard bounds

- At most 10 pages per audit, 2 levels deep (fewer is fine)
- At most 4 routing questions, 2 routing rounds
- At most 5 intake questions
- 3 to 8 recommendations
- Fetch timeouts: 15s / 20s / 25s, built into the script

## Error handling summary

Full rules live in SKILL.md ("Error Handling"). The shape: disclose failures
as they happen with concrete recovery options (paste content, describe the
page, confirm skipping), never mark unread pages as missing, audit the rest,
and mark findings from pasted content as `limited`. Login-walled sites get a
stated reduced scope. Script errors print actionable stderr; retry at most
twice per page.