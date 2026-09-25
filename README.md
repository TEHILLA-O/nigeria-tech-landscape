# Nigeria tech landscape (fintech + tech)

Open research dataset for **Tehilla Obanor / Omnific Hand**: Nigerian fintech and tech companies ranked by **total disclosed funding** (USD), plus a large **Directory** of real companies without clean disclosed funding totals. Short product notes, valuation status, ease-of-replication scores, and typical Nigeria licence hurdles are included where we could write honest notes.

This is not a paid Crunchbase dump. It is a careful public-sources compile. Funding and valuations are only included when we could point at a public figure. If something is unknown, it is marked **Undisclosed** or left blank. Nothing here is invented.

## Coverage (honest)

| Sheet / file | Rows |
|---|---|
| Ranked with disclosed funding (`Ranked_Disclosed`) | **102** |
| Directory without clean disclosed totals (`Directory`) | **987** |
| Notable no-funding subset (`No_Disclosed_Funding`) | **50** |
| **Grand unique total** | **1089** |

Directory volume comes mainly from **CBN Payment Service Provider / MMO / IMTO licence lists**, **FCCPC digital money lender registrations**, YC Africa (Nigeria) cohorts, StartupMapAfrica Nigeria sector pages, and curated press roundups. Licence rows have thin but real product blurbs tied to the licence category. Funding figures are never guessed.

Last verified: **2026-09-25**.

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

## How ranking works

1. Primary key: **Total_Disclosed_Funding_USD** (descending).
2. Figures may include equity and debt when press reported a combined total. See `Replicate_Notes` / Methodology for caveats (especially Moove, VertoFX, Grey, Fincra).
3. Valuations: only when publicly reported. Status column is `Reported`, `Estimated_by_press`, or `Undisclosed`.
4. **Ease_to_Replicate** is 1 (hardest) to 5 (easiest) for a small London digital consultancy / builder profile (ML, automation, product tooling) - **not** for a bank with unlimited capital.
5. Aliases merged where obvious (TeamApt -> Moniepoint, Appzone -> Zone, PayHippo -> Rivy, Paylater -> Carbon, Mkudi -> Nomba). Jumia is included as a Nigeria-major marketplace with clear disclosed funding (it is regional).
6. **Directory** holds everyone else we could identify from regulators or credible directories without inventing a funding total.

## Files

```
data/ranked_disclosed.csv          # ranked table (sourced funding only)
data/directory.csv                 # large no-funding directory
data/no_disclosed_funding.csv      # short notable subset of directory
data/licences_cheat_sheet.csv      # Nigeria licence map
data/Nigeria_Fintech_Tech_Ranked.xlsx  # multi-sheet workbook
data/extra_funded.json             # newly sourced funded rows
data/curated_directory.json        # curated non-licence seed blurbs
docs/licences.md                   # plain-English licence notes
sources.md                         # bibliography of URLs used
scripts/expand_build.py            # rebuild helper
raw_sources/                       # cached public licence/directory HTML (optional)
```

## How to use

- Open the CSV in Sheets/Excel, or the xlsx workbook (`Ranked_Disclosed` + `Directory` sheets).
- Filter by `Sector` (Fintech, SaaS, Marketplace, Logistics, Healthtech, Edtech, Agritech, AI, Cleantech, Insurtech, Other Tech).
- Sort or filter `Ease_to_Replicate` if you care about what a small team could actually build vs what needs a banking licence and float.
- Always click through `Source_URLs` before making a commercial decision. Numbers drift after every round.

## Rebuild

```bash
python3 -m venv .venv && .venv/bin/pip install openpyxl
# optional: refresh raw_sources/*.html from CBN/FCCPC/etc.
.venv/bin/python scripts/expand_build.py
```

## Getting closer to 1000+ with richer funding columns

This repo already clears **1000+ unique company names**. What still blocks **1000 Ranked_Disclosed funding rows** is paywalled deal databases (Crunchbase Pro, Tracxn, PitchBook). Free press roundups cover tens to low hundreds of clean totals, not thousands. Directory growth can continue via more SEC/NAICOM/NITDA public registries and deeper StartupList crawls.

## Licence

MIT for the compilation and documentation in this repository. Underlying company trademarks belong to their owners. Source articles remain under their publishers' terms.

## Disclaimer

Not investment advice. Not legal advice. Licence capital figures can change when CBN/SEC/NAICOM update circulars - check the regulator pages before you rely on them.
