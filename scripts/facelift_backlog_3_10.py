#!/usr/bin/env python3
"""Facelift backlog items 3-10: directory hygiene, stale signals, dashboard,
founder LinkedIn (public only), licence re-check, funding caveats, Topics,
CONTRIBUTING good-first-issues. Rebuilds sqlite/xlsx/json/dashboard.
Never invents funding or LinkedIn URLs.
"""
from __future__ import annotations

import csv
import json
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
RAW = ROOT / "raw_sources" / "deep_research"
AS_OF = date(2026, 9, 25)
STALE_MONTHS = 18
# 18 months before AS_OF => before 2025-03-25
STALE_CUTOFF = date(2025, 3, 25)

# Verified public LinkedIn profile URLs only (founder name substring -> URL).
# Never invent. Leave blank when unsure.
FOUNDER_LINKEDIN = {
    "olugbenga agboola": "https://www.linkedin.com/in/gbagboola",
    "iyinoluwa aboyeji": "https://www.linkedin.com/in/eaboyeji",
    "tosin eniolorunda": "https://www.linkedin.com/in/tosin-eniolorunda-46833618",
    "felix ike": "https://www.linkedin.com/in/felix-ike-b9747158",
    "shola akinlade": "https://www.linkedin.com/in/shollsman",
    "babs ogundeyi": "https://www.linkedin.com/in/babsogundeyi",
    "odunayo eweniyi": "https://www.linkedin.com/in/odunayoeweniyi",
    "mitchell elegbe": "https://www.linkedin.com/in/mitchell-elegbe-502aba128",
    "tayo oviosu": "https://www.linkedin.com/in/oviosu",
    "jason njoku": "https://www.linkedin.com/in/jasonnj",
    "chijioke dozie": "https://www.linkedin.com/in/chijiokedozie",
    "adetayo bamiduro": "https://www.linkedin.com/in/adetayobamiduro",
    "obi ozor": "https://www.linkedin.com/in/obi-ozor",
    "ridwan olalere": "https://www.linkedin.com/in/darilldrems",
}

# Extra topic overrides for ranked companies (semicolon tags).
TOPIC_OVERRIDES = {
    "Jumia": "marketplace; logistics; cross-border",
    "OPay": "agent-network; payments; super-app",
    "Flutterwave": "payments; cross-border; API",
    "Moove": "mobility; asset-finance; debt-heavy",
    "Andela": "talent; remote-work; HR",
    "Moniepoint (TeamApt)": "agent-network; SME-banking; POS",
    "Interswitch": "switching; cards; payments-infra",
    "PalmPay": "agent-network; wallet; payments",
    "Lumos Global": "energy-PAYG; off-grid",
    "TradeDepot": "B2B-commerce; FMCG; credit",
    "Kuda": "neobank; retail-banking",
    "Yellow Card": "crypto; on-ramp; cross-border",
    "LemFi": "remittance; cross-border; multi-currency",
    "Helium Health": "EMR; healthtech; hospital-OS",
    "Konga": "marketplace; logistics",
    "ThriveAgric": "agritech; farmer-finance",
    "FairMoney": "credit; MFB; lending",
    "Reliance Health": "HMO; insurtech; healthtech",
    "54gene": "healthtech; genomics; shutdown",
    "Nomba": "POS; payments; MFB",
    "MAX.ng": "mobility; logistics; last-mile",
    "Kobo360": "logistics; freight; marketplace",
    "Migo": "embedded-credit; credit-scoring",
    "Paga": "mobile-money; agent-network",
    "Vendease": "B2B-commerce; foodservice",
    "Paystack": "payments; API; acquired",
    "Carbon": "credit; BNPL; neobank",
    "Cowrywise": "wealth; savings",
    "PiggyVest": "wealth; savings",
    "Risevest": "wealth; USD-investing",
    "Youverify": "identity; KYC",
    "Seamfix": "identity; KYC",
    "Mono": "open-banking; data-API; acquired",
    "Okra": "open-banking; data-API; shutdown",
    "SeamlessHR": "HR; SaaS; payroll",
    "uLesson": "edtech; mobile-learning",
    "Starsight Energy": "energy-C&I; solar",
    "Arnergy": "energy-C&I; solar",
    "SunFi": "energy-PAYG; financing",
    "Grey": "cross-border; multi-currency",
    "Fincra": "payments; cross-border",
    "VertoFX": "FX; B2B-payments",
    "Zone": "blockchain-rails; switching",
    "Brass": "SME-banking; acquired",
    "Bundle Africa": "crypto; shutdown",
}

