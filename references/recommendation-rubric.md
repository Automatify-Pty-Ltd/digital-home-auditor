# Recommendation rubric — scoring, ranking, honesty rules

Every recommendation must trace to an audit gap (numbered in audit.json,
section I) and to a knowledge-base principle. No orphan advice, no invented
statistics. 3–8 recommendations; if the audit found fewer than 3 real gaps,
say that instead of padding.

## Dimensions (score every recommendation on all five)

| Dimension | Scale | Anchors |
|-----------|-------|---------|
| **Effort** | 1–5 | 1 = copy/CTA edit on one page · 2 = edits across a few pages · 3 = new page + content · 4 = new offer/funnel build · 5 = new product/business line |
| **Cost** | band | `$0` · `<$50` · `<$500` · `<$2k` · `$2k+` (tools, ads, services — not labor time) |
| **Time** | band | `S` < 2h · `M` < 2 days · `L` > 2 days (calendar time to live) |
| **Resources** | list | What's needed: email tool, checkout, landing-page builder, AI agent, VA/designer, existing list… |
| **Dependencies** | list | Hard prerequisites — e.g. "needs an email list tool first", "needs the offer decided before the page". Order dependent recs after their dependency, never before. |
| **Impact** | 1–5 | 5 = creates a missing collection point or fixes a `critical` gap · 4 = fixes `high` · 3 = strengthens a weak layer · 2 = polish with conversion effect · 1 = hygiene |

## Ranking formula (deterministic)

```
cost_index:  $0=1, <$50=2, <$500=3, <$2k=4, $2k+=5
time_index:  S=1, M=2, L=3
priority = (impact × 3) / (effort + cost_index + time_index)
```

Sort descending by priority (2 decimals). Ties → lower effort first. Rank 1 =
do this first. The "start here" pick is rank 1 *unless* a dependency forces
another rec ahead of it — then say so explicitly.

Impact dominates on purpose: a cheap tweak that fixes a `critical` gap (e.g.
adding a buy button) outranks a cheap tweak that merely polishes.

## Honesty rules

1. **Every recommendation cites:** `addresses_gap: N` (from audit.json) and
   `principle: "<knowledge-base concept>"` — one line on why this rec follows
   from the framework, in the user's words.
2. **Evidence basis flag:** if any audit evidence was `unknown`/`limited`, mark
   the whole set `provisional` and name what would make it firm (e.g. "the
   pricing page was a bot wall; confirm the pricing and this rec firms up").
3. **Provenance:** no statistics unless they exist in the knowledge base, and
   then only as "as cited in the video".
4. **Out-of-rubric honesty:** if a gap needs work this skill doesn't cover
   (technical SEO, performance, accessibility), say so and recommend the right
   kind of specialist — don't improvise advice outside the framework.
5. **One business, one audience:** recommendations that would split focus
   across audiences (the coffee + car insurance trap) must carry a warning or
   be cut.

## Output shape

Per recommendation (also the JSON shape in capture-schemas.md):

```json
{
  "rank": 1,
  "title": "Add a buy path for the flagship service",
  "what": "concrete action, one or two sentences",
  "addresses_gap": 2,
  "principle": "collection points / buy-today test",
  "why": "reasoning tied to the audit evidence",
  "effort": 2, "cost": "<$50", "time": "S",
  "resources": ["existing page builder"],
  "dependencies": [],
  "impact": 5,
  "priority": 2.5
}
```

## Worked example

Audit found: services page has no prices and no buy button (gap 2, critical);
newsletter link in footer only (gap 3, high). Email tool exists per intake.

- Rec A "Add a buy path": effort 2, cost <$50 (stripe link), time S, resources
  [payment link], deps [], impact 5 → priority = (5×3)/(2+2+1) = **3.00**
- Rec B "Lift the newsletter into a lead magnet + opt-in block": effort 3, cost
  $0 (existing tool), time M, resources [email tool, lead magnet copy], deps
  [], impact 4 → priority = (4×3)/(3+1+2) = **2.00**

Rank A first, mark it "start here". If evidence for the services page was
`unknown` (bot wall), both recs carry `provisional` until the user confirms
what's on that page.