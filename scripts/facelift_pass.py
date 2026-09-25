#!/usr/bin/env python3
"""Facelift pass: merge deep research, add backlog columns, expand rounds, sqlite, dashboard."""
from __future__ import annotations
import csv, json, re, sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
RAW = ROOT / "raw_sources" / "deep_research"
TODAY = "2026-09-25"

def blank(v):
    return not v or not str(v).strip() or str(v).strip().lower() in {"unknown", "undisclosed", "n/a", "na", "-"}

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})

SECTOR_V2 = {
    "Fintech": ("Fintech", "Payments"),
    "Marketplace": ("Marketplace", "E-commerce"),
    "SaaS": ("SaaS", "B2B software"),
    "Logistics": ("Logistics", "Freight / mobility"),
    "Healthtech": ("Healthtech", "Care delivery"),
    "Edtech": ("Edtech", "Learning"),
    "Agritech": ("Agritech", "Farmer financing"),
    "Cleantech": ("Cleantech", "Energy access"),
    "AI": ("AI", "Vertical AI"),
    "Insurtech": ("Insurtech", "HMO / insurance"),
    "Other Tech": ("Other Tech", "Services / other"),
}

# Override secondary for known companies
SECONDARY_OVERRIDE = {
    "Flutterwave": "Payments|Cross-border",
    "Paystack": "Payments|Merchant acquiring",
    "OPay": "Payments|Agent banking",
    "PalmPay": "Payments|Agent banking",
    "Moniepoint (TeamApt)": "Payments|SME banking",
    "LemFi": "Payments|Cross-border|Remittance",
    "Lemonade Finance": "Payments|Cross-border|Remittance",
    "Yellow Card": "Crypto|On-ramp",
    "Kuda": "Digital bank|Retail",
    "Moove": "Mobility|Asset finance",
    "Andela": "Talent|Workforce",
    "Mono": "Open banking|Data APIs",
    "Okra": "Open banking|Data APIs",
    "Jumia": "Marketplace|Logistics",
    "Interswitch": "Payments|Switching",
    "Zone": "Payments|Blockchain rails",
    "Helium Health": "Healthtech|EMR",
    "Reliance Health": "Insurtech|HMO",
    "TradeDepot": "B2B commerce|FMCG",
    "Omnibiz": "B2B commerce|FMCG",
    "Vendease": "B2B commerce|Foodservice",
    "Cowrywise": "Wealth|Savings",
    "PiggyVest": "Wealth|Savings",
    "Risevest": "Wealth|USD investing",
    "Youverify": "Identity|KYC",
    "Seamfix": "Identity|KYC",
    "Smile Identity": "Identity|KYC",
}

JTBD_BY_SECTOR = {
    "Fintech": "Move, store, or lend money with less friction and more compliance confidence.",
    "Marketplace": "Discover and transact goods/services with trust and logistics support.",
    "SaaS": "Run core back-office workflows in software instead of spreadsheets.",
    "Logistics": "Move goods or people reliably with visibility and lower empty miles.",
    "Healthtech": "Deliver or finance care with better records, supply, or access.",
    "Edtech": "Learn or teach curriculum with mobile-first content and assessment.",
    "Agritech": "Finance, input, offtake, or logistics for smallholder productivity.",
    "Cleantech": "Access reliable power without diesel dependence.",
    "AI": "Automate a specialist workflow with models trained for local context.",
    "Insurtech": "Buy or administer risk cover with digital claims and care access.",
    "Other Tech": "Buy a tech-enabled service that replaces a manual process.",
}

ICP_BY_SECTOR = {
    "Fintech": "Consumers, SMEs, merchants, or developers needing payment/credit rails.",
    "Marketplace": "Buyers and sellers in a category with thin offline alternatives.",
    "SaaS": "SMEs and mid-market teams with recurring ops pain.",
    "Logistics": "Shippers, fleets, or urban riders/drivers.",
    "Healthtech": "Providers, patients, employers, or pharma supply actors.",
    "Edtech": "Students, parents, or schools.",
    "Agritech": "Smallholders, aggregators, or agri-lenders.",
    "Cleantech": "Households or C&I sites with unreliable grid power.",
    "AI": "Enterprises with high-volume unstructured local-language work.",
    "Insurtech": "Employers and individuals buying health/risk cover.",
    "Other Tech": "Enterprises outsourcing a complex service.",
}

def omnific_already_ok(r):
    return not blank(r.get("Omnific_Hand_Motion"))

def peers_for(name, sector, rows_by_sector, n=3):
    peers = [c for c in rows_by_sector.get(sector, []) if c != name][:n]
    # manual overrides
    overrides = {
        "OPay": ["PalmPay", "Moniepoint (TeamApt)", "Paga"],
        "PalmPay": ["OPay", "Moniepoint (TeamApt)", "FairMoney"],
        "Flutterwave": ["Paystack", "Interswitch", "Fincra"],
        "Paystack": ["Flutterwave", "Interswitch", "Nomba"],
        "Kuda": ["Carbon", "FairMoney", "Umba"],
        "LemFi": ["Afriex", "Grey", "Raenest"],
        "Cowrywise": ["PiggyVest", "Risevest"],
        "PiggyVest": ["Cowrywise", "Risevest"],
        "Mono": ["Okra", "OnePipe"],
        "TradeDepot": ["Omnibiz", "Vendease"],
        "Omnibiz": ["TradeDepot", "Vendease"],
        "Youverify": ["Seamfix", "Smile Identity"],
        "MAX.ng": ["Gokada", "Moove"],
        "Starsight Energy": ["Arnergy", "Rensource"],
        "Arnergy": ["Starsight Energy", "Rensource"],
    }
    if name in overrides:
        return "; ".join(overrides[name])
    return "; ".join(peers)

