# Methodology

Last verified: **2026-09-25**.

This document explains how the Nigeria tech landscape dataset is built, ranked, and annotated. It is research documentation, not legal or investment advice.

## Scope

- Nigeria-founded or Nigeria-primary fintech and adjacent tech companies.
- Regional firms with major Nigeria operations may appear (for example Jumia) when disclosed funding is clear and Nigeria is a core market.
- Directory rows also include CBN-licensed payment entities and FCCPC-registered digital money lenders even when product marketing is thin.

## Ranking rules

1. **Primary sort key:** `Total_Disclosed_Funding_USD` descending.
2. Only include a funding total when at least one public source states a figure (company blog, reputable press, regulator-adjacent disclosure, S-1 / exchange filing).
3. Prefer company primary sources over secondary roundups when they conflict.
4. If only a single round is public, the ranked total may equal that round. Notes say so.
5. Ties keep stable prior order; we do not invent tie-breakers from headcount or valuation.

## What we never invent

- Funding amounts or cumulative totals
- Valuations
- Employee counts / ranges (only when LinkedIn or press states a public range)
- Founders or CEO names
- Licence status (Active licence vs applied)

Unknown fields stay blank, `Unknown`, or `Undisclosed`.

## Debt vs equity caveats

Press roundups sometimes sum **equity + debt + facilities** into one "raised" number.

Known caution rows (non-exhaustive):

- **Moove:** mobility finance; cumulative figures can blend equity and vehicle financing facilities.
- **VertoFX / Grey / Fincra:** some free lists under-report historical equity or highlight grants; treat small cells as floors when Notes say so.
- **Moniepoint:** Series C had a first close (2024) and a later completion announcement (2025). Ranking uses the defended cumulative total; latest-round fields cite the completion announcement.

Always read `Replicate_Notes` / `Notes` and click `Source_URLs`.

## FX and currency

- Store ranking figures in **USD** as reported by sources.
- Convert Naira-denominated rounds to USD **only** when the source itself states a USD equivalent.
- We do not restate old rounds at current FX.

## Heuristic vs researched fields

| Field class | Ranked_Disclosed | Directory |
|---|---|---|
| Funding / valuation / founders / licences held | Researched or blank | Almost always blank / Undisclosed |
| Ease_to_Replicate, default Licences_Regs_Needed | Manual notes + judgement | **Category heuristics** (`Heuristic=Yes`) |
| Opportunity_Angle_for_Builder | Written per company where possible | Short category default |
| Website | Researched / YC / company site | Filled when findable; left blank for pure regulator rows if unknown |

Heuristics are documented in `scripts/enrich_and_rebuild.py` (`CATEGORY_HEURISTICS`, `SECTOR_DEFAULTS`). They are starting points for builders, not diligence conclusions.

## Ease_to_Replicate scale

Scored **1 (hardest) to 5 (easiest)** for a small digital consultancy / builder profile (automation, ML, product tooling), **not** for a bank or OEM with unlimited capital.

Typical anchors:

- 1: National switch, licensed bank, dense agent network, mini-grid capex
- 2: Licensed MMO/MFB, multi-country remittance, heavy field credit
- 3: Crowded fintech product with partner-bank path
- 4: Vertical SaaS / data / content with distribution work
- 5: Thin SaaS workflow tools with PSP checkout

## Data confidence

- **High:** company primary source plus at least one reputable press or regulator corroboration for key facts used.
- **Med:** credible public sources, thinner corroboration, or fast-moving fields (CEO, headcount).
- **Low:** single secondary list, early-stage, or partial funding floor only.

## Directory construction

1. Parse CBN PSSP / PTSP / MMO / IMTO / Super-Agent / Switching lists.
2. Parse FCCPC digital money lender approvals.
3. Add YC Nigeria companies and curated StartupMapAfrica / press names without inventing funding.
4. Remove parse junk (addresses mistaken for legal names, numbered artefacts).
5. Deduplicate aliases against Ranked where obvious.
6. Apply category heuristics for Ease, licences needed, and builder angles.

## Licence notes

Licence commentary is **high-level research**, not a filing guide and not legal advice. Capital thresholds and forms change. Confirm on the live CBN, FCCPC, SEC Nigeria, and NAICOM pages (see `docs/licences.md`).

## Rebuild reproducibility

```bash
.venv/bin/python scripts/enrich_and_rebuild.py
```

Inputs: `data/ranked_disclosed.csv` (base), `data/ranked_enrichment.json`, `data/directory.csv` seeds / prior build, `raw_sources/*`, YC name list.

Outputs: enriched CSVs, `funding_rounds.csv`, `investors.csv`, `companies_enriched.json`, xlsx workbook, `build_meta.json`.

## Change policy

When adding a company or changing a funding cell, include a `Source_URLs` entry and update `Last_Verified_Date`. See `CONTRIBUTING.md`.
