# Failure modes, fixes, and results

Honest notes on where this dataset went wrong and how it was fixed. Everything below comes from the commit history and `CHANGELOG.md`. Nothing is invented.

## What can go wrong

- **Double counting after a rebrand.** One company under two names gets its funding counted twice and takes two ranks.
- **Equity and debt blended together.** Press headlines often mix equity rounds with credit facilities, which inflates "total raised".
- **Stale companies looking active.** A company that went quiet years ago still ranks on old funding.
- **Junk rows from scraped regulator lists.** PDF and app lists from regulators parse badly and produce fake "companies".
- **Guessing to fill blanks.** The easiest way to make coverage look good is to invent founders or totals. The rule here is blanks over guesses.

## What went wrong

1. **Lemonade Finance and LemFi were ranked as two companies** (Rank 28 and Rank 13). They are the same entity after the May 2023 rebrand, so $32.7M of overlapping funding was being counted on top of LemFi's $85M. LemFi's founders were also recorded wrongly as "Ridwan Bello; Rian Bello".
2. **Four parse-junk rows in the Directory**: concatenated FCCPC app lists and an address picked up as a company name from the IMTO list.
3. **Funding conflicts**: Moove's equity vs debt facilities, Moniepoint's Series C closes, and the Interswitch Visa stake did not agree across sources.
4. **Commercial framing leaked into an open dataset.** An interim pass added consultancy sales columns and a shortlist, which did not belong in neutral public research.

## How it was resolved

1. Lemonade Finance removed from Ranked and kept as a Directory alias pointing at LemFi. LemFi keeps the $85M total, the YC pre-seed round was reattributed, and founders corrected to Ridwan Olalere and Rian Cochran from YC, company and press sources. Ranks rebuilt.
2. Junk rows removed, with details in `raw_sources/deep_research/directory_quality_pass.json`. Directory went from 981 to 977 rows.
3. Conflicts logged in `docs/Funding_Caveats.md` and `data/funding_caveats.csv` instead of silently picking a number.
4. The sales layer was deleted, the column renamed to neutral `Builder_Notes`, and the docs rewritten as plain research.
5. Stale signals: a `Possibly_stale` flag marks companies whose last signal is more than 18 months old (30 Yes, 2 No, 69 Unknown as of 2026-09-25).

## Results

- 101 companies ranked by disclosed funding, 977 in the Directory, 1,078 unique rows in total.
- Website coverage on Ranked went to 101/101 and founders to 100/101. PalmPay's founders are left blank on purpose because there is no clean public founder list.
- Founder LinkedIn coverage went from 0/101 to 40/101, public profiles only. The pass stopped there rather than guess.
