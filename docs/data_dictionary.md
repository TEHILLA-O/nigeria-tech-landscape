# Data dictionary

Last verified: **2026-09-25**.

## Ranked_Disclosed (`data/ranked_disclosed.csv`)

| Column | Type | Definition |
|---|---|---|
| Rank | int | Position by Total_Disclosed_Funding_USD descending |
| Company | text | Common trading / brand name |
| Sector | text | Fintech, Marketplace, SaaS, Logistics, Healthtech, Edtech, Agritech, Cleantech, AI, Insurtech, Other Tech |
| Product_Summary | text | Short public-product description |
| Website | URL | Primary company site if known |
| LinkedIn_URL | URL | Company LinkedIn if known |
| Twitter_X_URL | URL | Company X/Twitter if known |
| Founders | text | Semicolon-separated founders when public |
| CEO_or_Lead | text | Current CEO or public lead when known |
| HQ_or_Primary_Market | text | Legacy free-text HQ / primary market |
| HQ_City | text | Parsed or researched city |
| HQ_Country | text | Parsed or researched country |
| Operating_Countries | text | Semicolon-separated markets |
| Legal_Entity_Name | text | Registered entity if publicly known |
| Founded_Year | text/int | Founding year if known |
| Company_Status | text | Active / Acquired / Merged / Shutdown / Pivoted / Unknown |
| Exit_Type | text | None / Acquired / Merged / Shutdown / IPO / Unknown. Use None when still independent with no exit event. |
| Acquirer | text | Acquiring company or consortium if Exit_Type is Acquired/Merged; else blank |
| Exit_Year | text | YYYY of exit/IPO when known; blank if Exit_Type is None |
| Exit_Source_URL | URL | Primary public source for the exit/IPO/shutdown claim; blank if none |
| Business_Model | text | B2B / B2C / B2B2C / Marketplace / etc. |
| Target_Customers | text | Who pays or uses |
| Core_Products | text | Semicolon list of main products |
| Tech_Stack_Hints | text | Only if publicly claimed; else blank |
| Employee_Range | text | Public ranges only (e.g. 51-200) |
| Total_Disclosed_Funding_USD | number | Cumulative disclosed funding used for rank |
| Latest_Round_Type | text | Seed / Series A / Series C / Acquisition / IPO path / etc. |
| Latest_Round_Amount_USD | number | Amount for latest sourced round if known |
| Latest_Round_Date | text | YYYY or YYYY-MM |
| Notable_Investors | text | Semicolon-separated investors for notable rounds |
| Valuation_USD | text/number | Public valuation or Undisclosed |
| Valuation_Status | text | Reported / Estimated_by_press / Undisclosed |
| Licence_Types_Held | text | Licences reported as held (verify on registers) |
| Licences_Regs_Needed | text | Typical or specific regulatory hurdles |
| Key_Competitors | text | Peer set |
| Moat_Notes | text | Why replication is hard or easy |
| Ease_to_Replicate | int 1-5 | Hardest=1, easiest=5 for small builder profile |
| Replicate_Notes | text | Narrative ease rationale |
| Replication_Capital_Intensity | text | Low / Med / High |
| Replication_Time_Estimate | text | Rough months/years; labelled estimate |
| Risk_Flags | text | FX, fraud, regulation, unit economics, etc. |
| Opportunity_Angle_for_Builder | text | Where a small automation/ML consultancy could sell |
| Omnific_Hand_Motion | text | Sell_to / Partner / Adjacent_tooling / Clone_avoid (explicit motion for Omnific Hand) |
| Omnific_Hand_Rationale | text | 1-2 sentences judging fit for a small London ML/automation/product-tooling consultancy |
| Data_Confidence | text | High / Med / Low |
| Source_URLs | text | Semicolon-separated sources |
| Last_Verified_Date | date | ISO date of last human/script verification |
| Notes | text | Caveats (optional in some builds) |

## Directory (`data/directory.csv`)

| Column | Type | Definition |
|---|---|---|
| Company | text | Name as listed (legal or brand) |
| Sector | text | Best-fit sector |
| Product_Summary | text | Short blurb (licence category or curated) |
| Website | URL | If findable; often blank for pure regulator rows |
| Regulator_Source | text | CBN / FCCPC / YC / Press / Other |
| Licence_or_Category | text | PSSP, MMO, IMTO, Digital Money Lender, SaaS, etc. |
| Licence_Status | text | Listed / Approved / Unknown |
| HQ_or_Primary_Market | text | Legacy free text |
| HQ_City / HQ_Country | text | When known |
| Founded_Year | text | If known |
| Business_Model | text | Often category default |
| Total_Disclosed_Funding_USD | number | Usually blank |
| Valuation_USD / Valuation_Status | text | Usually Undisclosed |
| Ease_to_Replicate | int | Often heuristic |
| Replicate_Notes | text | Short rationale |
| Licences_Regs_Needed | text | Category default or specific |
| Heuristic | text | Yes if Ease/licences from category defaults |
| Opportunity_Angle_for_Builder | text | Short optional wedge |
| Data_Confidence | text | High / Med / Low |
| Source_URLs | text | Semicolon-separated |
| Notes | text | Optional |
| Last_Verified_Date | date | Verification date |

## funding_rounds.csv

| Column | Definition |
|---|---|
| Company | Company name matching Ranked where possible |
| Round_Type | Seed / Series / Acquisition / IPO path / etc. |
| Amount_USD | Round amount if disclosed |
| Date | YYYY or YYYY-MM |
| Investors | Semicolon-separated |
| Source_URLs | Evidence |
| Notes | Caveats (first close vs final, grant floor, etc.) |

Only real sourced rounds. Incomplete by design.

## investors.csv

| Column | Definition |
|---|---|
| Investor | Name as it appears in sources |
| Type | VC/PE, CVC/Strategic, DFI/CVC, Accelerator, Angel, Other |
| Focus | Short focus note |
| Example_Companies | Companies in this dataset |
| Source_URLs | Evidence |

## companies_enriched.json

Array of Ranked companies as nested objects (funding, valuation, licences, replication, sources) for builders who prefer JSON.
