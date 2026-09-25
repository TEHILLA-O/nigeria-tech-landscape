# Notion sync (example)

This dataset can be mirrored into Notion for Omnific Hand ops. **Do not** require live Notion tokens in CI. Sync only when `NOTION_TOKEN` and `NOTION_DATABASE_ID` are present in the local environment and the user asked for a sync.

## Suggested mapping

| CSV column | Notion property |
|---|---|
| Company | Title |
| Rank | Number |
| Sector_Primary | Select |
| Total_Disclosed_Funding_USD | Number |
| Company_Status | Select |
| Exit_Type | Select |
| Omnific_Hand_Motion | Select |
| Website | URL |
| Omnific_Hand_Rationale | Rich text |
| Source_URLs | Rich text |

## Example flow

```bash
export NOTION_TOKEN=secret_...
export NOTION_DATABASE_ID=...
# future: python scripts/notion_sync.py --file data/ranked_disclosed.csv --dry-run
```

Until `notion_sync.py` exists, import the CSV manually via Notion CSV import or Make/Zapier.
