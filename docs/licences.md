# Nigeria tech licences (plain English)

**Not legal advice.** Application paths below are high-level research notes for builders. Capital, forms, and committees change. Confirm on the live regulator pages before you spend money or make commitments.

Last verified: **2026-09-25**.

## Who regulates what (tech-relevant)

| Regulator | Typical scope in this dataset |
|---|---|
| **CBN** | Payments (PSSP, PTSP, MMO, Super-Agent, Switching), IMTO, banks, MFBs |
| **FCCPC** | Digital money lender registrations; consumer protection |
| **SEC Nigeria** | Investments, funds, digital assets rules as applicable |
| **NAICOM** | Insurance / HMO |
| **NERC** | Electricity, mini-grids, private trading |
| **NITDA / NDPR** | Data protection compliance expectations |
| **NAFDAC** | Food, drugs, related supply chains |
| **CAC** | Company incorporation (baseline for everyone) |

## CBN payments licences (high level)

Common categories appearing in `Directory`:

- **PSSP:** Payment Solution Service Provider (gateway / merchant collections class).
- **PTSP:** Payment Terminal Service Provider (POS/terminal estate).
- **Super-Agent:** Agency banking distribution networks.
- **MMO:** Mobile Money Operator (e-money / wallets).
- **Switching & Processing:** National / scheme switching class.
- **IMTO:** International Money Transfer Operator.

### Typical application path (conceptual)

1. Incorporate at CAC; prepare capital, governance, and compliance manuals.
2. Engage CBN payments licensing process (forms, fit-and-proper, technology and security review).
3. Expect protracted review, possible objections, and ongoing supervisory reporting after approval.
4. Layer PCI-DSS, scheme membership, and bank sponsorship where required.

Exact capital floors and circulars change. Read the current CBN Payments System pages rather than this summary.

## FCCPC digital money lenders

- Many consumer loan apps must register as Digital Money Lenders.
- Registration is **not** a substitute for CBN MFB/banking rights.
- Consumer protection, disclosures, and collections conduct are enforcement themes.
- Directory rows tagged FCCPC are **listed names**, not endorsements of credit quality.

## Banking / MFB

- Taking deposits generally requires a CBN banking or MFB licence and NDIC considerations.
- Neobank UX on a partner bank is a different (still regulated) path from owning a licence.
- Timelines are measured in years, not sprints.

## Securities and wealth products

- Offering investments to the public can trigger SEC Nigeria oversight.
- Wealth apps often partner with licensed fund managers / custodians rather than self-issuing products.

## Insurance / HMO

- Risk-bearing health or insurance products typically need NAICOM authorisation.
- Care-access marketplaces without underwriting face a different (still non-trivial) compliance path.

## Energy

- Mini-grids, embedded generation, and private electricity trading sit under NERC frameworks.
- PAYG solar credit products often combine energy ops with lending partners.

## Data protection

- NDPR-style obligations apply to KYC, health, and consumer fintech data.
- Cross-border transfers and biometrics need careful design.

## Practical builder rule

If the product **holds customer funds**, **extends credit from your balance sheet**, **moves FX**, or **underwrites insurance**, assume you need counsel and a licence plan before build. If the product **sells software to already-licensed firms**, your path is usually CAC + NDPR + commercial contracts.

See also `data/licences_cheat_sheet.csv` and sector notes in `docs/sector_playbooks.md`.
