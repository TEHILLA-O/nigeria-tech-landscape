# Nigeria tech landscape (fintech + tech)

Open research dataset compiled by **Tehilla Obanor**: Nigerian fintech and adjacent tech companies, ranked by **total disclosed funding (USD)**, plus a large **Directory** of real firms drawn from regulators and public lists.

This is careful public-source research, not a scraped Crunchbase dump. Funding and valuations appear only when a public figure could be pointed at. Unknown stays blank, `Unknown`, or `Undisclosed`. Nothing here is invented.

> **How to cite:** see `CITATION.cff` and the [Cite this dataset](#cite-this-dataset) block below.

## Why this exists

Builders, operators, and researchers need an honest map of who is licensed, who has raised, and what is hard to copy. Most Africa startup lists either invent numbers or stop at logos. This repo prefers blanks over guesses.

## Coverage (2026-09-26)

| Sheet / file | Rows |
|---|---|
| Ranked with disclosed funding (`Ranked_Disclosed`) | **101** |
| Directory without clean disclosed totals (`Directory`) | **977** |
| Notable no-funding subset (`No_Disclosed_Funding`) | **50** |
| Sourced funding rounds (`funding_rounds.csv`) | **129** |
| Investors appearing in sourced rounds (`investors.csv`) | **119** |
| **Grand unique company rows** | **1078** |

Directory volume is driven by **CBN** payment-licence lists, **FCCPC** digital money lender registrations, YC Nigeria cohorts, and curated press / map roundups. Licence rows keep thin but real blurbs. Funding is never guessed for Directory.

### Enrichment coverage (Ranked)

| Field | Coverage |
|---|---|
| Website | 101/101 (100%) |
| Founders | 100/101 (99%) |
| CEO / lead | 75/101 (74%) |
| High data confidence | 37/101 (36%) |
| Builder_Notes | 101/101 (100%) |
| Company status | 101/101 (100%) |
| Exit_Type (incl. None) | 101/101 (100%) |
| JTBD / ICP | 101/101 (100%) |
| Peers | 101/101 (100%) |
| Sector_Primary / Secondary | 101/101 (100%) |
| Possibly_stale | 101/101 (100%) |
| Topics | 101/101 (100%) |
| Founder LinkedIn (public) | 40/101 |
| Register_Last_Checked (regulated subset) | 30/101 |
**Status / exit note:** Known public exits on the ranked sheet include Jumia (IPO 2019), Paystack to Stripe (2020), Brass to a Paystack-led consortium (2024), Mono to Flutterwave (2026), plus shutdowns for Okra (2025), 54gene (~2023), and Bundle Africa exchange (2023). Lemonade Finance was **deduped into LemFi** (Directory alias; same May 2023 rebrand entity). LemFi remains the sole ranked row. All other ranked rows are **Active** with `Exit_Type=None` unless a public exit source is found. Never invent exits.

Directory: regulator tagged for CBN (277), FCCPC (562), YC (37), Press (63), Other (38). Category heuristics fill Ease / licences / builder notes (`Heuristic=Yes`).

## Top 10 by disclosed funding

| Rank | Company | Disclosed funding (USD) |
|---|---|---|
| 1 | Jumia | $885,400,000 |
| 2 | OPay | $570,000,000 |
| 3 | Flutterwave | $474,960,000 |
| 4 | Moove | $445,000,000 |
| 5 | Andela | $381,000,000 |
| 6 | Moniepoint (TeamApt) | $328,158,694 |
| 7 | Interswitch | $310,000,000 |
| 8 | PalmPay | $140,000,000 |
| 9 | Lumos Global | $125,000,000 |
| 10 | TradeDepot | $123,000,000 |

## Example: how to read a row (Moniepoint)

Take **Moniepoint (TeamApt)** in `Ranked_Disclosed`:

1. **Funding:** `Total_Disclosed_Funding_USD` is the best public cumulative total we could defend for ranking. Treat it as a floor that drifts after every close.
2. **Latest round:** Series C completed above $200M (company blog, Oct 2025), led by DPI with LeapFrog and others. That is also in `funding_rounds.csv`.
3. **People:** Founders Tosin Eniolorunda and Felix Ike; Group CEO Tosin Eniolorunda (company sources).
4. **Moat:** Agent/POS density plus MFB / payments licences. The software layer is copyable; the distribution and licence stack are not.
5. **Builder notes:** Adjacent research angles include bookkeeping automation, credit decisioning features, agent analytics, or dispute/fraud ops tooling around Moniepoint-class merchants and peer MFBs. This is research context, not a sales target list.
6. **Confidence:** High when company + major press agree. Still click `Source_URLs` before any commercial decision.

Flutterwave is the payments-infrastructure twin of this pattern: multi-market licences and bank integrations are the moat; checkout UX alone is not.

## Files

```
data/ranked_disclosed.csv
data/directory.csv
data/no_disclosed_funding.csv
data/funding_rounds.csv
data/investors.csv
data/licences_cheat_sheet.csv
data/companies_enriched.json
data/Nigeria_Fintech_Tech_Ranked.xlsx
data/ranked_enrichment.json
docs/methodology.md
docs/data_dictionary.md
docs/sector_playbooks.md
docs/licences.md
docs/dashboard/index.html (filters + CSV export)
data/nigeria_tech_landscape.sqlite
CHANGELOG.md
sources.md
scripts/enrich_and_rebuild.py
scripts/expand_build.py
raw_sources/
CONTRIBUTING.md
CITATION.cff
```

## How ranking works

1. Primary key: **Total_Disclosed_Funding_USD** (descending).
2. Figures may include equity and debt when press reported a combined total. See Methodology and per-row notes (especially Moove, VertoFX, Grey, Fincra).
3. Valuations: only when publicly reported. Status is `Reported`, `Estimated_by_press`, or `Undisclosed`.
4. **Ease_to_Replicate** is 1 (hardest) to 5 (easiest) for a small digital product / ML tooling team, not for a bank with unlimited capital.
5. Aliases merged where obvious (TeamApt -> Moniepoint, Appzone -> Zone, PayHippo -> Rivy, Paylater -> Carbon, Mkudi -> Nomba, Lemonade Finance -> LemFi).
6. **Directory** holds everyone else we could identify from regulators or credible directories without inventing a funding total.

Full detail: [`docs/methodology.md`](docs/methodology.md).

## How to use

- Open the CSV in Sheets/Excel, or the xlsx workbook (`Ranked_Disclosed` + `Directory` + reference sheets).
- Prefer JSON (`data/companies_enriched.json`) if you want nested objects for builders.
- Filter by `Sector`, `Licence_or_Category`, or `Ease_to_Replicate`.
- Use `Builder_Notes` for optional research context on adjacent tooling; it is not a go-to-market pipeline.
- Always click through `Source_URLs` before making a commercial decision. Numbers drift after every round.

## Docs map

| Doc | Purpose |
|---|---|
| [Methodology](docs/methodology.md) | Ranking rules, FX, debt vs equity, heuristic vs researched |
| [Data dictionary](docs/data_dictionary.md) | Column definitions |
| [Sector playbooks](docs/sector_playbooks.md) | Payments, lending, banking, SaaS, logistics, health, edtech, energy, HR |
| [Licences](docs/licences.md) | High-level Nigeria licence paths (not legal advice) |
| [Funding caveats](docs/Funding_Caveats.md) | Disputed totals (Moove and others) |
| [Sources](sources.md) | Bibliography |
| [Contributing](CONTRIBUTING.md) | How to add a company honestly |

## Rebuild

```bash
python3 -m venv .venv && .venv/bin/pip install openpyxl pandas
# optional: refresh raw_sources from CBN/FCCPC/etc.
.venv/bin/python scripts/enrich_and_rebuild.py
```

See [`scripts/README.md`](scripts/README.md).

## Limitations (read these)

- Free press and regulator lists cover tens to low hundreds of clean funding totals, not thousands. Paywalled databases (PitchBook, Crunchbase Pro) would raise Ranked_Disclosed further; we refuse to invent.
- Some cumulative funding cells mix equity and debt or use generous press math. Row notes call out known caveats.
- Founder / employee / licence fields are sparse where public sources disagree or are silent. Blank means unknown, not zero.
- Licence tags are research aids, not a substitute for counsel or the live CBN/FCCPC register.
- Directory Ease scores for licence rows are **heuristics** (`Heuristic=Yes`), not company-specific diligence.

## Cite this dataset

```
Obanor, Tehilla (2026). Nigeria tech landscape (fintech + tech) open research dataset.
GitHub: https://github.com/TEHILLA-O/nigeriatechlandscape
Commit: see repository main branch. Last verified 2026-09-26.
```

Or use `CITATION.cff`.

## Licence

MIT for the compilation and documentation in this repository. Underlying company trademarks belong to their owners. Source articles remain under their publishers' terms.

## Disclaimer

Not investment advice. Not legal advice. Licence capital figures and registers change when CBN, FCCPC, SEC, or NAICOM update circulars. Check the regulator pages before you rely on them.


## Paid vendor imports

Crunchbase/Tracxn merge is **BLOCKED** without a licensed paid export. See `data/imports/README.md` and empty schema CSVs. Do not scrape paywalls.
