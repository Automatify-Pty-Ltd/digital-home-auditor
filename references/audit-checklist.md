# Audit checklist — how to walk a website

Work sections A→I in order. Every finding needs **evidence**: the page URL
plus a quote or the on-page element that proves the status. Evidence-free
claims do not go in the audit.

**Status vocabulary** (use exactly these):
- `present` — found, with evidence
- `missing` — page was read and the thing is genuinely not there
- `limited` — present but weak/incomplete (say what's weak)
- `unknown` — the page could not be read; **unknown is never a verdict** and
  never silently becomes `missing`. Disclose it in the fetch report and ask
  the user about it.

**Severity:** `critical` (blocks money flowing), `high` (major collection
point or layer gap), `medium` (weakness worth fixing), `low` (polish).

## A. Collection-point inventory (the core of the audit)

Walk every fetched page and list **every way someone can spend money or start
a relationship** with the business: buy button, product with a price, service
package, booking link, lead magnet, newsletter opt-in, quiz, community/event
sign-up, merch, donation — anything exchangeable.

- Record each as: name, type (buy / free-capture / relationship), page, evidence.
- Count them. Interpretation (from the knowledge base): 0 = digital brochure;
  1–2 = fragile, one bet; 3+ = starting to look like a home; the packed cafe
  runs 30+.
- A page that failed to fetch may hide collection points — mark the count
  "incomplete" and say which pages are unread, rather than undercounting silently.

## B. Buy-today test (test question 1)

Find the single clearest path a ready-to-buy visitor can take from homepage to
payment. Trace it: entry → offer → checkout/booking. Record: the path, the
number of steps, where friction appears (no price, "contact us" instead of a
buy, dead link, unclear CTA). If no buy path exists at all, that is a
`critical` gap — this is the emptiest-cafe failure mode.

## C. Free-path test (test question 2)

What can a not-ready visitor take for free in exchange for staying in touch?
Look for: lead magnet (guide/checklist/template), quiz funnel, newsletter
opt-in, free community. Record: the asset, where it's offered (above the fold?
buried?), what is exchanged (email? attention?). Email capture is the guestbook
— `missing` here means the site has no way to build a list it owns.

## D. Next-offer test (test question 3)

What is offered *after* the first purchase? Look for: upsells, cross-sells,
bundles, "what's next" journeys, tiered products. If the site sells exactly one
thing with no visible next step, record it — repurchase odds are ~1 in 4 (as
cited in the video), so the next door has to be built on purpose.

## E. The five layers

For each layer, judge the *best* collection point found in A–D (a site is
only as strong as its strongest path):

- **Offer:** is the main promise an "aspirin for the headache" — a solution to
  a stated immediate problem? Or vague self-description?
- **Copy:** does the text enter the visitor's conversation (their words, their
  problem) or just describe the business ("we are passionate about…")?
- **Content:** foot traffic — is there a blog/videos/updates section answering
  real customer questions, and does it look alive (dates, cadence) or abandoned?
- **Landing pages:** does each offer have a single-focus page with one CTA, or
  is the multipurpose homepage being asked to do a landing page's job?
- **Funnel:** after an opt-in, is there evidence of a nurture path (welcome
  sequence mention, automation, "you'll get…")? Or does capture lead nowhere?

## F. Value ladder

List every price point found (free → top). Check rungs exist: free thing →
small paid → mid → premium. Record the gaps between rungs. Most customers stay
at the bottom rung — that's fine; the question is whether rungs exist at all.

## G. AI-discoverability

- Is there an FAQ answering the actual questions customers ask?
- Does the site publicly answer its customers' questions in depth (topical
  authority)?
- Does the site link to the brand's presence on other platforms (YouTube,
  social) — signposts pointing back to the home?
- Every answer to a customer question that exists only in DMs/calls but not on
  the site is a missed signpost.

## H. Ownership check

Where does the relationship live? Look for: email capture owned by the site
(yes/no), checkout on owned domain vs external marketplace, social links
(roads in — good) vs the *only* presence being social (digital homelessness —
risky). Record what is owned vs rented.

## I. Digital Home Score, verdict, and gap list

**Digital Home Score (0–10)** — computed mechanically, no judgment calls.
Every point traces to a section of this checklist:

| Block | Points | Rule |
|-------|--------|------|
| Three test questions | 0–3 | 1 each: buy-today path exists (B), free path with email capture exists (C), next offer for buyers visible (D) |
| Five layers | 0–5 | 1 per layer `present`; 0.5 per layer `limited`; 0 for `missing` or `unknown` (E) |
| Reach & ownership | 0–2 | 1: FAQ or public question-answering present (G); 1: email capture owned by the site and checkout on the owned domain (H) |

- **Verdict label = the score's band:** below 4 → `digital brochure`;
  4 to below 8 → `partial digital home`; 8 and up → `digital home`. No
  separate verdict judgment, no rounding at band boundaries.
- **Presentation rule:** lead with the number everywhere the audit appears —
  chat, report, JSON: `Score: 6/10 — partial digital home · 4 collection
  points found`. The rest of the audit explains it.
- **Provisional flag:** if any scored item rests on `unknown` or `limited`
  evidence, the score carries `provisional: true` plus what would firm it
  up (the unread pages). Report the provisional number with its caveat —
  never lower it into a guess.
- **Worked example:** buy-today yes, free path yes, next offer missing (2/3);
  offer present, copy present, content limited, landing pages limited, funnel
  missing (3/5); FAQ present, checkout on a marketplace only (1/2) →
  **6/10, partial digital home**; biggest losses: no funnel, no next offer.
- Compile every gap found in A–H into a numbered list with severity and
  evidence. Gaps feed the recommendation flow: every recommendation must
  cite a gap by number.