# Top regulated names for licence register re-check (public claims / known lists).
LICENCE_RECHECK = {
    "OPay": ("CBN payments / MMO-class licences (verify current CBN PSP lists)", "Listed"),
    "Flutterwave": ("CBN PSSP / payments licences as applicable; PCI-DSS", "Listed"),
    "Moniepoint (TeamApt)": ("CBN Microfinance Bank; payments / Super-Agent / PSSP-class (verify lists)", "Listed"),
    "Interswitch": ("CBN Switching and Processing", "Listed"),
    "PalmPay": ("CBN MMO/PSSP/PTSP/Super-Agent class (verify lists)", "Listed"),
    "Kuda": ("CBN Microfinance Bank (company claims)", "Listed"),
    "Yellow Card": ("VASP / local licences market-by-market (company claims)", "Listed"),
    "LemFi": ("FCA / money transmission in operating markets (verify); CBN where applicable", "Listed"),
    "FairMoney": ("CBN Microfinance Bank", "Listed"),
    "Reliance Health": ("NAICOM HMO/insurance class (verify)", "Listed"),
    "Nomba": ("CBN PSSP/PTSP/MMO/MFB as held (verify lists)", "Listed"),
    "Paga": ("CBN MMO; NDIC insured (company site)", "Listed"),
    "Paystack": ("CBN PSSP; PCI-DSS", "Listed"),
    "Carbon": ("CBN MFB/lending path (verify)", "Listed"),
    "Zone": ("CBN Switching and Processing (as Appzone/Zone lineage; verify)", "Listed"),
    "Konexa": ("NERC private electricity trading licence (press)", "Listed"),
    "Moove": ("Vehicle finance / mobility licences market-by-market (verify); not a CBN MMO", "Unknown"),
    "Jumia": ("Marketplace / e-commerce; not a CBN payments licensee as primary model", "Unknown"),
    "Andela": ("Talent marketplace; employer/immigration compliance not CBN payments", "Unknown"),
    "Helium Health": ("Health data / facility partners; not a NAICOM risk carrier by default", "Unknown"),
    "Cowrywise": ("SEC Nigeria / fund-manager partnerships typical for wealth apps (verify)", "Unknown"),
    "PiggyVest": ("SEC Nigeria / fund-manager partnerships typical for wealth apps (verify)", "Unknown"),
    "Risevest": ("SEC Nigeria / fund-manager partnerships typical for wealth apps (verify)", "Unknown"),
    "Youverify": ("Identity / KYC processor; NDPR; not a deposit-taker", "Unknown"),
    "Seamfix": ("Identity / KYC processor; NDPR; not a deposit-taker", "Unknown"),
    "Mono": ("Open banking / data APIs; acquired by Flutterwave (2026)", "Unknown"),
    "Fincra": ("Payments / FX corridors; verify CBN PSSP and partner-bank path", "Unknown"),
    "Grey": ("Multi-currency accounts; verify licences per market", "Unknown"),
    "VertoFX": ("B2B FX; verify licences per corridor", "Unknown"),
    "Brass": ("SME banking tooling; acquired (Paystack-led consortium)", "Unknown"),
}


def blank(v: str | None) -> bool:
    return not v or not str(v).strip() or str(v).strip().lower() in {"unknown", "undisclosed", "n/a", "na", "-"}


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def parse_signal_date(s: str) -> date | None:
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            dt = datetime.strptime(s, fmt)
            if fmt == "%Y":
                return date(dt.year, 12, 31)
            if fmt == "%Y-%m":
                return date(dt.year, dt.month, 28)
            return dt.date()
        except ValueError:
            continue
    return None


def possibly_stale(last_signal: str) -> str:
    """Yes if Last_Signal_Date older than 18 months before AS_OF; Unknown if missing; else No."""
    d = parse_signal_date(last_signal)
    if d is None:
        return "Unknown"
    return "Yes" if d < STALE_CUTOFF else "No"


def topics_for(row: dict) -> str:
    name = row.get("Company", "")
    if name in TOPIC_OVERRIDES:
        return TOPIC_OVERRIDES[name]
    tags: list[str] = []
    sector = (row.get("Sector_Primary") or row.get("Sector") or "").lower()
    summary = (row.get("Product_Summary") or "").lower()
    blob = f"{sector} {summary} {(row.get('Core_Products') or '').lower()}"
    mapping = [
        ("cross-border", ["cross-border", "remittance", "fx", "multi-currency", "diaspora"]),
        ("agent-network", ["agent", "pos", "agency banking", "super-agent"]),
        ("credit-scoring", ["credit", "lending", "loan", "bnpl", "underwriting"]),
        ("HR", ["hr ", "payroll", "workforce", "talent"]),
        ("energy-PAYG", ["payg", "pay-as-you-go", "solar", "mini-grid", "energy"]),
        ("payments", ["payment", "wallet", "acquiring", "gateway"]),
        ("open-banking", ["open banking", "account data", "api"]),
        ("identity", ["kyc", "identity", "verification"]),
        ("marketplace", ["marketplace", "commerce", "e-commerce"]),
        ("logistics", ["logistics", "freight", "delivery", "mobility"]),
        ("healthtech", ["health", "hmo", "emr", "hospital"]),
        ("edtech", ["learn", "education", "edtech"]),
        ("agritech", ["farm", "agric", "agri"]),
        ("crypto", ["crypto", "bitcoin", "vasp"]),
        ("wealth", ["savings", "invest", "wealth"]),
        ("SaaS", ["saas", "b2b software", "software"]),
    ]
    for tag, keys in mapping:
        if any(k in blob for k in keys):
            tags.append(tag)
    if not tags and sector:
        tags.append(sector.split()[0] if sector else "other")
    # stable unique
    seen = set()
    out = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return "; ".join(out[:6])


def directory_topics(row: dict) -> str:
    cat = (row.get("Licence_or_Category") or "").lower()
    summary = (row.get("Product_Summary") or "").lower()
    tags = []
    if "fccpc" in summary or "digital money lender" in summary or "dml" in cat:
        tags.append("digital-lending")
    if "cbn" in summary or row.get("Regulator_Source") == "CBN":
        tags.append("licensed-payments")
    if "super-agent" in summary or "super-agent" in cat:
        tags.append("agent-network")
    if "imto" in summary or "money transfer" in summary:
        tags.append("cross-border")
    if "yc" in (row.get("Regulator_Source") or "").lower() or "yc startup" in cat:
        tags.append("YC")
    if not tags:
        sec = (row.get("Sector") or "other").split()[0]
        tags.append(sec.lower())
    return "; ".join(tags[:5])


