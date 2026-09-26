# Slack export / digest (example)

Optional weekly digest of ranked movers for personal research. **Never** send unsolicited Slack messages. Only post when the user explicitly asks and `SLACK_BOT_TOKEN` + `SLACK_CHANNEL_ID` are set locally.

## Example message shape

```
Nigeria tech landscape digest
- Ranked rows: 102
- New exits / status changes this week: ...
- Link: GitHub repo README + docs/dashboard/index.html
```

## Example flow

```bash
export SLACK_BOT_TOKEN=xoxb-...
export SLACK_CHANNEL_ID=C...
# future: python scripts/slack_export.py --summary --dry-run
```

Use `--dry-run` by default. A declined or blocked send must not be retried through another channel.
