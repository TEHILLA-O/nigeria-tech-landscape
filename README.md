# Nigeria tech landscape (fintech + tech)

Open research dataset for **Tehilla Obanor / Omnific Hand**: Nigerian fintech and tech companies ranked by **total disclosed funding** (USD), with short product notes, valuation status, ease-of-replication scores, and typical Nigeria licence hurdles.

This is not a paid Crunchbase dump. It is a careful public-sources compile. Funding and valuations are only included when we could point at a public figure. If something is unknown, it is marked **Undisclosed** or **Unknown**. Nothing here is invented.

## Coverage (honest)

| Sheet / file | Rows |
|---|---|
| Ranked with disclosed funding | **96** |
| Notable names without clean disclosed totals | **10** |

**"Top 1000" was not reachable from free public sources.** Disrupt Africa historically tracked a few hundred funded Nigerian startups across multi-year windows; Tracxn-style indexes claim hundreds of funded NG fintechs, but most individual totals sit behind paywalls. This repo ranks every company we could source a disclosed figure for, then lists a short "no disclosed funding" tab for notable gaps.

To get closer to 1000 verified funding rows you would need a paid Crunchbase or Tracxn export (or similar), plus manual dedupe of aliases and debt vs equity.

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
5. Aliases merged where obvious (TeamApt -> Moniepoint, Appzone -> Zone, PayHippo -> Rivy, Paylater -> Carbon). Jumia is included as a Nigeria-major marketplace with clear disclosed funding (it is regional).

## Files

```
data/ranked_disclosed.csv          # main ranked table
data/no_disclosed_funding.csv      # notable names without clean totals
data/licences_cheat_sheet.csv      # Nigeria licence map
data/Nigeria_Fintech_Tech_Ranked.xlsx  # same data as multi-sheet workbook
docs/licences.md                   # plain-English licence notes
sources.md                         # bibliography of URLs used
scripts/                           # rebuild helpers (optional)
```

## How to use

- Open the CSV in Sheets/Excel, or the xlsx workbook (`Ranked_Disclosed` sheet).
- Filter by `Sector` (Fintech, SaaS, Marketplace, Logistics, Healthtech, Edtech, Agritech, AI, Other Tech).
- Sort or filter `Ease_to_Replicate` if you care about what a small team could actually build vs what needs a banking licence and float.
- Always click through `Source_URLs` before making a commercial decision. Numbers drift after every round.

## Rebuild

```bash
python3 -m venv .venv && .venv/bin/pip install openpyxl
# data lives in data/companies_part*.json; merge via:
.venv/bin/python -c "print('see commit history for build snippet')"
```

## Licence

MIT for the compilation and documentation in this repository. Underlying company trademarks belong to their owners. Source articles remain under their publishers' terms.

## Disclaimer

Not investment advice. Not legal advice. Licence capital figures can change when CBN/SEC/NAICOM update circulars - check the regulator pages before you rely on them.