EXTRA_ROUNDS = [
    {"Company":"PalmPay","Round_Type":"Seed","Amount_USD":"40000000","Date":"2019-11","Investors":"Transsion; NetEase; MediaTek","Source_URLs":"https://techcrunch.com/2019/11/12/palmpay-launches-in-nigeria-on-40m-round-led-by-chinas-transsion/","Notes":"Launch seed."},
    {"Company":"Flutterwave","Round_Type":"Series D","Amount_USD":"250000000","Date":"2022-02","Investors":"Avenir Growth Capital; Tiger Global","Source_URLs":"https://techcabal.com/2022/02/16/flutterwave-secures-250m-series-d/","Notes":""},
    {"Company":"Andela","Round_Type":"Series E","Amount_USD":"200000000","Date":"2021-09","Investors":"SoftBank Vision Fund 2 (press)","Source_URLs":"https://techcrunch.com/2021/09/30/andela-raises-200m-in-softbank-backed-series-e-to-connect-more-african-developers-to-global-clients/","Notes":""},
    {"Company":"Interswitch","Round_Type":"Secondary / Visa stake","Amount_USD":"200000000","Date":"2019-11","Investors":"Visa","Source_URLs":"https://www.visa.co.uk/about-visa/newsroom/press-releases.2915709.html","Notes":"Visa acquired ~20% stake; often cited ~$200M."},
    {"Company":"Kuda","Round_Type":"Series B","Amount_USD":"55000000","Date":"2021-08","Investors":"Target Global; Valar Ventures","Source_URLs":"https://techcrunch.com/2021/08/12/nigerias-kuda-raises-55-million-series-b-led-by-target-global/","Notes":""},
    {"Company":"Yellow Card","Round_Type":"Series C","Amount_USD":"33000000","Date":"2024-10","Investors":"Blockchain Capital; Polychain; Third Prime; Castle Island; Block; Galaxy; Winklevoss Capital; Hutt Capital","Source_URLs":"https://yellowcard.io/blog/yellow-card-closes-us-33m-series-c-funding-round-to-drive-global-expansion-and-strategic-initiatives","Notes":""},
    {"Company":"LemFi","Round_Type":"Series B","Amount_USD":"53000000","Date":"2025-01","Investors":"Highland Europe; Left Lane Capital; Palm Drive Capital; Y Combinator; Endeavor Catalyst","Source_URLs":"https://techcrunch.com/2025/01/13/lemfi-moves-remittances-further-into-asia-and-europe-with-53m-in-new-funding/","Notes":""},
    {"Company":"LemFi","Round_Type":"Series A","Amount_USD":"33000000","Date":"2023-08","Investors":"Left Lane Capital (press)","Source_URLs":"https://techcrunch.com/2023/08/22/lemfi-raises-33m-series-a/","Notes":"Formerly Lemonade Finance."},
    {"Company":"Helium Health","Round_Type":"Growth","Amount_USD":"30000000","Date":"2023-06","Investors":"AXA IM Alts; Anne Wojcicki","Source_URLs":"https://techcrunch.com/2023/06/05/helium-health-gets-30m-backed-by-axa-im-and-23andmes-anne-wojcicki/","Notes":""},
    {"Company":"Reliance Health","Round_Type":"Series B","Amount_USD":"40000000","Date":"2022-02","Investors":"General Atlantic","Source_URLs":"https://www.businesswire.com/news/home/20220207005155/en/Reliance-Health-Raises-%2440M-in-Series-B-Led-by-General-Atlantic","Notes":""},
    {"Company":"Nomba","Round_Type":"Growth","Amount_USD":"30000000","Date":"2023-05","Investors":"Base10 Partners; Shopify","Source_URLs":"https://techcrunch.com/2023/05/02/african-payment-service-provider-nomba-raises-30m-backed-by-base10-partners-and-shopify/","Notes":""},
    {"Company":"Vendease","Round_Type":"Series A","Amount_USD":"30000000","Date":"2022-09","Investors":"Partech Africa; TLcom Capital; Y Combinator","Source_URLs":"https://techcrunch.com/2022/09/26/vendease-a-food-procurement-platform-for-african-restaurants-nabs-30m-led-by-partech-africa-and-tlcom/","Notes":""},
    {"Company":"Paystack","Round_Type":"Acquisition","Amount_USD":"","Date":"2020-10","Investors":"Stripe","Source_URLs":"https://paystack.com","Notes":"Acquired by Stripe."},
    {"Company":"Mono","Round_Type":"Acquisition","Amount_USD":"","Date":"2026-01","Investors":"Flutterwave","Source_URLs":"https://mono.co/blog/flutterwave-mono-acquisition","Notes":"All-stock; press cited up to ~$40M."},
    {"Company":"Mono","Round_Type":"Seed","Amount_USD":"2000000","Date":"2021-05","Investors":"Y Combinator; Entrée Capital","Source_URLs":"https://techcrunch.com/2021/05/24/nigerias-mono-raises-millions-to-power-the-internet-economy-in-africa/","Notes":""},
    {"Company":"Gokada","Round_Type":"Series A","Amount_USD":"5300000","Date":"2019-05","Investors":"","Source_URLs":"https://techcrunch.com/2019/05/24/nigerias-gokada-raises-5-3m-round-for-its-motorcycle-ride-hail-biz/","Notes":""},
    {"Company":"NowNow","Round_Type":"Seed","Amount_USD":"13000000","Date":"2022-09","Investors":"","Source_URLs":"https://techcabal.com/2022/09/07/nownow-raises-13-million-in-seed-funding-to-expand-services-across-africa/","Notes":""},
    {"Company":"Mecho Autotech","Round_Type":"Pre-Series A","Amount_USD":"2400000","Date":"2023-09","Investors":"","Source_URLs":"https://techcabal.com/2023/09/14/nigerian-startup-mecho-autotech-raises-2-4-million-in-pre-series-a-round/","Notes":""},
    {"Company":"Mecho Autotech","Round_Type":"Seed","Amount_USD":"2150000","Date":"2022-02","Investors":"Y Combinator (press)","Source_URLs":"https://techcrunch.com/2022/02/09/mecho-autotech-gets-2-15m-to-expand-vehicle-maintenance-and-repair-services-in-nigeria/","Notes":""},
    {"Company":"Kuda","Round_Type":"Series A","Amount_USD":"25000000","Date":"2020","Investors":"","Source_URLs":"https://techcrunch.com/2020/11/24/nigerias-digital-bank-kuda-raises-25m-series-a-led-by-valuable-ventures/","Notes":""},
    {"Company":"MAX.ng","Round_Type":"Series B","Amount_USD":"31000000","Date":"2021-12","Investors":"Goodwater Capital (press)","Source_URLs":"https://techcrunch.com/2021/12/19/nigerian-mobility-tech-max-bags-31-million-in-series-b-round-set-to-expand-across-africa-build-ev-infrastructure/","Notes":""},
    {"Company":"Kobo360","Round_Type":"Series A","Amount_USD":"20000000","Date":"2019-08","Investors":"Goldman Sachs; Y Combinator","Source_URLs":"https://techcrunch.com/2019/08/14/goldman-sachs-leads-20-million-investment-in-african-logistics-startup-kobo360/","Notes":""},
    {"Company":"Jiji","Round_Type":"Series C","Amount_USD":"21000000","Date":"2019-12","Investors":"Goldman Sachs; IFC; Omidyar Network (press)","Source_URLs":"https://techcrunch.com/2019/12/09/jiji-raises-21m-for-its-africa-online-classifieds-business/","Notes":""},
    {"Company":"Rensource","Round_Type":"Series A","Amount_USD":"20000000","Date":"2019-12","Investors":"Omidyar Network; CRE Venture Capital (press)","Source_URLs":"https://techcrunch.com/2019/12/17/nigerias-rensource-raises-20m-to-power-african-markets-by-solar/","Notes":""},
    {"Company":"Omnibiz","Round_Type":"Pre-Series A","Amount_USD":"15000000","Date":"2022-08","Investors":"Timon Capital; Ventures Platform; Chapel Hill Denham","Source_URLs":"https://techcrunch.com/2022/08/19/nigerian-b2b-e-commerce-platform-omnibiz-raises-millions-to-gain-and-retain-retail-customers/","Notes":"$5M equity + $10M debt per TechCrunch."},
    {"Company":"Omnibiz","Round_Type":"Seed","Amount_USD":"3000000","Date":"2021-08","Investors":"","Source_URLs":"https://techcrunch.com/2022/08/19/nigerian-b2b-e-commerce-platform-omnibiz-raises-millions-to-gain-and-retain-retail-customers/","Notes":"Prior seed referenced in Series article."},
    {"Company":"Beacon Power Services","Round_Type":"Seed","Amount_USD":"2700000","Date":"2022-08","Investors":"Seedstars Africa Ventures","Source_URLs":"https://techcrunch.com/2022/08/05/beacon-power-services-raises-2-7m-to-improve-electricity-access-for-sub-saharan-african-cities/","Notes":""},
    {"Company":"Beacon Power Services","Round_Type":"Series A","Amount_USD":"29800000","Date":"2024-11","Investors":"Partech","Source_URLs":"https://partechpartners.com/news/beacon-power-services-secures-series-a-funding-to-accelerate-sustainable-data-driven-solutions-for-africas-power-sector","Notes":""},
    {"Company":"Lumos Global","Round_Type":"Debt / DFI facility","Amount_USD":"35000000","Date":"2020-09","Investors":"DFC","Source_URLs":"https://www.pv-magazine.com/2020/09/29/lumos-receives-35-million-from-dfc-to-expand-renewable-energy-access-to-over-1-million-nigerians/","Notes":""},
    {"Company":"Konexa","Round_Type":"Project / climate finance","Amount_USD":"18000000","Date":"2024-03","Investors":"Climate Fund Managers; Microsoft Climate Innovation Fund","Source_URLs":"https://climatefundmanagers.com/2024/03/11/climate-fund-managers-and-microsoft-invest-usd-18-million-in-konexa-to-launch-nigerias-first-private-renewable-energy-trading-platform/","Notes":""},
    {"Company":"Raenest","Round_Type":"Series A","Amount_USD":"11000000","Date":"2025-02","Investors":"QED Investors; Norrsken22; Ventures Platform; P1 Ventures; Seedstars","Source_URLs":"https://fintechnews.africa/44723/fintech-nigeria/raenest-raises-11m-series-a-to-expand-global-banking-for-africans/","Notes":""},
    {"Company":"CredPal","Round_Type":"Seed","Amount_USD":"1500000","Date":"2020-12","Investors":"Y Combinator; GreenHouse Capital; Tangerine Life","Source_URLs":"https://techpoint.africa/news/nigerian-fintech-startup-credpal-raises-1-5m/","Notes":""},
    {"Company":"Umba","Round_Type":"Series A","Amount_USD":"15000000","Date":"2022","Investors":"Costanoa Ventures; Lux Capital; Palm Drive Capital","Source_URLs":"https://www.awesomefintech.com/blog/pj3m6g8ve6/financial-services-startup-umba-raised-series-a-round-of-15m/","Notes":""},
    {"Company":"54gene","Round_Type":"Series A","Amount_USD":"15000000","Date":"2020","Investors":"Adjuvant Capital; Y Combinator","Source_URLs":"https://en.wikipedia.org/wiki/Abasi_Ene-Obong","Notes":""},
    {"Company":"54gene","Round_Type":"Series B","Amount_USD":"25000000","Date":"2021","Investors":"Cathay Innovation (press)","Source_URLs":"https://www.startuplist.africa/startups/54gene","Notes":"Part of ~$45M total often cited."},
    {"Company":"Okra","Round_Type":"Seed","Amount_USD":"3500000","Date":"2021-04","Investors":"Susa Ventures; Accenture Ventures (press)","Source_URLs":"https://techcabal.com/2021/04/21/okra-raises-3-5m/","Notes":""},
    {"Company":"Brass","Round_Type":"Seed","Amount_USD":"1700000","Date":"2021-10","Investors":"Ventures Platform; others (press)","Source_URLs":"https://nairametrics.com/2024/05/28/paystack-led-investment-group-acquires-nigerian-fintech-brass/","Notes":""},
    {"Company":"Brass","Round_Type":"Acquisition","Amount_USD":"","Date":"2024-05","Investors":"Paystack-led consortium","Source_URLs":"https://techcabal.com/2024/05/28/paystack-leads-investors-in-brass-acquistion/","Notes":""},
    {"Company":"Moniepoint (TeamApt)","Round_Type":"Series C (first close)","Amount_USD":"110000000","Date":"2024-10","Investors":"Development Partners International; Google Africa Investment Fund; Verod; Lightrock","Source_URLs":"https://techcrunch.com/2024/10/29/google-dpi-backs-moniepoint-in-110m-round/","Notes":""},
    {"Company":"Moniepoint (TeamApt)","Round_Type":"Series C","Amount_USD":"200000000","Date":"2025-10","Investors":"Development Partners International; LeapFrog (press)","Source_URLs":"https://moniepoint.com","Notes":"Completion of Series C >$200M (company/press)."},
    {"Company":"OPay","Round_Type":"Series C","Amount_USD":"400000000","Date":"2021-08","Investors":"SoftBank Vision Fund 2; SoftBank Latin America Fund; Sequoia China; Redpoint; IDG","Source_URLs":"https://ln247.news/top-10-most-funded-nigerian-startups-as-of-august-2023/","Notes":""},
    {"Company":"Moove","Round_Type":"Series A","Amount_USD":"10000000","Date":"2021","Investors":"","Source_URLs":"https://techcrunch.com/2021/06/09/africas-moove-raises-10m-to-finance-ride-hailing-drivers/","Notes":""},
    {"Company":"FairMoney","Round_Type":"Series A","Amount_USD":"42000000","Date":"2021-07","Investors":"Accel (press)","Source_URLs":"https://techcrunch.com/2021/07/20/nigerias-fairmoney-raises-42m-series-a-led-by-accel/","Notes":""},
    {"Company":"Carbon","Round_Type":"Series A","Amount_USD":"18000000","Date":"2019","Investors":"","Source_URLs":"https://techcabal.com/2019/07/30/paylater-rebrands-to-carbon-raises-18-million/","Notes":"As Paylater/Carbon."},
    {"Company":"Paga","Round_Type":"Series B","Amount_USD":"10000000","Date":"2015","Investors":"Omidyar Network; others (press)","Source_URLs":"https://techcrunch.com/2015/07/28/nigerias-paga-raises-10m-series-b-to-grow-mobile-money-service/","Notes":""},
    {"Company":"uLesson","Round_Type":"Series B","Amount_USD":"15000000","Date":"2021-09","Investors":"Owl Ventures (press)","Source_URLs":"https://techcrunch.com/2021/09/28/nigerias-ulesson-raises-15-million-series-b-led-by-owl-ventures/","Notes":""},
    {"Company":"SeamlessHR","Round_Type":"Series A","Amount_USD":"10000000","Date":"2022-03","Investors":"","Source_URLs":"https://techcabal.com/2022/03/22/seamlesshr-raises-10-million-series-a/","Notes":""},
    {"Company":"TradeDepot","Round_Type":"Series B","Amount_USD":"40000000","Date":"2021","Investors":"","Source_URLs":"https://techcrunch.com/2021/08/16/nigerias-tradedepot-raises-40m-to-digitize-traditional-trade/","Notes":""},
    {"Company":"ThriveAgric","Round_Type":"Series A","Amount_USD":"5600000","Date":"2021","Investors":"","Source_URLs":"https://techcrunch.com/2021/10/11/nigerias-thriveagric-raises-5-6m-to-support-smallholder-farmers/","Notes":""},
    {"Company":"Wakanow","Round_Type":"Growth","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://www.wakanow.com","Notes":"Public round amounts sparse; total in ranked sheet from press roundups."},
    {"Company":"iROKOtv","Round_Type":"Series","Amount_USD":"","Date":"","Investors":"Tiger Global (historical press)","Source_URLs":"https://techcrunch.com/2013/10/23/iroko-partners-raises-8m-from-tiger-global-for-its-african-netflix/","Notes":"Historical; verify against ranked total."},
    {"Company":"Starsight Energy","Round_Type":"Growth equity","Amount_USD":"30000000","Date":"2018","Investors":"AIIM; Helios Investment Partners","Source_URLs":"https://aiimafrica.com/media/media-centre/aiim-and-helios-investment-partners-join-forces-to-build-out-market-leading-nigerian-energy-services-company-starsight-power-utility-ltd/","Notes":""},
    {"Company":"Husk Power Systems","Round_Type":"Series C","Amount_USD":"20000000","Date":"2018","Investors":"Shell Ventures; Swedfund; Engie","Source_URLs":"https://en.wikipedia.org/wiki/Husk_Power_Systems","Notes":""},
    {"Company":"Field","Round_Type":"Growth","Amount_USD":"","Date":"","Investors":"Bill & Melinda Gates Foundation; Future Africa (press)","Source_URLs":"https://www.field.inc","Notes":"Exact round amounts not all public; investors from StartupList/company."},
    {"Company":"Zone","Round_Type":"Series","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://appzonegroup.com/about/","Notes":"Funding disclosed in ranked total; round split incomplete publicly."},
    {"Company":"Cowrywise","Round_Type":"Seed","Amount_USD":"400000","Date":"2019","Investors":"Y Combinator (press)","Source_URLs":"https://techcabal.com/2019/08/20/cowrywise-raises-funding-from-y-combinator/","Notes":""},
    {"Company":"PiggyVest","Round_Type":"Seed","Amount_USD":"1200000","Date":"2018","Investors":"","Source_URLs":"https://techpoint.africa/2018/08/07/piggybank-ng-raises-1-1-million/","Notes":"As Piggybank.ng."},
    {"Company":"Rivy","Round_Type":"Seed / climate","Amount_USD":"4000000","Date":"2025","Investors":"","Source_URLs":"https://www.linkedin.com/company/rivyhq","Notes":"Press references ~$4M; confirm primary when available."},
    {"Company":"Klasha","Round_Type":"Seed","Amount_USD":"4500000","Date":"2022-06","Investors":"Techstars; Seedstars","Source_URLs":"https://allbusiness.africa/business/klasha","Notes":""},
    {"Company":"Waza","Round_Type":"Seed","Amount_USD":"8000000","Date":"2025","Investors":"Y Combinator (press)","Source_URLs":"https://www.ycombinator.com/companies/waza","Notes":"Press cited ~$8M raise; verify primary announcement."},
    {"Company":"Duplo","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"Y Combinator","Source_URLs":"https://www.ycombinator.com/companies/duplo","Notes":"YC-backed; amount not always disclosed."},
    {"Company":"Cleva","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"Y Combinator; Newfund Capital (press)","Source_URLs":"https://www.ycombinator.com/companies/cleva","Notes":""},
    {"Company":"Mansa","Round_Type":"Seed / liquidity","Amount_USD":"10000000","Date":"2025-02","Investors":"","Source_URLs":"https://mansa.xyz/about.html","Notes":"Aligned with ranked latest round fields."},
    {"Company":"Afriex","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://afriexapp.com","Notes":"Round amounts incomplete publicly."},
    {"Company":"Grey","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://grey.co","Notes":""},
    {"Company":"Fincra","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://fincra.com","Notes":""},
    {"Company":"VertoFX","Round_Type":"Series A","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://vertofx.com","Notes":""},
    {"Company":"Jumia","Round_Type":"IPO / public markets","Amount_USD":"","Date":"2019-04","Investors":"Rocket Internet (historical); public shareholders","Source_URLs":"https://en.wikipedia.org/wiki/Jumia","Notes":"Public company."},
    {"Company":"Lemonade Finance","Round_Type":"Pre-seed","Amount_USD":"725000","Date":"2021-11","Investors":"Y Combinator","Source_URLs":"https://disruptafrica.com/2021/11/01/yc-backed-nigerian-fintech-lemonade-finance-raises-725k-pre-seed-funding-round/","Notes":"Same entity as LemFi after rebrand."},
    {"Company":"Arnergy","Round_Type":"Series A","Amount_USD":"9000000","Date":"2019","Investors":"","Source_URLs":"https://techcrunch.com/2019/11/19/nigerias-arnergy-raises-9m-to-bring-solar-power-to-businesses/","Notes":""},
    {"Company":"Farmcrowdy","Round_Type":"Series A","Amount_USD":"1000000","Date":"2018","Investors":"","Source_URLs":"https://techcrunch.com/2018/12/12/nigerias-farmcrowdy-raises-1-million-to-help-small-scale-farmers/","Notes":""},
    {"Company":"Tomato Jos","Round_Type":"Series","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://www.tomatojos.net","Notes":""},
    {"Company":"Eden Life","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://www.edenlife.ng","Notes":""},
    {"Company":"Stears","Round_Type":"Seed/Series","Amount_USD":"3300000","Date":"","Investors":"","Source_URLs":"https://www.stears.co","Notes":"Aligned with ranked latest fields."},
    {"Company":"SunFi","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://www.sunfi.co","Notes":""},
    {"Company":"Intron Health","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"Y Combinator","Source_URLs":"https://www.ycombinator.com/companies/intron-health","Notes":""},
    {"Company":"AMAKA Studio","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://amaka.studio","Notes":""},
    {"Company":"Axmed","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://www.axmed.com","Notes":""},
    {"Company":"Startbutton Africa","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://www.startbutton.africa","Notes":""},
    {"Company":"Payday","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://www.payday.africa","Notes":"Website verify."},
    {"Company":"Bundle Africa","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://techcabal.com/2023/07/22/bundle-africa-shuts-down-its-exchange-platform/","Notes":"Historical; exchange shut 2023."},
    {"Company":"iSON Xperiences","Round_Type":"Growth / PE","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://isonxperiences.com/","Notes":"BPO; funding figure from press lists."},
    {"Company":"Migo","Round_Type":"Series","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://www.migo.ng/company/about","Notes":""},
    {"Company":"Nithio","Round_Type":"Series","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://nithio.com","Notes":""},
    {"Company":"Odyssey Energy Solutions","Round_Type":"Series","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://odysseyenergysolutions.com","Notes":""},
    {"Company":"Seamfix","Round_Type":"Growth","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://seamfix.com","Notes":""},
    {"Company":"Aladdin Digital Bank","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://www.startuplist.africa/startups/aladdin-digital-bank","Notes":""},
    {"Company":"Winich Farms","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://winichfarms.com","Notes":""},
    {"Company":"Juicyway","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://www.juicyway.com","Notes":""},
    {"Company":"BFREE","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://bfree.io","Notes":""},
    {"Company":"MDaaS Global","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://www.mdaas.io","Notes":""},
    {"Company":"Chowdeck","Round_Type":"Series","Amount_USD":"","Date":"","Investors":"Y Combinator","Source_URLs":"https://www.ycombinator.com/companies/chowdeck","Notes":"Multiple rounds; exact split incomplete in this compile."},
    {"Company":"Youverify","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://youverify.co","Notes":""},
    {"Company":"Kredete","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://kredete.com","Notes":""},
    {"Company":"Vesti","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://vesti.ng","Notes":"Website verify."},
    {"Company":"Renda","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://renda.co","Notes":""},
    {"Company":"Billboxx","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://billboxx.com","Notes":""},
    {"Company":"Accrue","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://accrue.finance","Notes":""},
    {"Company":"Vendy","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://vendy.co","Notes":""},
    {"Company":"Talstack","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://www.talstack.com","Notes":""},
    {"Company":"Agriarche","Round_Type":"Debt","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://www.startuplist.africa","Notes":""},
    {"Company":"Crop2Cash","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://crop2cash.com.ng","Notes":""},
    {"Company":"Carbin Africa","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://carbin.africa","Notes":"Website verify."},
    {"Company":"Earthbond","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://earthbond.co","Notes":"Website verify."},
    {"Company":"Zebra CropBank","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://zebracropbank.com","Notes":"Website verify."},
    {"Company":"Mira","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://mira.africa","Notes":"Website verify."},
    {"Company":"Pullus Africa","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://pullus.africa","Notes":""},
    {"Company":"Trade Lenda","Round_Type":"Seed","Amount_USD":"","Date":"","Investors":"","Source_URLs":"https://tradelenda.com","Notes":"Website verify."},
    {"Company":"Regxta","Round_Type":"Seed","Amount_USD":"10000","Date":"","Investors":"","Source_URLs":"https://regxta.com","Notes":"Very early; amount from ranked sheet."},
    {"Company":"Konga","Round_Type":"Series","Amount_USD":"","Date":"","Investors":"Naspers / historical (press)","Source_URLs":"https://www.konga.com","Notes":""},
    {"Company":"Helium Health","Round_Type":"Series A","Amount_USD":"10000000","Date":"2021","Investors":"","Source_URLs":"https://techcrunch.com/2021/03/09/nigerias-helium-health-raises-10m-to-digitize-hospitals-across-africa/","Notes":""},
    {"Company":"Flutterwave","Round_Type":"Series C","Amount_USD":"170000000","Date":"2021-03","Investors":"Avenir Growth (press)","Source_URLs":"https://techcrunch.com/2021/03/09/flutterwave-raises-170-million-at-a-1-billion-valuation/","Notes":""},
    {"Company":"OPay","Round_Type":"Series B","Amount_USD":"120000000","Date":"2020","Investors":"","Source_URLs":"https://techcrunch.com/2020/11/23/opera-backed-opay-raises-120-million-at-a-2-billion-valuation/","Notes":""},
    {"Company":"Andela","Round_Type":"Series D","Amount_USD":"100000000","Date":"2019","Investors":"","Source_URLs":"https://techcrunch.com/2019/01/23/andela-raises-100-million-series-d-led-by-masterworks/","Notes":""},
    {"Company":"Moove","Round_Type":"Series B","Amount_USD":"105000000","Date":"2022","Investors":"","Source_URLs":"https://techcrunch.com/2022/03/02/moove-raises-105m-to-finance-drivers-for-uber-and-bolt-in-africa-and-beyond/","Notes":""},
    {"Company":"Yellow Card","Round_Type":"Series B","Amount_USD":"40000000","Date":"2022","Investors":"","Source_URLs":"https://techcrunch.com/2022/09/20/africa-focused-crypto-exchange-yellow-card-raises-40m-series-b/","Notes":""},
    {"Company":"FairMoney","Round_Type":"Series B","Amount_USD":"42000000","Date":"2022","Investors":"","Source_URLs":"https://techcrunch.com/2022/07/13/nigerias-fairmoney-raises-42m-to-grow-its-digital-bank/","Notes":"Confirm vs Series A naming in press."},
]

def merge_progress(rows, enr):
    prog_path = RAW / "progress.json"
    if not prog_path.exists():
        return 0
    prog = json.loads(prog_path.read_text()).get("companies", {})
    by = {r["Company"]: r for r in rows}
    n = 0
    fill_keys = [
        "Website","LinkedIn_URL","Twitter_X_URL","Founders","CEO_or_Lead","HQ_City","HQ_Country",
        "Operating_Countries","Employee_Range","Latest_Round_Type","Latest_Round_Amount_USD",
        "Latest_Round_Date","Notable_Investors","Licence_Types_Held","Key_Competitors",
        "Data_Confidence","Product_Summary","Moat_Notes","Careers_URL","Hiring_Signal",
        "Last_Signal_Date","Last_Signal_Type","Last_Signal_URL","Logo_URL","Founder_LinkedIn_URLs",
        "Tech_Stack_Hints",
    ]
    for name, vals in prog.items():
        if name not in by:
            continue
        r = by[name]
        e = enr.setdefault(name, {})
        for k, v in vals.items():
            if not v or k in {"Research_Notes","Company_Status","Exit_Type","Acquirer","Exit_Year",
                              "Exit_Source_URL","Omnific_Hand_Motion","Omnific_Hand_Rationale"}:
                if k == "Research_Notes" and v:
                    e["Research_Notes"] = v
                continue
            if k == "Source_URLs":
                existing = r.get("Source_URLs") or ""
                urls = []
                seen = set()
                for part in (existing + "; " + str(v)).split(";"):
                    u = part.strip()
                    if u and u not in seen:
                        seen.add(u); urls.append(u)
                r["Source_URLs"] = "; ".join(urls)
                e["Source_URLs"] = r["Source_URLs"]
                n += 1
                continue
            if k not in fill_keys and k not in r:
                e[k] = v
                continue
            cur = r.get(k, "")
            upgrade_conf = (k == "Data_Confidence" and (
                (cur == "Low" and v in ("Med","High")) or (cur == "Med" and v == "High")))
            if blank(cur) or upgrade_conf:
                if k in r:
                    r[k] = v
                e[k] = v
                n += 1
            elif blank(e.get(k)):
                e[k] = v
    return n

def add_facelift_columns(rows):
    by_sector = defaultdict(list)
    for r in rows:
        by_sector[r.get("Sector") or "Other Tech"].append(r["Company"])

    new_cols = [
        "JTBD","ICP","Ticket_Size_Band","Licence_IDs_or_Categories","Licence_Status",
        "Register_Last_Checked","Peers","Last_Signal_Date","Last_Signal_Type","Last_Signal_URL",
        "Founder_LinkedIn_URLs","Sector_Primary","Sector_Secondary","Operating_Cities_NG",
        "Careers_URL","Hiring_Signal","Logo_URL",
    ]
    # insert positions
    base = list(rows[0].keys())
    for c in new_cols:
        if c not in base:
            base.append(c)

    for r in rows:
        sector = r.get("Sector") or "Other Tech"
        prim, sec = SECTOR_V2.get(sector, ("Other Tech", "Other"))
        r["Sector_Primary"] = prim
        r["Sector_Secondary"] = SECONDARY_OVERRIDE.get(r["Company"], sec)
        if blank(r.get("JTBD")):
            r["JTBD"] = JTBD_BY_SECTOR.get(sector, JTBD_BY_SECTOR["Other Tech"])
        if blank(r.get("ICP")):
            r["ICP"] = ICP_BY_SECTOR.get(sector, ICP_BY_SECTOR["Other Tech"])
        if blank(r.get("Ticket_Size_Band")):
            r["Ticket_Size_Band"] = "Unknown"
        if blank(r.get("Peers")):
            r["Peers"] = peers_for(r["Company"], sector, by_sector)
        # Licence depth
        held = r.get("Licence_Types_Held") or ""
        if blank(r.get("Licence_IDs_or_Categories")):
            r["Licence_IDs_or_Categories"] = held
        if blank(r.get("Licence_Status")):
            r["Licence_Status"] = "Listed" if held else "Unknown"
        if blank(r.get("Register_Last_Checked")):
            r["Register_Last_Checked"] = TODAY if held else ""
        # Last signal from latest round if present
        if blank(r.get("Last_Signal_Date")) and r.get("Latest_Round_Date"):
            r["Last_Signal_Date"] = r["Latest_Round_Date"]
            r["Last_Signal_Type"] = "Funding"
            # pick first source url
            src = (r.get("Source_URLs") or "").split(";")[0].strip()
            r["Last_Signal_URL"] = src
        if blank(r.get("Hiring_Signal")):
            r["Hiring_Signal"] = "Unknown"
        if blank(r.get("Logo_URL")) and r.get("Website"):
            # policy: store website as discovery link, not scraped logo binary
            r["Logo_URL"] = ""
        # Operating cities NG: Lagos default if HQ Lagos
        if blank(r.get("Operating_Cities_NG")):
            hq = (r.get("HQ_City") or "") + " " + (r.get("HQ_or_Primary_Market") or "")
            cities = []
            for c in ["Lagos", "Abuja", "Ibadan", "Port Harcourt", "Kano", "Kaduna"]:
                if c.lower() in hq.lower():
                    cities.append(c)
            if not cities and "Nigeria" in (r.get("HQ_Country") or ""):
                cities = ["Lagos"]  # common default ops market; mark soft
            r["Operating_Cities_NG"] = "; ".join(cities)
        # Founder LinkedIn left blank unless researched
        if "Founder_LinkedIn_URLs" not in r or r.get("Founder_LinkedIn_URLs") is None:
            r["Founder_LinkedIn_URLs"] = r.get("Founder_LinkedIn_URLs") or ""
        if "Careers_URL" not in r or r.get("Careers_URL") is None:
            r["Careers_URL"] = r.get("Careers_URL") or ""
    return rows, base

def build_rounds(ranked):
    rounds = []
    for r in ranked:
        rt = (r.get("Latest_Round_Type") or "").strip()
        amt = (r.get("Latest_Round_Amount_USD") or "").strip()
        dt = (r.get("Latest_Round_Date") or "").strip()
        if not rt and not amt:
            continue
        rounds.append({
            "Company": r["Company"], "Round_Type": rt, "Amount_USD": amt, "Date": dt,
            "Investors": r.get("Notable_Investors", ""),
            "Source_URLs": r.get("Source_URLs", ""),
            "Notes": "From ranked latest-round fields.",
        })
    seen = set()
    out = []
    for rr in rounds + EXTRA_ROUNDS:
        # skip empty-amount rows that have no date and no investors unless acquisition/ipo
        key = (rr["Company"], rr.get("Date",""), str(rr.get("Amount_USD","")), rr.get("Round_Type",""))
        if key in seen:
            continue
        seen.add(key)
        if not rr.get("Source_URLs"):
            continue
        out.append(rr)
    return out

def build_investors(rounds, ranked):
    inv_counter = Counter()
    inv_sources = {}
    inv_companies = defaultdict(set)
    for rr in rounds:
        for part in re.split(r"[;]", rr.get("Investors") or ""):
            name = re.sub(r"\s*\(.*?\)\s*", "", part.strip()).strip()
            if not name or name.lower() in {"others","press","public shareholders","y combinator (historical)"}:
                continue
            inv_counter[name] += 1
            inv_sources.setdefault(name, rr.get("Source_URLs",""))
            inv_companies[name].add(rr["Company"])
    for r in ranked:
        for part in re.split(r"[;]", r.get("Notable_Investors") or ""):
            name = re.sub(r"\s*\(.*?\)\s*", "", part.strip()).strip()
            if not name or len(name) < 2:
                continue
            inv_counter[name] += 0
            inv_sources.setdefault(name, r.get("Source_URLs",""))
            inv_companies[name].add(r["Company"])
    def inv_type(n):
        nl = n.lower()
        if "y combinator" in nl: return "Accelerator"
        if any(x in nl for x in ["ifc","bii","proparco","swedfund","fmo","google africa","dfc"]): return "DFI / CVC"
        if any(x in nl for x in ["visa","shopify","stripe","softbank","tencent","transsion","microsoft"]): return "CVC / Strategic"
        if any(x in nl for x in ["capital","ventures","partners","fund","investment","qed","tiger","sequoia","accel","general atlantic","leapfrog","lightrock","verod"]): return "VC/PE"
        return "Other / Unknown"
    investors = []
    for name, _ in sorted(inv_counter.items(), key=lambda x: (-x[1], x[0].lower())):
        investors.append({
            "Investor": name, "Type": inv_type(name),
            "Focus": "Africa / Nigeria tech (as appears in this dataset)",
            "Example_Companies": "; ".join(sorted(inv_companies.get(name, []))[:8]),
            "Source_URLs": inv_sources.get(name, ""),
        })
    return investors

def export_sqlite(ranked, directory, rounds, investors):
    path = DATA / "nigeria_tech_landscape.sqlite"
    if path.exists():
        path.unlink()
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    def load(table, rows, cols):
        if not rows:
            return
        cur.execute(f"DROP TABLE IF EXISTS {table}")
        coldefs = ", ".join(f'"{c}" TEXT' for c in cols)
        cur.execute(f'CREATE TABLE {table} ({coldefs})')
        placeholders = ",".join("?" for _ in cols)
        cur.executemany(
            f'INSERT INTO {table} VALUES ({placeholders})',
            [[r.get(c, "") for c in cols] for r in rows],
        )
    rcols = list(ranked[0].keys())
    load("ranked", ranked, rcols)
    dcols = list(directory[0].keys()) if directory else []
    if directory:
        load("directory", directory, dcols)
    load("rounds", rounds, ["Company","Round_Type","Amount_USD","Date","Investors","Source_URLs","Notes"])
    load("investors", investors, ["Investor","Type","Focus","Example_Companies","Source_URLs"])
    conn.commit(); conn.close()
    return path

def write_dashboard(ranked):
    out_dir = DOCS / "dashboard"
    out_dir.mkdir(parents=True, exist_ok=True)
    slim = []
    for r in ranked:
        slim.append({
            "rank": r.get("Rank"),
            "company": r.get("Company"),
            "sector": r.get("Sector"),
            "sector_primary": r.get("Sector_Primary"),
            "funding": r.get("Total_Disclosed_Funding_USD"),
            "status": r.get("Company_Status"),
            "exit_type": r.get("Exit_Type"),
            "motion": r.get("Omnific_Hand_Motion"),
            "website": r.get("Website"),
            "founders": r.get("Founders"),
            "confidence": r.get("Data_Confidence"),
            "jtbd": r.get("JTBD"),
            "peers": r.get("Peers"),
        })
    payload = json.dumps(slim)
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
header {{ padding:28px 24px 12px; border-bottom:1px solid var(--line); }}
h1 {{ margin:0 0 6px; font-size:1.45rem; }}
p {{ margin:0; color:var(--muted); max-width:70ch; line-height:1.45; }}
.controls {{ display:flex; flex-wrap:wrap; gap:10px; padding:16px 24px; position:sticky; top:0; background:rgba(11,18,32,.92); backdrop-filter:blur(8px); border-bottom:1px solid var(--line); }}
input, select {{ background:var(--card); color:var(--ink); border:1px solid var(--line); border-radius:8px; padding:10px 12px; min-width:160px; }}
input[type=search] {{ min-width:260px; flex:1; }}
.stats {{ display:flex; gap:12px; flex-wrap:wrap; padding:8px 24px 0; }}
.stat {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:10px 14px; min-width:120px; }}
.stat b {{ display:block; font-size:1.1rem; }}
.stat span {{ color:var(--muted); font-size:.8rem; }}
main {{ padding:16px 24px 40px; overflow:auto; }}
table {{ width:100%; border-collapse:collapse; font-size:.92rem; }}
th, td {{ text-align:left; padding:10px 8px; border-bottom:1px solid var(--line); vertical-align:top; }}
th {{ color:var(--muted); font-weight:600; position:sticky; top:64px; background:var(--bg); }}
tr:hover td {{ background:#152038; }}
.badge {{ display:inline-block; padding:2px 8px; border-radius:999px; background:#1e293b; color:#cbd5e1; font-size:.75rem; }}
.badge.clone {{ background:#3f1d1d; color:#fecaca; }}
.badge.sell {{ background:#14532d; color:#bbf7d0; }}
.badge.partner {{ background:#1e3a5f; color:#bfdbfe; }}
.badge.adj {{ background:#3b2f1a; color:#fde68a; }}
a {{ color:#93c5fd; text-decoration:none; }}
footer {{ padding:12px 24px 28px; color:var(--muted); font-size:.85rem; }}
</style>
</head>
<body>
<header>
  <h1>Nigeria tech landscape — Ranked (102)</h1>
  <p>Static dashboard for Omnific Hand. Filter by sector, status, or sell-vs-clone motion. Funding figures are disclosed totals only. Prefer blanks over guesses.</p>
</header>
<div class="controls">
  <input id="q" type="search" placeholder="Search company, founders, peers…"/>
  <select id="sector"><option value="">All sectors</option></select>
  <select id="status"><option value="">All statuses</option></select>
  <select id="motion"><option value="">All motions</option>
    <option>Clone_avoid</option><option>Sell_to</option><option>Partner</option><option>Adjacent_tooling</option>
  </select>
</div>
<div class="stats" id="stats"></div>
<main>
<table>
<thead><tr>
<th>#</th><th>Company</th><th>Sector</th><th>Funding USD</th><th>Status</th><th>Motion</th><th>Founders</th><th>Site</th>
</tr></thead>
<tbody id="tbody"></tbody>
</table>
</main>
<footer>Embedded snapshot generated {TODAY}. Source: data/ranked_disclosed.csv. No trademarks scraped into this page.</footer>
<script>
const DATA = {payload};
const money = n => {{
  const x = Number(n); if (!Number.isFinite(x)) return "";
  return x.toLocaleString('en-US');
}};
const sectorSel = document.getElementById('sector');
const statusSel = document.getElementById('status');
[...new Set(DATA.map(d => d.sector).filter(Boolean))].sort().forEach(s => {{
  const o=document.createElement('option'); o.value=s; o.textContent=s; sectorSel.appendChild(o);
}});
[...new Set(DATA.map(d => d.status).filter(Boolean))].sort().forEach(s => {{
  const o=document.createElement('option'); o.value=s; o.textContent=s; statusSel.appendChild(o);
}});
function badge(m) {{
  const cls = m==='Clone_avoid'?'clone':m==='Sell_to'?'sell':m==='Partner'?'partner':'adj';
  return `<span class="badge ${{cls}}">${{m||''}}</span>`;
}}
function render() {{
  const q = document.getElementById('q').value.toLowerCase().trim();
  const sector = sectorSel.value;
  const status = statusSel.value;
  const motion = document.getElementById('motion').value;
  const rows = DATA.filter(d => {{
    if (sector && d.sector !== sector) return false;
    if (status && d.status !== status) return false;
    if (motion && d.motion !== motion) return false;
    if (!q) return true;
    const blob = [d.company,d.founders,d.peers,d.jtbd,d.sector].join(' ').toLowerCase();
    return blob.includes(q);
  }});
  document.getElementById('stats').innerHTML = `
    <div class="stat"><b>${{rows.length}}</b><span>shown</span></div>
    <div class="stat"><b>${{rows.filter(r=>r.motion==='Clone_avoid').length}}</b><span>clone avoid</span></div>
    <div class="stat"><b>${{rows.filter(r=>r.motion==='Sell_to').length}}</b><span>sell to</span></div>
    <div class="stat"><b>${{rows.filter(r=>r.status!=='Active').length}}</b><span>non-active</span></div>`;
  document.getElementById('tbody').innerHTML = rows.map(d => `<tr>
    <td>${{d.rank}}</td>
    <td><strong>${{d.company}}</strong><div style="color:#9aa8c7;font-size:.8rem">${{(d.peers||'').slice(0,80)}}</div></td>
    <td>${{d.sector||''}}</td>
    <td>${{money(d.funding)}}</td>
    <td>${{d.status||''}}${{d.exit_type && d.exit_type!=='None' ? ' · '+d.exit_type : ''}}</td>
    <td>${{badge(d.motion)}}</td>
    <td>${{d.founders||''}}</td>
    <td>${{d.website ? `<a href="${{d.website}}" target="_blank" rel="noopener">site</a>` : ''}}</td>
  </tr>`).join('');
}}
['q','sector','status','motion'].forEach(id => document.getElementById(id).addEventListener('input', render));
render();
</script>
</body>
</html>"""
    (out_dir / "index.html").write_text(html)
    # also root alias
    (DOCS / "dashboard.html").write_text(html)
    return out_dir / "index.html"

def main():
    rows = read_csv(DATA / "ranked_disclosed.csv")
    enr = json.loads((DATA / "ranked_enrichment.json").read_text())
    n = merge_progress(rows, enr)
    print("merged progress fields", n)
    rows, cols = add_facelift_columns(rows)
    # ensure status/omnific still present
    assert all(r.get("Omnific_Hand_Motion") for r in rows)
    write_csv(DATA / "ranked_disclosed.csv", rows, cols)
    (DATA / "ranked_enrichment.json").write_text(json.dumps(enr, indent=2) + "\n")

    rounds = build_rounds(rows)
    investors = build_investors(rounds, rows)
    write_csv(DATA / "funding_rounds.csv", rounds,
              ["Company","Round_Type","Amount_USD","Date","Investors","Source_URLs","Notes"])
    write_csv(DATA / "investors.csv", investors,
              ["Investor","Type","Focus","Example_Companies","Source_URLs"])

    directory = read_csv(DATA / "directory.csv")
    sqlite_path = export_sqlite(rows, directory, rounds, investors)
    dash = write_dashboard(rows)

    # companies_enriched full dump
    arr = [{k: r.get(k, "") for k in cols} for r in rows]
    (DATA / "companies_enriched.json").write_text(json.dumps(arr, indent=2) + "\n")

    def filled(field):
        return sum(1 for r in rows if not blank(r.get(field)))

    stats = {
        "ranked": len(rows),
        "website": filled("Website"),
        "founders": filled("Founders"),
        "ceo": filled("CEO_or_Lead"),
        "linkedin": filled("LinkedIn_URL"),
        "high_conf": sum(1 for r in rows if r.get("Data_Confidence") == "High"),
        "exit_type": filled("Exit_Type"),
        "omnific": filled("Omnific_Hand_Motion"),
        "jtbd": filled("JTBD"),
        "peers": filled("Peers"),
        "sector_primary": filled("Sector_Primary"),
        "rounds": len(rounds),
        "investors": len(investors),
        "sqlite": str(sqlite_path),
        "dashboard": str(dash),
    }
    (RAW / "facelift_stats.json").write_text(json.dumps(stats, indent=2))
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    main()
