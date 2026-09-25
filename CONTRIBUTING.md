# Contributing

Thanks for helping keep this dataset honest.

## Ground rules

1. **Never invent** funding, valuations, employee counts, founders, or licence status.
2. Prefer primary sources: company blogs, regulator registers, reputable press.
3. Every funding or valuation cell needs a `Source_URLs` entry.
4. If you cannot verify, leave the field blank and say so in Notes.
5. No em or en dashes in README prose (plain hyphens only).

## Add a Ranked company (disclosed funding)

1. Confirm a public cumulative or round total.
2. Add a row to `data/ranked_disclosed.csv` **or** an entry in `data/ranked_enrichment.json` and rebuild.
3. Fill Product_Summary, Sector, Source_URLs, Last_Verified_Date.
4. Add a row to `data/funding_rounds.csv` when you have company + (amount or type) + date + source.
5. Run `scripts/enrich_and_rebuild.py`.
6. Open a PR with the source links in the description.

## Add a Directory company

1. Prefer regulator lists (CBN, FCCPC) or YC / credible directories.
2. Do **not** invent funding. Leave totals blank.
3. Set `Regulator_Source`, `Licence_or_Category`, and `Heuristic=Yes` if using category defaults.
4. Rebuild and PR.

## Deduping

Check aliases before adding: TeamApt/Moniepoint, Appzone/Zone, PayHippo/Rivy, Paylater/Carbon, Mkudi/Nomba, Identitypass/Prembly, etc. (`scripts/expand_build.py` has an alias map).

## Licence commentary

Keep licence notes high-level. Link the regulator page. Do not give filing advice.

## Tone

Write like a careful researcher. Short sentences. No hype.

## Good first issues

Concrete tasks that help without inventing numbers:

1. **Fill one blank Website** on Ranked or Directory from the company primary site (PR must include the URL you used).
2. **Add a sourced funding round** to `data/funding_rounds.csv` with Company, Round_Type, Amount_USD (if disclosed), Date, Investors, and Source_URLs. No guessed amounts.
3. **Confirm one licence row** against the live CBN or FCCPC register; update `Register_Last_Checked` and Notes.
4. **Improve one thin Directory blurb** using the company About page (still no invented funding).
5. **Add Founder_LinkedIn_URLs** only when the public profile clearly matches the named founder. Never invent URLs.
6. **Tag Topics** on a Ranked row (semicolon tags such as `cross-border`, `agent-network`, `credit-scoring`, `HR`, `energy-PAYG`).
7. **Document a funding conflict** in `docs/Funding_Caveats.md` / `data/funding_caveats.csv` when two reputable sources disagree.
8. **Fix a Directory parse artefact** (address-as-name, concatenated app list) by removing or splitting the row and noting it in the PR.

Pick one row, keep the diff small, and link sources in the PR body.

