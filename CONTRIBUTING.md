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
