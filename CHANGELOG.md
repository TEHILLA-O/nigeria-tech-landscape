# Changelog

All notable dataset enrichments for nigeria-tech-landscape.

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
