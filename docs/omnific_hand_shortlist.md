# Omnific Hand shortlist

Filter of `Ranked_Disclosed` for outreach and partnering. Built for Tehilla / Omnific Hand (small London ML, automation, and product-tooling consultancy), not for a bank with unlimited capital.

## Who is on it

Include a ranked company when `Omnific_Hand_Motion` is one of:

- **Sell_to**: realistic vendor / ISV / ops-tooling buyer
- **Adjacent_tooling**: do not clone the core product; sell a thin wedge beside it
- **Partner**: product, data, or distribution partnership lane

Exclude **Clone_avoid** unless the motion is also Partner (it never is). Capital-heavy licensed rails, dense agent networks, and balance-sheet products stay off this list on purpose.

Current row count: see `data/omnific_hand_shortlist.csv` (also sheet `Omnific_Hand_Shortlist` in the xlsx, and table `omnific_hand_shortlist` in the sqlite).

## Columns

| Column | Use |
|---|---|
| Rank | Funding rank from the main sheet (context only; not outreach priority) |
| Company | Brand name |
| Sector_Primary | Coarse sector |
| Omnific_Hand_Motion | Sell_to / Adjacent_tooling / Partner |
| Omnific_Hand_Rationale | Why that motion |
| JTBD / ICP | Job to be done and who buys |
| Website / Careers_URL | Public entry points |
| Last_Signal_Date / Possibly_stale | Freshness hygiene before you write |
| Outreach_One_Liner | One natural sentence you could send. Edit before sending. Not a mail-merge blast. |

## How to use

1. Open `data/omnific_hand_shortlist.csv` or the xlsx sheet.
2. Sort or filter by motion. Start with **Sell_to** where `Possibly_stale` is No or Unknown and a careers or founder LinkedIn exists on the ranked sheet.
3. Click through Website and `Source_URLs` on the full ranked row before any commercial claim.
4. Personalise `Outreach_One_Liner`. Keep it short. No em dashes. Do not paste the same line to fifty inboxes.
5. Prefer founder LinkedIn or a warm intro over cold careers forms when a public founder URL exists on Ranked.
6. Re-run ranking hygiene after big funding news; this shortlist is a cut of Ranked, not a separate truth.

## What this is not

- Not investment advice.
- Not a licence to invent funding, founders, or LinkedIn URLs.
- Not a guarantee the company wants vendors. Motions are research scores for a small consultancy profile.

See also: [data dictionary](data_dictionary.md), [methodology](methodology.md), [sector playbooks](sector_playbooks.md).
