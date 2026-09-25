# Sector playbooks

Practical notes for builders evaluating Nigeria opportunities. **Not legal advice.** Licence names and capital change; confirm on regulator sites.

Last verified: **2026-09-25**.

## Fintech: payments / acquiring / wallets

**Typical licences:** CBN PSSP, PTSP, Super-Agent, MMO, Switching & Processing; PCI-DSS; NDPR.

**Capital intensity:** High for licensed acquiring and wallets (float, agents, compliance). Med for software layered on partner PSPs.

**Replicate difficulty:** 1-2 for licensed networks; 3-4 for checkout UX on Paystack/Flutterwave APIs.

**Example companies in dataset:** Flutterwave, Paystack, Moniepoint, OPay, PalmPay, Interswitch, Nomba, Paga, Zone.

**Builder wedge:** Reconciliation, dispute automation, merchant plugins, agent analytics, AML transaction monitoring sold **to** PSPs and their merchants. Do not attempt unlicensed e-money.

## Fintech: lending / BNPL / DML

**Typical licences:** FCCPC Digital Money Lender registration; CBN MFB for deposit-taking lenders; credit bureaus; consumer protection; NDPR.

**Capital intensity:** High (book funding). Software decisioning is separate from balance sheet.

**Replicate difficulty:** 2-3 for FCCPC DML apps (crowded, collections-sensitive); harder for MFB.

**Examples:** FairMoney, Carbon, CredPal, Migo; hundreds of FCCPC DML directory rows.

**Builder wedge:** Ethical collections SaaS, underwriting feature stores, model monitoring, affordability checks. Reputation risk is real.

## Fintech: banking / MFB / neobank

**Typical licences:** CBN banking or Microfinance Bank; NDIC; card schemes; NDPR.

**Capital intensity:** Very high.

**Replicate difficulty:** 1. App UX is not the product.

**Examples:** Kuda, Moniepoint (MFB path), FairMoney MFB, Aladdin Digital Bank, Trade Lenda (aspirant).

**Builder wedge:** Sell compliance ops, onboarding automation, and credit tooling to licensed MFBs; do not raise a bank yourself.

## Fintech: remittance / FX / multi-currency

**Typical licences:** CBN IMTO (Nigeria payouts); foreign MSB/EMI; AML/CFT; NDPR.

**Capital intensity:** High (liquidity + licences).

**Replicate difficulty:** 2.

**Examples:** LemFi, Grey, Afriex, Raenest, VertoFX, Waza.

**Builder wedge:** Payout orchestration, compliance case management, FX exposure dashboards.

## SaaS / HR / data

**Typical licences:** CAC; NDPR; payroll tax integrations for HR.

**Capital intensity:** Low to Med.

**Replicate difficulty:** 4-5 for workflow SaaS; distribution is the hard part.

**Examples:** SeamlessHR, Stears, Billboxx, Youverify, BFREE.

**Builder wedge:** Highest fit for a London automation/ML consultancy. Custom modules, integrations, and vertical AI on top of HRIS / data products.

## Logistics / mobility / delivery

**Typical licences:** State transport permits; insurance; CAC; NDPR. Okada rules vary by city.

**Capital intensity:** Med-High (fleet, riders, working capital).

**Replicate difficulty:** 2-3; city politics can kill passenger bike models.

**Examples:** MAX.ng, Kobo360, Gokada, Chowdeck, Renda.

**Builder wedge:** Routing, dispatch, telematics, demand forecasting sold to operators.

## Healthtech

**Typical licences:** Facility licences; NAICOM for HMO/insurance; NAFDAC for pharma/labs; health data / NDPR.

**Capital intensity:** Med-High (clinical sales + possible facilities).

**Replicate difficulty:** 2-3 for EMR/HMO; higher for clinics networks.

**Examples:** Helium Health, Reliance Health, Field, Intron Health, MDaaS Global, Axmed.

**Builder wedge:** Clinical NLP (African accents), claims automation, interoperability connectors, lab LIS.

## Edtech

**Typical licences:** CAC; NDPR (minors); education standards if school-integrated.

**Capital intensity:** Low-Med (content cost matters).

**Replicate difficulty:** 3-4.

**Examples:** uLesson, Talstack.

**Builder wedge:** Assessment analytics, adaptive learning, employer upskilling LMS.

## Energy / cleantech

**Typical licences:** NERC mini-grid / electricity rules; EPC; consumer credit partners; CAC.

**Capital intensity:** High (hardware + project finance).

**Replicate difficulty:** 1-2 for assets; 3 for monitoring software.

**Examples:** Lumos Global, Starsight Energy, Rensource, Arnergy, Husk Power Systems, Konexa, SunFi, Rivy.

**Builder wedge:** Remote monitoring, PAYG collections, credit scoring for solar lenders, MRV for climate finance.

## Talent / HR marketplaces

**Typical licences:** CAC; labour/immigration; NDPR.

**Capital intensity:** Med (brand + recruiting ops).

**Replicate difficulty:** 2-3.

**Examples:** Andela; SeamlessHR on the software side.

**Builder wedge:** Skills assessment ML, interview automation, Nigeria-market recruiting ops tooling.

## Cross-cutting builder advice

1. Sell **to** regulated incumbents before competing with them.
2. Use licensed PSPs for payments; never hold customer funds without a licence.
3. Treat FCCPC DML crowding as a warning, not an opportunity to clone another loan app.
4. Prefer SaaS, data, verification, collections ethics, and ops automation wedges scored Ease 3-5.
