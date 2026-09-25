# Paid data imports (Crunchbase / Tracxn)

## Status: BLOCKED without paid export

This folder is the sanctioned place to drop vendor CSVs. The public research dataset does **not** scrape Crunchbase or Tracxn paywalls and does **not** invent fills from locked pages.

## Expected files

| File | Purpose |
|---|---|
| `crunchbase_import.csv` | Optional paid Crunchbase export mapped to our schema |
| `tracxn_import.csv` | Optional paid Tracxn export (same column contract) |

Empty schema templates live beside this README. After the user drops a real export:

1. Keep originals under `data/imports/raw/` (gitignored if sensitive).
2. Map columns via a future `scripts/merge_vendor_export.py` (not required yet).
3. Prefer vendor rows only when they include a Source_URL or export provenance note.
4. Never overwrite a High-confidence public field with an unsourced vendor guess.

## What the user still needs to provide

- A licensed Crunchbase or Tracxn CSV/JSON export for the Ranked 102 (or the full Directory).
- Confirmation that redistribution into this open repo is allowed under the vendor licence (often it is **not**; in that case keep imports local/private).
