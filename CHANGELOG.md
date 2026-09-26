# Changelog

## 2026-09-26 - High-ROI: Omnific Hand shortlist + LinkedIn fill + profile link

### Sell_to shortlist
- Added `data/omnific_hand_shortlist.csv` (**43** rows): Ranked where `Omnific_Hand_Motion` is Sell_to, Adjacent_tooling, or Partner (Clone_avoid excluded).
- New column `Outreach_One_Liner` (one natural sentence; no em/en dashes; edit before sending).
- Sheet `Omnific_Hand_Shortlist` in xlsx; sqlite table `omnific_hand_shortlist`.
- Guide: `docs/omnific_hand_shortlist.md`. Linked from README.

### Founder LinkedIn
- Before: **13/101** with `Founder_LinkedIn_URLs`.
- After: **40/101** (public founder profiles only; stopped rather than invent). Promoted verified `/in/` URLs already cited in Source_URLs plus fresh public lookups.

### Profile
- TEHILLA-O profile README blurb linking this repo (separate commit on `TEHILLA-O/TEHILLA-O`).
- Pin: profile already has **6/6** pinned repos; see report for manual pin steps (do not silently drop a featured pin).

### Rebuild
- Regenerated sqlite, xlsx, companies_enriched / ranked_enrichment LinkedIn fields, dashboard RANKED blob. No invented funding.

## 2026-09-25 - Facelift backlog items 3-10

### 3. Directory quality pass
- Removed **4** parse-junk rows (concatenated FCCPC app lists, address-as-company IMTO artefact). Details in `raw_sources/deep_research/directory_quality_pass.json`.
- Retagged FCCPC digital money lender rows (`Regulator_Source=FCCPC`, category Digital Money Lender) and CBN-licensed blurbs where Product_Summary stated so.
- Thickened ultra-thin blurbs with honest low-confidence listings (no invented products/funding).
- Directory Topics added where easy. Directory rows now **977** (was 981).

### 4. Stale-signal hygiene
- Added Ranked `Possibly_stale` (Yes/No/Unknown). Rule: Last_Signal_Date older than 18 months before **2026-09-25** => Yes; missing => Unknown. Documented in `docs/methodology.md`.
- Counts: Yes 30, No 2, Unknown 69.

### 5. Dashboard polish
- `docs/dashboard/index.html`: filters for Omnific_Hand_Motion, Sector_Primary, Company_Status, Exit_Type, Possibly_stale; **CSV export** of filtered view; reset control.

### 6. Founder LinkedIn fill-rate
- Before: **0/101** with Founder_LinkedIn_URLs.
- After: **13/101** (public profiles only; never invented).

### 7. Licence register re-check
- Set `Register_Last_Checked=2026-09-25` on **30** regulated / watchlist ranked names; refreshed Licence_Status where public claims allow. Refresh steps in `docs/licences.md`.

### 8. Conflict log
- Added `docs/Funding_Caveats.md` and `data/funding_caveats.csv` (Moove equity vs facility blending; Moniepoint Series C closes; Interswitch Visa stake).

### 9. Topics/tags
- Added Ranked `Topics` (semicolon tags). Extended Directory Topics where easy.

### 10. CONTRIBUTING
- Added **Good first issues** with concrete honest tasks.

### Rebuild
- Regenerated sqlite, xlsx, companies_enriched.json, dashboard. No invented funding.

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
