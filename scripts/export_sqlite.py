#!/usr/bin/env python3
"""Rebuild data/nigeria_tech_landscape.sqlite from CSV tables."""
from pathlib import Path
import csv, sqlite3

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "nigeria_tech_landscape.sqlite"

def load(conn, table, path):
    rows = list(csv.DictReader(path.open(encoding="utf-8")) )
    if not rows:
        return 0
    cols = list(rows[0].keys())
    cur = conn.cursor()
    cur.execute(f'DROP TABLE IF EXISTS "{table}"')
    cur.execute('CREATE TABLE "{}" ({})'.format(table, ", ".join(f'"{c}" TEXT' for c in cols)))
    cur.executemany(
        'INSERT INTO "{}" VALUES ({})'.format(table, ",".join("?" for _ in cols)),
        [[r.get(c, "") for c in cols] for r in rows],
    )
    return len(rows)

def main():
    if OUT.exists():
        OUT.unlink()
    conn = sqlite3.connect(OUT)
    n1 = load(conn, "ranked", DATA / "ranked_disclosed.csv")
    n2 = load(conn, "directory", DATA / "directory.csv")
    n3 = load(conn, "rounds", DATA / "funding_rounds.csv")
    n4 = load(conn, "investors", DATA / "investors.csv")
    conn.commit(); conn.close()
    print(f"wrote {OUT} ranked={n1} directory={n2} rounds={n3} investors={n4}")

if __name__ == "__main__":
    main()