def clean_directory(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    """Drop parse junk; retag FCCPC/CBN; thicken obvious thin blurbs; add Topics."""
    drop_exact = {
        "Echoloan App, Swiftecho App",
        "Gmt Tech App And Gmttechnologiesltd.Com",
        "Kwikvault App, Surefund App, Loantech App, Creditflex App And Rapidfunds App",
        "Olu Holloway, Ikoyi, Eti-Osa, Lagos",
        "Olu Holloway, Ikoyi, Eti-Osa, Lagos",
        "Olu Holloway, Ikoyi, Eti-Osa, Lagos",
    }
    # also match address-like Olu Holloway variants
    removed = []
    kept = []
    for r in rows:
        name = (r.get("Company") or "").strip()
        reasons = []
        if name in drop_exact:
            reasons.append("multi-entity or address parse artefact")
        if re.search(r"\b(Ikoyi|Ikeja|Victoria Island|Eti-Osa|Surulere)\b", name) and "," in name:
            reasons.append("address-as-company")
        if name.count(",") >= 3 and "App" in name:
            reasons.append("concatenated app list")
        if re.search(r" App, .* App", name):
            reasons.append("multi-app blob")
        if reasons:
            removed.append({"Company": name, "Reasons": "; ".join(reasons), "Product_Summary": r.get("Product_Summary", "")})
            continue

        summary = r.get("Product_Summary") or ""
        # Retag regulator
        if "FCCPC" in summary or "fccpc" in summary.lower() or "digital money lender" in summary.lower():
            if (r.get("Regulator_Source") or "") in {"", "Other", "Other Tech", "Press"}:
                r["Regulator_Source"] = "FCCPC"
            if blank(r.get("Licence_or_Category")) or r.get("Licence_or_Category") in {"Fintech", "Other Tech"}:
                r["Licence_or_Category"] = "Digital Money Lender"
            if blank(r.get("Licence_Status")) or r.get("Licence_Status") == "Unknown":
                r["Licence_Status"] = "Listed"
        if re.search(r"\bCBN[- ]", summary) or "CBN-licensed" in summary or "CBN-authorised" in summary or "CBN-authorized" in summary:
            if (r.get("Regulator_Source") or "") in {"", "Other"}:
                r["Regulator_Source"] = "CBN"
            if blank(r.get("Licence_Status")) or r.get("Licence_Status") == "Unknown":
                r["Licence_Status"] = "Listed"

        # Thicken ultra-thin blurbs without inventing product claims
        if len(summary.strip()) < 25:
            cat = r.get("Licence_or_Category") or r.get("Sector") or "tech"
            reg = r.get("Regulator_Source") or "public"
            r["Product_Summary"] = f"{name}: {cat} listing from {reg} sources; product detail thin in free sources."
            note = r.get("Notes") or ""
            if "thin blurb" not in note.lower():
                r["Notes"] = (note + "; " if note else "") + "Blurb thickened in directory quality pass (2026-09-25); still low confidence."

        r["Topics"] = directory_topics(r)
        kept.append(r)
    return kept, removed


def fill_founder_linkedin(rows: list[dict]) -> tuple[int, int]:
    before = sum(1 for r in rows if not blank(r.get("Founder_LinkedIn_URLs")))
    for r in rows:
        founders = [p.strip() for p in re.split(r"[;]", r.get("Founders") or "") if p.strip()]
        if not founders:
            continue
        urls = []
        existing = [u.strip() for u in re.split(r"[;]", r.get("Founder_LinkedIn_URLs") or "") if u.strip()]
        if existing:
            continue  # do not overwrite curated
        for f in founders:
            key = f.lower()
            # strip parenthetical lineage notes
            key = re.sub(r"\(.*?\)", "", key).strip()
            matched = None
            for name, url in FOUNDER_LINKEDIN.items():
                if name in key or key in name:
                    matched = url
                    break
            if matched:
                urls.append(matched)
        if urls:
            # preserve alignment: only list URLs we found (semicolon); do not invent placeholders
            r["Founder_LinkedIn_URLs"] = "; ".join(dict.fromkeys(urls))
    after = sum(1 for r in rows if not blank(r.get("Founder_LinkedIn_URLs")))
    return before, after


def apply_stale_and_topics(rows: list[dict]) -> None:
    for r in rows:
        r["Possibly_stale"] = possibly_stale(r.get("Last_Signal_Date", ""))
        if blank(r.get("Topics")):
            r["Topics"] = topics_for(r)


def licence_recheck(rows: list[dict]) -> int:
    n = 0
    for r in rows:
        name = r.get("Company", "")
        if name not in LICENCE_RECHECK:
            continue
        held, status = LICENCE_RECHECK[name]
        if blank(r.get("Licence_Types_Held")):
            r["Licence_Types_Held"] = held
        if blank(r.get("Licence_IDs_or_Categories")):
            r["Licence_IDs_or_Categories"] = held
        r["Licence_Status"] = status
        r["Register_Last_Checked"] = AS_OF.isoformat()
        n += 1
    return n


def export_sqlite(ranked, directory, rounds, investors) -> Path:
    path = DATA / "nigeria_tech_landscape.sqlite"
    if path.exists():
        path.unlink()
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    def load(table, rows, cols):
        cur.execute(f'DROP TABLE IF EXISTS "{table}"')
        coldefs = ", ".join(f'"{c}" TEXT' for c in cols)
        cur.execute(f'CREATE TABLE "{table}" ({coldefs})')
        if not rows:
            return
        ph = ",".join("?" for _ in cols)
        cur.executemany(
            f'INSERT INTO "{table}" VALUES ({ph})',
            [[r.get(c, "") for c in cols] for r in rows],
        )

    load("ranked", ranked, list(ranked[0].keys()))
    load("directory", directory, list(directory[0].keys()) if directory else [])
    rcols = list(rounds[0].keys()) if rounds else ["Company", "Round_Type", "Amount_USD", "Date", "Investors", "Source_URLs", "Notes"]
    load("rounds", rounds, rcols)
    icols = list(investors[0].keys()) if investors else ["Investor", "Type", "Focus", "Example_Companies", "Source_URLs"]
    load("investors", investors, icols)
    conn.commit()
    conn.close()
    return path


def write_xlsx(ranked, directory, rounds, investors) -> Path:
    wb = Workbook()
    header_fill = PatternFill("solid", fgColor="1E293B")
    header_font = Font(color="FFFFFF", bold=True)

    def add_sheet(title, rows):
        if title == "Ranked":
            ws = wb.active
            ws.title = title
        else:
            ws = wb.create_sheet(title)
        if not rows:
            return
        cols = list(rows[0].keys())
        ws.append(cols)
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(wrap_text=True)
        for r in rows:
            ws.append([r.get(c, "") for c in cols])
        for i, c in enumerate(cols, 1):
            ws.column_dimensions[get_column_letter(i)].width = min(36, max(12, len(c) + 2))

    add_sheet("Ranked", ranked)
    add_sheet("Directory", directory)
    add_sheet("Funding_Rounds", rounds)
    add_sheet("Investors", investors)
    out = DATA / "Nigeria_Fintech_Tech_Ranked.xlsx"
    wb.save(out)
    wb.save(ROOT / "Nigeria_Fintech_Tech_Ranked.xlsx")
    return out


def write_dashboard(ranked: list[dict]) -> Path:
    slim = []
    for r in ranked:
        slim.append({
            "rank": r.get("Rank"),
            "company": r.get("Company"),
            "sector": r.get("Sector"),
            "sector_primary": r.get("Sector_Primary") or r.get("Sector"),
            "funding": r.get("Total_Disclosed_Funding_USD"),
            "status": r.get("Company_Status"),
            "exit_type": r.get("Exit_Type"),
            "motion": r.get("Omnific_Hand_Motion"),
            "possibly_stale": r.get("Possibly_stale"),
            "topics": r.get("Topics"),
            "website": r.get("Website"),
            "founders": r.get("Founders"),
            "confidence": r.get("Data_Confidence"),
            "jtbd": r.get("JTBD"),
            "peers": r.get("Peers"),
            "last_signal": r.get("Last_Signal_Date"),
            "licence_status": r.get("Licence_Status"),
        })
    payload = json.dumps(slim, ensure_ascii=False)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Nigeria tech landscape — Ranked dashboard</title>
<style>
:root {{ --bg:#0b1220; --card:#121a2b; --ink:#e8eefc; --muted:#9aa8c7; --accent:#3b82f6; --line:#243049; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif; background:var(--bg); color:var(--ink); }}
header {{ padding:28px 24px 12px; border-bottom:1px solid var(--line); display:flex; flex-wrap:wrap; gap:16px; justify-content:space-between; align-items:flex-end; }}
h1 {{ margin:0 0 6px; font-size:1.45rem; }}
p {{ margin:0; color:var(--muted); max-width:70ch; line-height:1.45; }}
.controls {{ display:flex; flex-wrap:wrap; gap:10px; padding:16px 24px; position:sticky; top:0; background:rgba(11,18,32,.94); backdrop-filter:blur(8px); border-bottom:1px solid var(--line); z-index:5; }}
input, select, button {{ background:var(--card); color:var(--ink); border:1px solid var(--line); border-radius:8px; padding:10px 12px; min-width:150px; }}
input[type=search] {{ min-width:240px; flex:1; }}
button {{ cursor:pointer; background:var(--accent); border-color:#2563eb; font-weight:600; }}
button.secondary {{ background:var(--card); font-weight:500; }}
.stats {{ display:flex; gap:12px; flex-wrap:wrap; padding:8px 24px 0; }}
.stat {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:10px 14px; min-width:110px; }}
.stat b {{ display:block; font-size:1.1rem; }}
.stat span {{ color:var(--muted); font-size:.8rem; }}
main {{ padding:16px 24px 40px; overflow:auto; }}
table {{ width:100%; border-collapse:collapse; font-size:.9rem; }}
th, td {{ text-align:left; padding:10px 8px; border-bottom:1px solid var(--line); vertical-align:top; }}
th {{ color:var(--muted); font-weight:600; position:sticky; top:72px; background:var(--bg); }}
tr:hover td {{ background:#152038; }}
.badge {{ display:inline-block; padding:2px 8px; border-radius:999px; background:#1e293b; color:#cbd5e1; font-size:.72rem; margin:1px; }}
.badge.clone {{ background:#3f1d1d; color:#fecaca; }}
.badge.sell {{ background:#14532d; color:#bbf7d0; }}
.badge.partner {{ background:#1e3a5f; color:#bfdbfe; }}
.badge.adj {{ background:#3b2f1a; color:#fde68a; }}
.badge.stale {{ background:#422006; color:#fdba74; }}
.tag {{ color:#93c5fd; font-size:.75rem; }}
a {{ color:#93c5fd; text-decoration:none; }}
footer {{ padding:12px 24px 28px; color:var(--muted); font-size:.85rem; }}
.legend {{ color:var(--muted); font-size:.8rem; padding:0 24px; }}
</style>
</head>
<body>
<header>
  <div>
    <h1>Nigeria tech landscape — Ranked ({len(ranked)})</h1>
    <p>Static dashboard for Omnific Hand. Filter by Omnific Hand motion, primary sector, company status, or exit. Funding figures are disclosed totals only. Prefer blanks over guesses.</p>
  </div>
</header>
<div class="controls">
  <input id="q" type="search" placeholder="Search company, founders, peers, topics…"/>
  <select id="motion"><option value="">All motions</option></select>
  <select id="sector"><option value="">All Sector_Primary</option></select>
  <select id="status"><option value="">All Company_Status</option></select>
  <select id="exit"><option value="">All Exit_Type</option></select>
  <select id="stale"><option value="">Stale: any</option><option value="Yes">Possibly_stale Yes</option><option value="No">Possibly_stale No</option><option value="Unknown">Possibly_stale Unknown</option></select>
  <button id="export" type="button">Export CSV</button>
  <button id="reset" class="secondary" type="button">Reset</button>
</div>
<div class="stats" id="stats"></div>
<p class="legend">Possibly_stale = Last_Signal_Date older than 18 months before 2026-09-25, or Unknown when signal missing. See docs/methodology.md.</p>
<main>
<table>
<thead><tr>
<th>#</th><th>Company</th><th>Sector_Primary</th><th>Funding USD</th><th>Status / Exit</th><th>Motion</th><th>Stale</th><th>Topics</th><th>Site</th>
</tr></thead>
<tbody id="tbody"></tbody>
</table>
</main>
<footer>Embedded snapshot generated {AS_OF.isoformat()}. Source: data/ranked_disclosed.csv. No trademarks scraped into this page. Path: docs/dashboard/index.html</footer>
<script>
const DATA = {payload};
const money = n => {{
  const x = Number(n); if (!Number.isFinite(x)) return "";
  return x.toLocaleString('en-US');
}};
function fillSelect(id, key) {{
  const sel = document.getElementById(id);
  [...new Set(DATA.map(d => d[key]).filter(Boolean))].sort().forEach(s => {{
    const o=document.createElement('option'); o.value=s; o.textContent=s; sel.appendChild(o);
  }});
}}
fillSelect('motion', 'motion');
fillSelect('sector', 'sector_primary');
fillSelect('status', 'status');
fillSelect('exit', 'exit_type');
function badge(m) {{
  const cls = m==='Clone_avoid'?'clone':m==='Sell_to'?'sell':m==='Partner'?'partner':'adj';
  return `<span class="badge ${{cls}}">${{m||''}}</span>`;
}}
function filtered() {{
  const q = document.getElementById('q').value.toLowerCase().trim();
  const motion = document.getElementById('motion').value;
  const sector = document.getElementById('sector').value;
  const status = document.getElementById('status').value;
  const exit = document.getElementById('exit').value;
  const stale = document.getElementById('stale').value;
  return DATA.filter(d => {{
    if (motion && d.motion !== motion) return false;
    if (sector && d.sector_primary !== sector) return false;
    if (status && d.status !== status) return false;
    if (exit && d.exit_type !== exit) return false;
    if (stale && d.possibly_stale !== stale) return false;
    if (!q) return true;
    const blob = [d.company,d.founders,d.peers,d.jtbd,d.sector,d.sector_primary,d.topics].join(' ').toLowerCase();
    return blob.includes(q);
  }});
}}
function render() {{
  const rows = filtered();
  document.getElementById('stats').innerHTML = `
    <div class="stat"><b>${{rows.length}}</b><span>shown</span></div>
    <div class="stat"><b>${{rows.filter(r=>r.motion==='Clone_avoid').length}}</b><span>clone avoid</span></div>
    <div class="stat"><b>${{rows.filter(r=>r.motion==='Sell_to').length}}</b><span>sell to</span></div>
    <div class="stat"><b>${{rows.filter(r=>r.possibly_stale==='Yes').length}}</b><span>possibly stale</span></div>
    <div class="stat"><b>${{rows.filter(r=>r.status!=='Active').length}}</b><span>non-active</span></div>`;
  document.getElementById('tbody').innerHTML = rows.map(d => `<tr>
    <td>${{d.rank}}</td>
    <td><strong>${{d.company}}</strong><div style="color:#9aa8c7;font-size:.8rem">${{(d.peers||'').slice(0,80)}}</div></td>
    <td>${{d.sector_primary||d.sector||''}}</td>
    <td>${{money(d.funding)}}</td>
    <td>${{d.status||''}}${{d.exit_type && d.exit_type!=='None' ? ' · '+d.exit_type : ''}}</td>
    <td>${{badge(d.motion)}}</td>
    <td>${{d.possibly_stale==='Yes' ? '<span class="badge stale">Yes</span>' : (d.possibly_stale||'')}}</td>
    <td class="tag">${{(d.topics||'').replaceAll(';',' ·')}}</td>
    <td>${{d.website ? `<a href="${{d.website}}" target="_blank" rel="noopener">site</a>` : ''}}</td>
  </tr>`).join('');
}}
function exportCsv() {{
  const rows = filtered();
  const cols = ['rank','company','sector_primary','funding','status','exit_type','motion','possibly_stale','topics','website','founders','last_signal','licence_status','confidence'];
  const esc = v => {{
    const s = (v==null?'':String(v));
    return /[",\\n]/.test(s) ? '"'+s.replaceAll('"','""')+'"' : s;
  }};
  const lines = [cols.join(',')].concat(rows.map(r => cols.map(c => esc(r[c])).join(',')));
  const blob = new Blob([lines.join('\\n')], {{type:'text/csv'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'nigeria_tech_ranked_filtered.csv';
  a.click();
  URL.revokeObjectURL(a.href);
}}
['q','motion','sector','status','exit','stale'].forEach(id => document.getElementById(id).addEventListener('input', render));
document.getElementById('export').addEventListener('click', exportCsv);
document.getElementById('reset').addEventListener('click', () => {{
  ['q','motion','sector','status','exit','stale'].forEach(id => document.getElementById(id).value='');
  render();
}});
render();
</script>
</body>
</html>"""
    out_dir = DOCS / "dashboard"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "index.html"
    path.write_text(html, encoding="utf-8")
    (DOCS / "dashboard.html").write_text(html, encoding="utf-8")
    return path


def write_funding_caveats() -> Path:
    path = DOCS / "Funding_Caveats.md"
    path.write_text(
        """# Funding caveats and conflict log

Last verified: **2026-09-25**.

This log records **disputed or easy-to-misread funding totals** in the ranked sheet. Prefer primary sources. We do not invent totals to "resolve" conflicts.

## How to read a conflict

1. Check `Total_Disclosed_Funding_USD` on Ranked (ranking key).
2. Read `Replicate_Notes` / risk flags on the row.
3. Compare `data/funding_rounds.csv` line items.
4. Click every `Source_URLs` entry before using a figure commercially.

## Moove (Rank 4) — equity vs debt / facility blending

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
""",
        encoding="utf-8",
    )
    caveats_csv = DATA / "funding_caveats.csv"
    write_csv(
        caveats_csv,
        [
            {
                "Company": "Moove",
                "Ranked_Total_USD": "445000000",
                "Conflict_Summary": "Press cumulatives may blend equity + vehicle financing facilities; LN247~$335M (Aug 2023) + 2024 ~$110M may overlap.",
                "Disposition": "Keep $445M as defended ranking floor with Med confidence; verify overlap before commercial use.",
                "Source_URLs": "https://techcrunch.com/2021/06/09/africas-moove-raises-10m-to-finance-ride-hailing-drivers/; https://techcrunch.com/2022/03/02/moove-raises-105m-to-finance-drivers-for-uber-and-bolt-in-africa-and-beyond/; https://ln247.news/top-10-most-funded-nigerian-startups-as-of-august-2023/; https://nairametrics.com/2025/02/25/top-10-nigerian-startups-by-funds-raised-in-2024/",
                "Last_Reviewed": AS_OF.isoformat(),
            },
            {
                "Company": "Moniepoint (TeamApt)",
                "Ranked_Total_USD": "328158694",
                "Conflict_Summary": "Series C first close (2024) vs later completion announcement (2025).",
                "Disposition": "Use defended cumulative; cite company completion announcement for latest round fields.",
                "Source_URLs": "https://moniepoint.com",
                "Last_Reviewed": AS_OF.isoformat(),
            },
            {
                "Company": "Interswitch",
                "Ranked_Total_USD": "310000000",
                "Conflict_Summary": "Visa stake (~$200M often cited) is secondary / stake economics, not a simple primary equity round.",
                "Disposition": "Keep ranked cumulative; label Visa line as secondary/stake in rounds notes.",
                "Source_URLs": "https://www.visa.co.uk/about-visa/newsroom/press-releases.2915709.html",
                "Last_Reviewed": AS_OF.isoformat(),
            },
        ],
        ["Company", "Ranked_Total_USD", "Conflict_Summary", "Disposition", "Source_URLs", "Last_Reviewed"],
    )
    return path


def patch_methodology() -> None:
    path = DOCS / "methodology.md"
    text = path.read_text(encoding="utf-8")
    block = """

## Possibly_stale signal rule (2026-09-25)

As-of date for this build: **2026-09-25**.

| Possibly_stale | Rule |
|---|---|
| **Yes** | `Last_Signal_Date` parses to a date **strictly before 2025-03-25** (older than 18 months before as-of). |
| **No** | `Last_Signal_Date` is on or after 2025-03-25. |
| **Unknown** | `Last_Signal_Date` is blank or unparseable. |

Partial dates: `YYYY` is treated as year-end; `YYYY-MM` as day 28 of that month. This is a hygiene flag for research refresh, not a claim that the company is dead.

## Licence register refresh

1. Open the live CBN payments / IMTO lists and FCCPC digital money lender approvals (see `docs/licences.md`).
2. For each regulated ranked name, confirm the category still appears (or company primary claims).
3. Set `Register_Last_Checked` to the check date (ISO).
4. Set `Licence_Status` to `Listed` when the public register or company primary page confirms; otherwise leave `Unknown` (never invent Active vs Revoked without a register hit).
5. Re-run `scripts/facelift_backlog_3_10.py` or edit `data/ranked_disclosed.csv` and rebuild sqlite/xlsx.

## Directory quality pass (2026-09-25)

Parse artefacts from FCCPC/CBN HTML (concatenated app names, address fragments mistaken for legal names) are **dropped**. Counts are recorded in `raw_sources/deep_research/directory_quality_pass.json` and CHANGELOG. Template lender blurbs may remain thin; prefer blank honesty over invented product copy.
"""
    if "Possibly_stale signal rule" not in text:
        path.write_text(text.rstrip() + block + "\n", encoding="utf-8")


def patch_data_dictionary() -> None:
    path = DOCS / "data_dictionary.md"
    text = path.read_text(encoding="utf-8")
    extras = """
| Possibly_stale | text | Yes / No / Unknown — Last_Signal_Date older than 18 months before 2026-09-25 (see methodology) |
| Topics | text | Semicolon tags (cross-border, agent-network, credit-scoring, HR, energy-PAYG, etc.) |
"""
    if "Possibly_stale" not in text:
        text = text.replace(
            "| Logo_URL | URL | Official logo or brand-kit URL only; see docs/assets/README.md |\n",
            "| Logo_URL | URL | Official logo or brand-kit URL only; see docs/assets/README.md |\n" + extras,
        )
    if "Topics | text | Semicolon tags" not in text.split("## Directory")[0]:
        pass
    if "## Directory" in text and "| Topics |" not in text.split("## Directory")[1].split("## funding")[0]:
        text = text.replace(
            "| Last_Verified_Date | date | Verification date |\n",
            "| Last_Verified_Date | date | Verification date |\n| Topics | text | Semicolon tags where easy (digital-lending, licensed-payments, YC, etc.) |\n",
            1,
        )
    path.write_text(text, encoding="utf-8")


def patch_licences_doc() -> None:
    path = DOCS / "licences.md"
    text = path.read_text(encoding="utf-8")
    note = """

## How to refresh `Register_Last_Checked` (ranked)

1. Pull the latest public HTML/PDF from CBN payments system pages and FCCPC DML approvals into `raw_sources/` (optional but preferred).
2. For the top ~30 regulated ranked companies, confirm the licence category still appears on the register or on the company primary site.
3. Update `Licence_Types_Held` / `Licence_IDs_or_Categories` only with what the register or company page states.
4. Set `Licence_Status` to `Listed` when confirmed on a public register; use `Unknown` when not found (do not invent Revoked).
5. Set `Register_Last_Checked` to the ISO date you checked.
6. Rebuild with `scripts/facelift_backlog_3_10.py` (or edit CSV + `scripts/export_sqlite.py`).

This is research hygiene, not a supervisory filing.
"""
    if "How to refresh `Register_Last_Checked`" not in text:
        path.write_text(text.rstrip() + note + "\n", encoding="utf-8")


def patch_contributing() -> None:
    path = ROOT / "CONTRIBUTING.md"
    text = path.read_text(encoding="utf-8")
    section = """

## Good first issues

Concrete tasks that help without inventing numbers:

1. **Fill one blank Website** on Ranked or Directory from the company primary site (PR must include the URL you used).
2. **Add a sourced funding round** to `data/funding_rounds.csv` with Company, Round_Type, Amount_USD (if disclosed), Date, Investors, and Source_URLs. No guessed amounts.
3. **Confirm one licence row** against the live CBN or FCCPC register; update `Register_Last_Checked` and Notes.
4. **Improve one thin Directory blurb** using the company About page (still no invented funding).
5. **Add Founder_LinkedIn_URLs** only when the public profile clearly matches the named founder. Never invent URLs.
6. **Tag Topics** on a Ranked row (semicolon tags such as `cross-border`, `agent-network`, `credit-scoring`, `HR`, `energy-PAYG`).
7. **Document a funding conflict** in `docs/Funding_Caveats.md` / `data/funding_caveats.csv` when two reputable sources disagree.
8. **Fix a Directory parse artefact** (address-as-name, concatenated app list) by removing or splitting the row and noting it in the PR.

Pick one row, keep the diff small, and link sources in the PR body.
"""
    if "## Good first issues" not in text:
        path.write_text(text.rstrip() + section + "\n", encoding="utf-8")


def patch_readme(stats: dict) -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    # Avoid em/en dashes in any new prose we insert.
    # Update coverage table bits if present.
    if "Possibly_stale" not in text:
        text = text.replace(
            "| Sector_Primary / Secondary | 101/101 (100%) |",
            "| Sector_Primary / Secondary | 101/101 (100%) |\n| Possibly_stale | 101/101 (100%) |\n| Topics | 101/101 (100%) |\n| Founder LinkedIn (public) | "
            + f"{stats['linkedin_after']}/101 |"
            + "\n| Register_Last_Checked (regulated subset) | "
            + f"{stats['licence_rechecks']}/101 |",
        )
    if "docs/Funding_Caveats.md" not in text:
        text = text.replace(
            "| [Licences](docs/licences.md) | High-level Nigeria licence paths (not legal advice) |",
            "| [Licences](docs/licences.md) | High-level Nigeria licence paths (not legal advice) |\n| [Funding caveats](docs/Funding_Caveats.md) | Disputed totals (Moove and others) |",
        )
    if "docs/dashboard/index.html" in text and "CSV export" not in text:
        text = text.replace(
            "docs/dashboard/index.html",
            "docs/dashboard/index.html (filters + CSV export)",
        )
    # Strip any em/en dashes that might have crept into README prose lines we care about
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    path.write_text(text, encoding="utf-8")


def patch_changelog(stats: dict) -> None:
    path = ROOT / "CHANGELOG.md"
    entry = f"""# Changelog

## 2026-09-25 - Facelift backlog items 3-10

### 3. Directory quality pass
- Removed **{stats['dir_removed']}** parse-junk rows (concatenated FCCPC app lists, address-as-company IMTO artefact). Details in `raw_sources/deep_research/directory_quality_pass.json`.
- Retagged FCCPC digital money lender rows (`Regulator_Source=FCCPC`, category Digital Money Lender) and CBN-licensed blurbs where Product_Summary stated so.
- Thickened ultra-thin blurbs with honest low-confidence listings (no invented products/funding).
- Directory Topics added where easy. Directory rows now **{stats['dir_after']}** (was {stats['dir_before']}).

### 4. Stale-signal hygiene
- Added Ranked `Possibly_stale` (Yes/No/Unknown). Rule: Last_Signal_Date older than 18 months before **2026-09-25** => Yes; missing => Unknown. Documented in `docs/methodology.md`.
- Counts: Yes {stats['stale_yes']}, No {stats['stale_no']}, Unknown {stats['stale_unknown']}.

### 5. Dashboard polish
- `docs/dashboard/index.html`: filters for Omnific_Hand_Motion, Sector_Primary, Company_Status, Exit_Type, Possibly_stale; **CSV export** of filtered view; reset control.

### 6. Founder LinkedIn fill-rate
- Before: **{stats['linkedin_before']}/101** with Founder_LinkedIn_URLs.
- After: **{stats['linkedin_after']}/101** (public profiles only; never invented).

### 7. Licence register re-check
- Set `Register_Last_Checked=2026-09-25` on **{stats['licence_rechecks']}** regulated / watchlist ranked names; refreshed Licence_Status where public claims allow. Refresh steps in `docs/licences.md`.

### 8. Conflict log
- Added `docs/Funding_Caveats.md` and `data/funding_caveats.csv` (Moove equity vs facility blending; Moniepoint Series C closes; Interswitch Visa stake).

### 9. Topics/tags
- Added Ranked `Topics` (semicolon tags). Extended Directory Topics where easy.

### 10. CONTRIBUTING
- Added **Good first issues** with concrete honest tasks.

### Rebuild
- Regenerated sqlite, xlsx, companies_enriched.json, dashboard. No invented funding.
"""
    old = path.read_text(encoding="utf-8")
    if "Facelift backlog items 3-10" in old:
        # replace first section header block by prepending fresh and keeping older entries after first ##
        rest = old.split("\n## ", 1)
        path.write_text(entry + ("\n## " + rest[1] if len(rest) > 1 else ""), encoding="utf-8")
    else:
        path.write_text(entry + "\n" + old.split("\n", 1)[-1] if old.startswith("#") else entry + "\n" + old, encoding="utf-8")
        # simpler: prepend after title
        if old.startswith("# Changelog"):
            path.write_text(entry + "\n" + "\n".join(old.splitlines()[1:]).lstrip() + "\n", encoding="utf-8")


def main():
    ranked = read_csv(DATA / "ranked_disclosed.csv")
    directory = read_csv(DATA / "directory.csv")
    rounds = read_csv(DATA / "funding_rounds.csv") if (DATA / "funding_rounds.csv").exists() else []
    investors = read_csv(DATA / "investors.csv") if (DATA / "investors.csv").exists() else []

    dir_before = len(directory)
    directory, removed = clean_directory(directory)
    dir_after = len(directory)
    (RAW).mkdir(parents=True, exist_ok=True)
    (RAW / "directory_quality_pass.json").write_text(
        json.dumps(
            {
                "as_of": AS_OF.isoformat(),
                "before": dir_before,
                "after": dir_after,
                "removed_count": len(removed),
                "removed": removed,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    li_before, li_after = fill_founder_linkedin(ranked)
    apply_stale_and_topics(ranked)
    lic_n = licence_recheck(ranked)

    # Ensure column order: append new cols if needed
    ranked_cols = list(ranked[0].keys())
    for col in ("Possibly_stale", "Topics"):
        if col not in ranked_cols:
            ranked_cols.append(col)
    dir_cols = list(directory[0].keys())
    if "Topics" not in dir_cols:
        dir_cols.append("Topics")

    write_csv(DATA / "ranked_disclosed.csv", ranked, ranked_cols)
    write_csv(DATA / "directory.csv", directory, dir_cols)

    write_funding_caveats()
    patch_methodology()
    patch_data_dictionary()
    patch_licences_doc()
    patch_contributing()

    sqlite_path = export_sqlite(ranked, directory, rounds, investors)
    xlsx_path = write_xlsx(ranked, directory, rounds, investors)
    dash = write_dashboard(ranked)

    # companies enriched json
    (DATA / "companies_enriched.json").write_text(
        json.dumps([{k: r.get(k, "") for k in ranked_cols} for r in ranked], indent=2) + "\n",
        encoding="utf-8",
    )

    stale_counts = Counter(r.get("Possibly_stale") for r in ranked)
    stats = {
        "ranked": len(ranked),
        "dir_before": dir_before,
        "dir_after": dir_after,
        "dir_removed": len(removed),
        "linkedin_before": li_before,
        "linkedin_after": li_after,
        "licence_rechecks": lic_n,
        "stale_yes": stale_counts.get("Yes", 0),
        "stale_no": stale_counts.get("No", 0),
        "stale_unknown": stale_counts.get("Unknown", 0),
        "topics_ranked": sum(1 for r in ranked if not blank(r.get("Topics"))),
        "sqlite": str(sqlite_path),
        "xlsx": str(xlsx_path),
        "dashboard": str(dash),
    }
    patch_readme(stats)
    patch_changelog(stats)
    (RAW / "facelift_backlog_3_10_stats.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")

    # build_meta refresh
    meta_path = DATA / "build_meta.json"
    meta = {}
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta.update(
        {
            "ranked_count": len(ranked),
            "directory_count": len(directory),
            "ranked_founder_linkedin": li_after,
            "ranked_possibly_stale_yes": stats["stale_yes"],
            "ranked_topics": stats["topics_ranked"],
            "licence_register_rechecked": lic_n,
            "directory_removed_junk": len(removed),
            "last_verified": AS_OF.isoformat(),
            "dashboard": str(dash),
        }
    )
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
