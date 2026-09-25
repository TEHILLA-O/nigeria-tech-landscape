# Nigeria licences cheat sheet (fintech + tech)

Plain-English map of licences and frameworks that often come up when you try to **replicate** a Nigerian fintech or regulated tech product. Capital figures below come from public counsel summaries of the CBN Dec 2020 payments categorisation circular and may have been updated since - always confirm on the regulator site.

This is not legal advice.

## Company basics

| Item | Regulator | Note |
|---|---|---|
| Incorporation | CAC | You need a Nigerian company (or local subsidiary) before most operating licences. |
| Personal data | NDPC (NDPR / NDPA) | Applies to almost every startup handling customer data. |

## CBN payments categories (Dec 2020 framework)

| Licence | Can hold customer funds? | Typical use | Min capital (public summaries) |
|---|---|---|---|
| Switching and Processing | No (not as MMO) | National rails, card processing, non-bank acquiring | N2 billion |
| Mobile Money Operator (MMO) | **Yes** | Wallets, e-money, pool management | N2 billion |
| PSSP | No | Payment gateways, merchant aggregation | N100 million |
| PTSP | No | POS terminals and merchant support | N100 million |
| Super-Agent | No | Agent network management | N50 million |
| PSS composite | No | Combo of Super-Agent + PTSP + PSSP | N250 million |
| Regulatory Sandbox | Per approval | Time-bound product tests | Case-by-case |

If you want **both** Switching and MMO activities, CBN expects a **Payments Service Holding Company (PSHC)** structure with ring-fenced subsidiaries (non-operating holdco).

Sources: [Aspen Sahel explainer](https://aspensahel.com/2021/09/new-license-categorisations-for-the-nigerian-payments-system/), [AElex on PSHC](https://aelex.com/analysing-cbns-guidelines-for-licensing-and-regulating-payment-service-holding-companies/), [CBN](https://www.cbn.gov.ng/).

## Banking and lending

| Path | Regulator | Note |
|---|---|---|
| Microfinance Bank (MFB) | CBN | Common for digital lenders (FairMoney-class, Moniepoint lineage). Capital varies by unit/state/national tier. |
| Commercial / merchant bank | CBN | Hardest path for neobanks (Kuda-class). |
| Deposit insurance | NDIC | For deposit-takers. |

## Other sector regulators

| Topic | Regulator | Typical products |
|---|---|---|
| Investments, crowdfunding, some digital assets | SEC Nigeria | Cowrywise / Risevest-class; crypto platforms depending on activity |
| Insurance / HMO | NAICOM | Reliance Health-class |
| Telecom / VAS / short codes | NCC | Comms-adjacent products |
| Drugs, food, medical products | NAFDAC | Healthtech supply, food processing |
| Electricity / mini-grids / trading | NERC | Cleantech (Konexa trading licence class) |

## Practical takeaway for builders

- **SaaS / tooling / KYC UX / billing automation**: often CAC + NDPR + a licensed PSP partner. Highest ease scores in this dataset.
- **Payment gateway**: PSSP (or partner under a licensed entity) + PCI + bank integrations.
- **Wallet / agent network**: MMO and/or Super-Agent/PTSP stack, float, and distribution. Hard.
- **Neobank / lender**: MFB or full bank path. Hardest.
- **Insurance / energy trading / pharma**: sector regulator first, software second.

CSV mirror: `data/licences_cheat_sheet.csv`.
