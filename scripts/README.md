# Scripts

| Script | Purpose |
|---|---|
| `enrich_and_rebuild.py` | Main enricher: merges `ranked_enrichment.json`, cleans Directory junk, applies category heuristics, builds investors/funding_rounds, JSON, xlsx, `build_meta.json` |
| `expand_build.py` | Earlier builder that expands licence lists + curated seeds into CSVs/xlsx |
| `rebuild.py` | Thin wrapper / legacy helper |
| `export_sqlite.py` | Rebuild `data/nigeria_tech_landscape.sqlite` from CSVs |
| `facelift_backlog_3_10.py` | Prior facelift batch (stale flags, LinkedIn map, dashboard) |

## Usual rebuild

```bash
cd /path/to/nigeriatechlandscape
python3 -m venv .venv
.venv/bin/pip install openpyxl pandas
.venv/bin/python scripts/enrich_and_rebuild.py
```

Optional: refresh HTML under `raw_sources/` from CBN/FCCPC before expand/enrich.

## Enrichment input

Deep Ranked fields live in `data/ranked_enrichment.json` (keyed by exact Company name). Edit there for researched facts, then rebuild.
