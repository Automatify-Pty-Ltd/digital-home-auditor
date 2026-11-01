# Report writing rules

Read once before the first user-facing output of the engagement (audit
presentation, recommendations, Q&A answers, report.md) and apply throughout.
Picked from the `unslop` skill: rules 1-7 are the patterns that most often
wreck an audit report. Rules 8-9 make report.md readable for someone with
no context at all.

1. **No puffery, no promotion.** Cut "vibrant", "stunning", "beautifully
   designed", "impressive". A site is described by evidence, not adjectives.
   Write "The homepage states the company serves 40+ clients", not "The
   homepage showcases an impressive client roster".

2. **Plain words.** "Serves as" is "is". "Utilize" is "use". "Facilitates"
   is "helps". "Crucial" is the concrete reason something matters, stated
   as that reason.

3. **No "not just X, but Y" and no forced triples.** State the point
   directly. Use the natural number of examples; three is not a magic
   number.

4. **Numbers, quotes, and facts instead of feelings.** Every finding is a
   page, a quote, a count, or a score. Replace "significantly" with the
   delta. Replace "feels dated" with "the latest blog post is from March
   2023". If a sentence cannot be restated as a fact, quote, or number,
   cut it.

5. **Specific endings, no chatbot closers.** No "the future looks bright",
   "I hope this helps", "let me know if you want more", "great question".
   End with the concrete change: "The buy path adds 1 point to the score
   and gives visitors a way to spend money today."

6. **Vary the rhythm.** Short sentences for findings. A longer one when
   the reasoning needs room. One idea per sentence; if the reader has to
   backtrack to parse a sentence, split it.

7. **Punctuation discipline.** No em dashes anywhere; use periods or
   commas. Colons only before lists and tables. No bold label that repeats
   the words after it. Sentence case for headings. Straight quotes.

8. **No source meta-references in report.md.** Never write "as cited in the
   video", "the video says", "the framework", or "this skill" in the
   report. State ideas and figures directly, hedged where needed: "a
   common benchmark: roughly one in four online customers buys again".
   Exact provenance stays in the JSON captures; chat Q&A keeps its own
   labels.

9. **In report.md, write for a reader with zero context.** No framework
   term without a plain-language definition at first use; prefer plain
   words outright. "Collection points" becomes "ways people can spend
   money or stay in touch". "Funnel" becomes "the follow-up emails
   people get after signing up". Define the score in one line at the
   top. Never explain a term by pointing at a later section; each line
   makes sense where it stands.

Self-audit before delivering: read the text and ask "what makes this
obviously AI generated?" Fix what shows up. For report.md also ask:
"would this make sense to someone who has never heard of this
framework?" The score, the tables, and the fetch disclosure carry the
facts; these rules make them easy to read.