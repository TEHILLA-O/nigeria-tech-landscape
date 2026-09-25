# Changelog

## 2026-09-25 - LemFi dedupe + ranked blank chase

### LemFi / Lemonade Finance
- Removed **Lemonade Finance** from Ranked (was Rank 28, Pivoted). Same entity as **LemFi** after the May 2023 rebrand ([Disrupt Africa](https://disruptafrica.com/2023/05/31/nigerias-lemonade-finance-rebrands-to-lemfi-as-it-expands-vision/); [TechCabal](https://techcabal.com/2023/05/29/from-lemonade-finance-to-lemfi-international-payments-for-everyone/)).
- Canonical ranked row: **LemFi** (Rank 13). Funding **not** double-counted — kept LemFi `Total_Disclosed_Funding_USD=$85,000,000`; retired Lemonade's overlapping `$32,700,000` ranked total.
- Corrected LemFi founders/CEO to **Ridwan Olalere; Rian Cochran** (YC / company / press). Prior "Ridwan Bello; Rian Bello" treated as bad alias data.
- Reattributed YC pre-seed (`$725k`, 2021-11) from Lemonade Finance → LemFi in `funding_rounds.csv` with same-entity note.
- Added **Lemonade Finance** Directory alias (no funding) pointing at LemFi. Documented in `Replicate_Notes` + enrichment `Research_Notes`.
- Ranks rebuilt for **101** disclosed rows.

### Ranked website / founders fills (verified public sources only)
Websites (and founders where also blank or expanded):
- Aladdin Digital Bank: `https://www.aladdin.ng` — founders: Darlington Onyeagoro; Avi Umukoro
- Vesti: `https://wevesti.com` — founders: Olusola Amusan; Abimbola Amusan
- Payday: `https://www.usepayday.com` — founders: Favour Ori
- Agriarche: `https://agriarche.com` — founders: Deina Mayaki; Nancy Chinemerem Nwaka
- Carbin Africa: `https://carbin.africa` — founders: Femi Oriowo; Fawaz Abdul
- Earthbond: `https://www.earthbond.co` — founders: Chidalu Onyenso
- Zebra CropBank: `https://zebracropbank.com` — founders: Buffy Okeke-Ojiudu
- Mira: `https://usemira.com` — founders: Ted Oladele
- Trade Lenda: `https://tradelenda.com` — founders: Adeshina Adewumi; Shina Arogundade; Oluwatosin Ayodele

Founders-only fills:
- Tomato Jos: Mira Mehta
- Odyssey Energy Solutions: Emily McAteer; Piyush Mathur
- Nithio: Bobby Pittman; Queen Chinyere Quinn; Kate Steel
- Duplo: Yele Oyekola; Tunde Akinnuwa
- Intron Health: Tobi Olatunji; Olakunle Asekun
- Bundle Africa: Yele Bademosi

- **PalmPay** founders left blank — Transsnet/Transsion-backed; no clean public founder slate (exec names ≠ founders). Note in enrichment / progress.

### Coverage (Ranked)
- Website: **101/101** (100%)
- Founders: **100/101** (99%)
- Directory rows: **981**; unique companies **1082** (Lemonade moved Ranked→Directory).


## 2026-09-25 - Status/exit + Omnific Hand sell-vs-clone (interim)

### Added (Ranked_Disclosed, all 102 rows)
- `Exit_Type`, `Acquirer`, `Exit_Year`, `Exit_Source_URL`
- `Omnific_Hand_Motion` (`Sell_to` / `Partner` / `Adjacent_tooling` / `Clone_avoid`)
- `Omnific_Hand_Rationale` (1-2 sentences for Omnific Hand / small London ML-automation consultancy)

### Refined
- `Company_Status` vocabulary: Active / Acquired / Merged / Shutdown / Pivoted / Unknown
- Sourced exits: Jumia IPO; Paystack→Stripe; Brass→Paystack-led consortium; Mono→Flutterwave; Okra shutdown; 54gene wind-down; Bundle Africa exchange shutdown; Lemonade Finance→LemFi rebrand (Pivoted, not an exit)

### Docs
- `docs/data_dictionary.md` updated for new columns
- README enrichment coverage table + status/Omnific notes

### Policy
- Prefer blank / `None` over inventing exits, acquirers, or years
- Deep-research pass and Facelift backlog items 1-18 continue after this interim ship
\n