# Funding caveats and conflict log

Last verified: **2026-09-25**.

This log records **disputed or easy-to-misread funding totals** in the ranked sheet. Prefer primary sources. We do not invent totals to "resolve" conflicts.

## How to read a conflict

1. Check `Total_Disclosed_Funding_USD` on Ranked (ranking key).
2. Read `Replicate_Notes` / risk flags on the row.
3. Compare `data/funding_rounds.csv` line items.
4. Click every `Source_URLs` entry before using a figure commercially.

## Moove (Rank 4): equity vs debt / facility blending

| Field | Value / note |
|---|---|
| Ranked total used | **$445,000,000** |
| Why contested | Press roundups often blend **equity + vehicle financing facilities + debt**. Cumulative "raised" figures from listicles (e.g. LN247 Aug 2023 ~$335M cumulative; 2024 follow-on headlines ~$100-110M) may **overlap** or mix instrument types. |
| Ranked construction | Sheet note: LN247 Aug 2023 cumulative (~$335M) plus 2024 disclosed ~$110M; **verify overlap before relying**. |
| Sourced rounds in-repo | Series A $10M (2021, TechCrunch); Series B $105M (2022, TechCrunch); plus a press-cumulative latest-round stub. |
| Sources | https://techcrunch.com/2021/06/09/africas-moove-raises-10m-to-finance-ride-hailing-drivers/ ; https://techcrunch.com/2022/03/02/moove-raises-105m-to-finance-drivers-for-uber-and-bolt-in-africa-and-beyond/ ; https://ln247.news/top-10-most-funded-nigerian-startups-as-of-august-2023/ ; https://nairametrics.com/2025/02/25/top-10-nigerian-startups-by-funds-raised-in-2024/ |
| Disposition | Keep $445M as the **defended ranking floor** with Med confidence; treat as **upper-bound blended** until a company primary cumulative equity figure is published. |

Also tracked as CSV: `data/funding_caveats.csv`.

## Other watch rows (non-exhaustive)

| Company | Issue | Guidance |
|---|---|---|
| Moniepoint (TeamApt) | Series C first close (2024) vs completion (2025) | Use defended cumulative; cite company blog for latest close. |
| VertoFX / Grey / Fincra | Free lists under-report or highlight grants | Treat small cells as floors when Notes say so. |
| Bundle Africa | Exchange shutdown 2023 | Historical funding only; status Shutdown. |
| 54gene / Okra | Wind-down / shutdown | Funding is historical; not an operating raise signal. |
| Interswitch | Visa stake often cited ~$200M | Secondary / stake economics differ from primary equity raise. |

## Policy

- Never invent a "reconciled" total without a public source.
- When sources conflict, keep the defended rank total, document the conflict here, and leave Notes honest.
- Debt, revenue-based facilities, and equity must not be silently summed without a caveat.
