# Instawards Statement of Work (SOW)

## Institutional Signer Kit: Sign without holding — 30-Day Scoped Engagement

*A public institution signs on Stellar without ever holding XLM.*

---

## 1. Problem Statement & Objective

### Problem Being Addressed

No Peruvian municipality can buy, custody or account for a crypto asset just to pay network fees. Doing so requires a procurement process, a budget line, key-custody rules and reporting to the Comptroller, and it conflicts with the single-treasury-account principle. The administrative cost of enabling the payment exceeds the payment itself by orders of magnitude. That is where most public-sector blockchain pilots die, before any architecture discussion.

The effect shows up in real portfolios. In a joint workshop with Peru's SGTD, TechGob mapped 23 public challenges from 25 entities. In a network analysis for prototype implementation produced by TechGob for SGTD, this obstacle led to permissioned networks being preferred because they do not force the entity to hold an asset. Stellar (recommended for its native capabilities in 2 of 23 challenges) cannot be ruled out on technical grounds, and this project provides the component it needs to compete with the other networks. It also gives the authority evidence that measures the cost per transition and per cycle, together with technical documentation of who pays, who signs and what happens if the operator disappears. *(The portfolio analysis is working material with SGTD; available to the review committee under NDA.)*

The participatory budget, which municipalities are legally mandated to carry out, shows why the missing piece matters. Stellar can already answer **who received** a payment. Nobody answers **who decided, by which act and under which rule**. In the two pilot municipalities that evidence is a scanned PDF with no integrity (Tocache) and a natively digital decree with seven valid signatures but no qualified timestamp or long-term validation data (La Punta). Neither municipality lacks spending capacity. Both lack a chain of evidence linking what citizens agreed to with what was actually done.

Today there is no reusable component that lets a public entity, together:

- sign with keys that belong to offices and terms, as Peru's Personal Data Protection Law N.° 29733 requires;
- delegate fee payment to an operator that **cannot** use its payer role for anything else;
- audit every fee the operator paid;
- keep working if the operator disappears or refuses to submit;
- have the network reject an administrative step that the law does not allow.

The first four conditions are built and tested. The fifth is the object of this sprint.

### Objective

Within 30 days TechGob will deliver, on Stellar Testnet:

1. **Signer Kit v1**, complete, packaged and documented, with all five relayer refusal cases run on testnet and `sign-auth-entry` generalized to any contract and function;
2. the **cycle registry T0–T4** with guards G1, G2, G6 and G7, where a skipped legal step fails on the network, plus the **milestone certificate** demonstrated with a consumer contract;
3. the **two real cycle openings on testnet**, one per municipality, covering both genesis variants the law produces;
4. the **live verifier and fee measurement over T0–T4**, reproducible by a third party without TechGob's intervention.

**Definition of success:** two distinct institutional role keys, each holding 0 XLM, open and advance two real legal cycles up to T4; a transition that skips a step is rejected by the network; and an external reviewer reproduces fingerprint, commitment and fee of at least one transition per municipality using only the repository and the walkthrough.

---

## 2. Project & Team Information

| Field | Value |
|---|---|
| Project Name | Institutional Signer Kit |
| Applicant | TECH GOB CONSULTORA EN TRANSFORMACIÓN DIGITAL Y TECNOLOGÍAS EMERGENTES SpA (TechGob), Chile |
| Builder / Team | Nadinne Canto Novoa (@techgob) — Product Owner (scope, prioritization, acceptance of deliverables; state machine derived from the legal framework; data contract; institutional relations) · Kevin Alexander Soto Burgos (@kasbsquall) — Developer (technical architecture, Soroban implementation, signer–payer separation, ingestion and verifier) |
| Primary Contact | Nadinne Canto |
| Ambassador Chapter | [to be confirmed] |
| Ambassador Chapter Lead | [to be confirmed] |
| Repository | https://github.com/techgob/institutional-signer-kit (Apache-2.0, CI enabled) |
| Interactive walkthrough | https://signerkit.govtechpe.work |
| Demo video | https://youtu.be/Pel8UScd8x4 (1:41) |
| Network | Stellar Testnet (Soroban) |
| Field validation partners | Municipalidad Provincial de Tocache (San Martín) and Municipalidad Distrital de La Punta (Callao), Peru, with access enabled by the National Network of Digital Innovation Labs of Peru's Secretariat of Government and Digital Transformation (SGTD-PCM) |
| Date Submitted | November 2026 |
| Suggested Sprint Start Date | 9 November 2026, subject to award resolution and Chapter Lead confirmation |
| Duration | 30 days (4-week sprint) |
| Requested Budget | USD 5,000 |

---

## 3. Instawards Overview & Intent

### 3.1 Purpose

This Instaward puts the **Institutional Signer Kit** to work: an open, reusable component that lets a public institution authorize Soroban invocations with **zero XLM, no budget line and no asset custody**.

Soroban signs authorization entries independently from the transaction envelope, so the authorizer and the fee payer can be different accounts. The kit packages that property in four pieces. **All four are built, with passing automated tests.** The fourth, the policy-restricted relayer, was built with self-funded work during the application window and is not charged to this Instaward.

The administrative process the kit is put to work on is the participatory budget cycle that Peruvian law makes mandatory, modelled as a state machine from the real municipal documents of two municipalities. The result is the cycle registry announced at the end of the demo video: a contract where **a transition that skips a legal step is rejected by the network**, and where each completed step produces a **milestone certificate — a precondition a disbursement can require**.

With the kit already built, this sprint concentrates on the one block with no executed precedent: the registry's guards, over the first stretch of the cycle (T0 to T4), with both real cycle openings on testnet. What follows is proposed as subsequent sprints, exactly as the programme's rules contemplate (section 7).

### 3.2 Starting point: what is already public and verifiable

The sprint starts from working evidence. Every item below is in the repository, in the interactive walkthrough or in the video, at commit `e2d374e` or later.

**The four pieces of the kit**

| Piece | Status today | Evidence |
|---|---|---|
| 1. Role-and-cycle signing — keys belong to offices and terms, not people | **Proven on testnet.** Classic role account with 0 XLM and sponsored reserve; passkey contract account whose key rotates per cycle while the role address stays fixed | HU-01 run; passkey run P-1 to P-4 (`evidence/transacciones.md`) |
| 2. Policy-restricted relayer — payer can only submit whitelisted calls, with spend caps and rate limits | **Built, with nine passing automated tests in CI** (`signer-kit/test_relayer.py`): refusal of a non-whitelisted contract, a non-whitelisted function, a role outside the policy, the rate limit, an excessive estimated fee, an expired signature and the spend cap, plus the accepted path. **Three of those cases were run on testnet** (R-1 to R-3): a whitelisted invocation the operator paid, a refusal by function and a refusal by spend cap. **What remains is running the non-whitelisted-contract and rate-limit refusals on testnet**; today they are proven against a network double | PR #11; `signer-kit/test_relayer.py`; `evidence/transacciones.md`, section "Relayer con política restringida"; raw logs in `evidence/relayer/` |
| 3. Fee-to-authorization traceability — every fee linked to the signed entry behind it | **Proven**, keyless, over confirmed transactions (checks C1 to C6) | `verifier/conformidad.py`; R-1 returned conformant |
| 4. Portable authorization — any third party can submit a published entry; the operator cannot censor | **Proven on testnet**: entry B published as XDR and submitted by a third party; replay of entry A rejected | tx `fb284c5b…b8dd`; tx `ac8f406c…0542` (`Error(Auth, ExistingValue)`) |

The distinction between "proven in automated tests" and "run on testnet" is kept throughout this document, because it is the one a reviewer can check independently. The relayer does not touch the network in order to refuse: by design a refusal is decided before the fee is estimated and produces no transaction, so its evidence is the line in `evidence/relayer/rechazos.jsonl` and the fact that the operator paid nothing.

**Recorded testnet transactions**

Thirteen in total: account creation with sponsored reserve, HU-01 (entry A, entry B, replay), operator handover (T-1, T-2), passkey rotation (P-1 to P-4) and the relayer run (R-1 to R-3). The invocation paid by the relayer is `544f62f8…dbb8`, ledger 5,066,171, **13,666 stroops charged against 23,811 estimated**, with the role at 0 XLM. Operator handover is already a configuration change, not a migration: the role key and the contract stay the same.

**The cycle registry, specified and tested off-chain**

| Asset | Status today |
|---|---|
| State machine: 14 transitions T0–T13 grouped in 8 milestones, guards G1–G12, substitution rules R1–R7, two genesis variants | Specified (`docs/maquina-estados.md`); shown milestone by milestone in the walkthrough |
| Guards | **Specified, contract not deployed** |
| Data contract with per-field admission rules and two-layer validator | 7 test cases passing in CI, including the personal-data case that must fail |
| Existing Soroban contracts (`ejemplo` and `cuenta-passkey`) | With their own tests, running in CI since PR #11 |
| Ingestion against a real document | **T0 only**: Tocache ordinance 001-2026-MPT, result `observado` with 16 inconsistencies (1 blocking, INC-01: hash computed on a copy, not on the direct portal download) |
| Local verifier (PDF hash + canonical commitment) | Working, with tests |
| Decision to enforce transitions with Soroban contracts | ADR-001 accepted |

### 3.3 Maturity-level declaration

This section exists so the reviewer does not have to infer it. The project contains two objects at different maturity levels, and conflating them would mean reading more into this application than it promises.

The scale is the European Commission's technology readiness levels: nine levels, where the third is literally "experimental proof of concept", the fourth "technology validated in lab", the fifth "technology validated in relevant environment", the sixth "technology demonstrated in relevant environment" and the seventh "system prototype demonstration in operational environment" (European Commission, 2014).

| Object | At sprint start | At sprint close |
|---|---|---|
| **Signer Kit**, the reusable component | 4: all four pieces built with passing automated tests, three of them run on testnet | **5**, with the signing pieces defensible at 6: all five policy checks run on the network, an invocation to a contract other than the example one, installable from a clean clone by a third party |
| **Cycle registry**, the application | 2: state machine specified, contract not deployed, ingestion validated on T0 only | **5** for the T0–T4 stretch: contract deployed, four guards executed on the network, and two real openings with legal documents from two entities |

**Why this is above a proof of concept.** A proof of concept answers whether something is possible, under conditions chosen by whoever builds it, with data it may invent, without anyone else needing to be able to repeat it, and without measuring its cost. This sprint forbids itself all five: the conditions are set by the law, and the two genesis variants exist because the law produces them; the documents are real and their fingerprints are verified against the direct download from the official portal; an external reviewer reproducing fingerprint, commitment and fee without TechGob's intervention is an acceptance criterion, not an aspiration; cost is measured per transition, per cycle and per variant; and failure modes are documented and tested, including what happens if the operator disappears or refuses to submit. To that add what no proof of concept produces: a multi-year state-rent policy, an architecture decision with the thresholds that would reverse it (ADR-001), and a report that lets a public entity decide.

**And why it is no more than that.** It is not a pilot: no entity operates it and no administrative procedure depends on it. It is not a minimum viable product: the planning and budget office has no surface to use it yet, and that begins with the sprint-2 user research. It confers no legal validity: the registry documents facts, it does not rule on legality and does not substitute for the qualified timestamp that La Punta's documents lack. The stretch covered is five of fourteen transitions and four of twelve guards.

**What this declaration enables.** The programme's rules exclude funding "vague exploration, unbounded research, or long-term roadmap funding" and ask for a concrete technical deliverable with criteria evaluable at close. Declaring the level is how this application shows it is the latter. It also opens the funding path that follows: Peru's state instrument for technological development requires projects with an "entry level of TRL 4 or 5 and an exit level of TRL 6 or higher" (PROCIENCIA, 2025). The three-sprint sequence in section 7 therefore leaves the component exactly in the band the State funds on its own. The Instaward is not the end of the funding path: it is the step that makes a public instrument reachable.

**Sources for this section**

- European Commission. (2014). *Horizon 2020 – Work Programme 2014-2015. General Annexes, Annex G: Technology readiness levels (TRL)* (Decision C(2014)4995). https://ec.europa.eu/research/participants/data/ref/h2020/wp/2014_2015/annexes/h2020-wp1415-annex-g-trl_en.pdf
- PROCIENCIA. (2025). *Bases del concurso Proyectos de Desarrollo Tecnológico E041-2026-03*. Consejo Nacional de Ciencia, Tecnología e Innovación Tecnológica. https://prociencia.gob.pe/wp-content/uploads/2026/Proyectos%20de%20Desarrollo%20Tecnol%C3%B3gico%202026-03/20251030_Bases-PDT-2026%5BF%5D%5BF%5D.pdf

---

## 4. Scope of Work

The stretch this sprint covers:

| T0 | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| ordinance | in force | convened | accreditation | workshop |

In the interactive walkthrough these are milestones 1 to 3 (Genesis, Call, Workshop). Milestones 4 to 8 (T5–T13) remain specified and belong to the subsequent sprints described in section 7.

### Deliverable 1 — Signer Kit v1, complete

**Build:**

- `sign-auth-entry` generalized to any contract function. Today the scripts invoke `registrar(rol, huella)` and `signer-kit/README.md` states the limit: "No hay todavía un `sign-auth-entry` genérico"
- Testnet runs of the two remaining relayer refusal cases: **non-whitelisted contract** and **rate limit**. The code and its tests already exist and pass; what is added is the real run, with its line in `evidence/relayer/rechazos.jsonl` and its row in `evidence/transacciones.md`
- An invocation authorized by a role holding 0 XLM to a **contract other than the example contract**, submitted and paid by the relayer, with the conformance checker returning C1 to C6 conformant
- Operator handover and conformance checker packaged as kit commands
- Installation guide and "use it with your own contract" guide (`require_auth()` on the role)

**Acceptance criteria:**

- All five relayer refusal cases — contract, function, role, rate, spend cap — are run on testnet, each with its log entry and its evidence row
- A role account with 0 XLM authorizes a call to a contract other than the example contract; the relayer submits and pays; the conformance checker returns C1 to C6 conformant
- A published entry is submitted by a third-party account
- The kit installs and runs from a clean clone following only the README

**Why this matters:**
This is the reusable piece for any Stellar builder serving a public entity. What an auditor checks is not that the relayer works, but that it is demonstrated it **cannot** act outside its policy. The automated tests demonstrate that against a network double; the testnet run demonstrates it against the real network. The deliverable closes when both exist.

---

### Deliverable 2 — Cycle registry T0–T4 with guards, and both real openings

**Build:**

- Soroban registry contract implementing T0 to T4 in order: **a transition that skips a legal step is rejected by the network**
- Guards:
  - **G1** open cycle — no transition without a previously opened cycle
  - **G2** unique key — ubigeo + ordinance number + fiscal year; a second opening is rejected
  - **G6** dual timestamp — declared act date compared with the ledger timestamp; retroactive records flagged
  - **G7** acts before entry into force — alert raised, transition accepted (the registry documents facts and does not rule on legality)
- Role authorization per transition through the Signer Kit, with the signer prescribed for each step in `docs/maquina-estados.md`
- Storage decision documented **before** any guard is written: what is stored persistently and what only as a fingerprint. ADR-001 disables the contract's upgrade path, so this decision admits no correction after the first real opening
- Every guard written first as a pure predicate with its test vectors, like the data contract's seven cases, and ported to Rust afterwards
- Both genesis variants the law produces, each with its real opening on testnet: **(A) single ordinance**, Tocache ordinance 001-2026-MPT; **(B) framework ordinance plus annual mayoral decree**, La Punta decree 002-2026-MDLP/AL
- INC-01 closed: fingerprints recalculated on the direct download from the official portal, registered by two distinct roles
- **Milestone certificate**: a read-only query returning, for a cycle and a transition, whether the step is completed, its document fingerprint, its signer role and its ledger. Demonstrated with a minimal consumer contract that refuses to act unless the milestone exists. No funds move
- State-rent policy: what is stored persistently and what only as a fingerprint, the TTL extension strategy and its cost

**Acceptance criteria:**

- Automated tests fail on the network for: skipped step, duplicate cycle, transition without a cycle, wrong signer role
- Every guard has, besides its refusal test, a passing test for the valid case: a guard that refuses everything is not a guard
- No real opening is recorded before the storage decision has been exercised on the network against a disposable test cycle
- Both real openings confirm on testnet, one per genesis variant, signed by **two distinct role keys holding 0 XLM**; the duplicate opening is rejected
- The consumer contract succeeds when the milestone exists and fails when it does not
- `evidence/documentos.md` marks both documents' fingerprints as "verified against the source"
- No anchored payload contains personal data; the privacy test case still fails as designed
- Upgrade path disabled or gated by more than one key, as ADR-001 requires

**Why this matters:**
Detecting an invalid step afterwards is not the same as preventing it. The milestone certificate is the link the ecosystem lacks between an administrative act and a disbursement: **verifiable act → certified milestone → disbursement**. And the two genesis variants are not decoration: they are the proof that the registry models the law rather than one particular municipality.

---

### Deliverable 3 — Live verifier, fee measurement and report to the authorities

**Build:**

- **Report on costs and on the mechanism for the competent authorities**, addressed to SGTD and both municipalities: measured cost per transition, per cycle and per genesis variant; who signs and who pays at each step; what happens if the operator disappears; and what the entity would have to decide in order to operate it on its own. This is the document that turns technical evidence into an administrative decision that can actually be taken

- **Live verifier over T0–T4**: the walkthrough at signerkit.govtechpe.work moves from recorded evidence to live reads for this stretch. A person downloads a document from the official portal and the page checks (1) its SHA-256 fingerprint and (2) the canonical commitment against the ledger. It remains a static page with no backend
- Update of the piece-2 label in the walkthrough and of the labels of the delivered guards, each linked to its transaction
- **Fee measurement**: actual fee of every T0–T4 transaction, total per cycle and per genesis variant, and state-rent cost over a multi-year horizon, published in the repository
- End-to-end QA from a clean clone, with CI green across its four jobs
- Updated demo video showing the registry rejecting a skipped step on testnet
- Mainnet readiness note: audit path (OpenZeppelin Stellar Contracts modules and an application to the Soroban Security Audit Bank), rent budget, admin-key governance, operator handover to the SGTD lab
- Interview guide and scheduled sessions with both planning and budget offices, so sprint 2 opens with the interviews ready to happen. The sessions themselves and the requirements document belong to sprint 2, not to this one

**Acceptance criteria:**

- An external reviewer reproduces the fingerprint, commitment and fee of at least one transition per municipality **without TechGob's intervention**, following only the README
- Fee report published with figures taken from transaction hashes, not estimated
- Report on costs and mechanism delivered to SGTD and both municipalities, with every figure referred to its transaction hash and no estimates
- No claim in the walkthrough, the kit README or this SOW contradicts another at sprint close
- Readiness note lists the ADR-001 thresholds that would reverse the use of contracts
- Interview guide closed and sprint-2 sessions scheduled, or the refusal or non-response recorded in writing

**Why this matters:**
The registry is only as trustworthy as a citizen's ability to check it alone, and the sustainability argument needs a measured cost, not an estimate.

---

### Out of scope for this sprint

The following is specified and proposed as subsequent sprints (section 7), not promised in this one:

- Transitions T5 to T8 and guards G8 and G10
- Ingestion of La Punta's five published cycles (2023–2027)
- User research with the planning and budget offices, and field work
- The complete citizen verifier, with cycle history in plain language
- Project-level transitions T9 to T13 and substitution with rules R1 to R7
- Tokenization: a non-transferable token per project on SEP-50
- Programa del Vaso de Leche profile
- Role-and-cycle multisig and therefore guard G9

Excluded from the whole programme as it currently stands:

- Mainnet deployment and external security audit
- Any value transfer, stablecoin or disbursement. The milestone certificate is demonstrated with a consumer contract that moves no funds
- Passkey ceremony with a hardware authenticator in the browser
- Integration with SIAF, SEACE or the MEF application
- Storage of documents on-chain or in the repository; personal data at any stage

---

## 4.2 Deliverable-Aligned Budget Request

**Requested Budget: USD 5,000** · Single rate of USD 20/hour for the whole team · 215 hours

### By category

| Category | Item | Hours | Amount | Share |
|---|---|---|---|---|
| **Core team** | Soroban development | 120 | USD 2,400 | 48% |
| | Product, deliverable review and institutional management | 95 | USD 1,900 | 38% |
| | **Subtotal** | **215** | **USD 4,300** | **86%** |
| **Technology & Operations** | Infrastructure | — | USD 250 | 5% |
| | Network fees and state rent | — | USD 150 | 3% |
| | Contingency | — | USD 300 | 6% |
| | **Subtotal** | — | **USD 700** | **14%** |
| **Total** | | **215** | **USD 5,000** | **100%** |

The contribution-and-distribution agreement ties the 120 hours of Soroban development to the scope of the current work plan and provides that **if during execution the scope were to exceed them, the parties agree in writing before any additional hours are worked**, deciding in that same act whether they are paid, the scope is reduced, or the work is deferred to the next stage. This SOW is that current work plan.

### The 120 hours of Soroban development

Distribution by task, derived from the deliverables in section 4. The total is what is committed; the split across tasks is the Product Owner's planning and may shift between tasks during execution without changing the total.

| Task | Hours | Deliverable |
|---|---|---|
| `sign-auth-entry` generalized to any contract function | 12 | D1 |
| Testnet run of the non-whitelisted-contract and rate-limit refusals, with their logs and evidence rows | 5 | D1 |
| Invocation to a contract other than the example contract, submitted and paid, with the conformance checker conformant C1 to C6 | 6 | D1 |
| Operator handover and conformance checker packaged as kit commands | 4 | D1 |
| Installation guide and "use it with your own contract" guide | 3 | D1 |
| Soroban registry contract covering T0 to T4 in order, with role authorization on every transition | 18 | D2 |
| Guards G1, G2, G6 and G7, each with its refusal test and its valid-case test | 16 | D2 |
| Milestone certificate and consumer contract that refuses to act unless the milestone exists | 10 | D2 |
| Both genesis variants and both real openings on testnet | 10 | D2 |
| State-rent policy and TTL extension strategy | 6 | D2 |
| Live verifier over T0–T4 and updated walkthrough labels | 14 | D3 |
| Fee measurement per transition, per cycle and per variant | 5 | D3 |
| End-to-end QA from a clean clone, with CI green | 5 | D3 |
| Updated demo video showing a skipped step rejected | 3 | D3 |
| Mainnet readiness note | 3 | D3 |
| **Total** | **120** | |

The heaviest stretch is the registry contract with its guards: 44 of the 120 hours, and the only block with no executed precedent. If those hours fall short, the week-3 checkpoint decides, and the adjustment is agreed in writing before any additional hours are worked.

### The 95 hours of product, deliverable review and institutional management

These are not coordination hours. They are the work that turns code into a registry that models the law, and they are itemized because a reviewer is entitled to know what is being bought:

| Task | Hours | Basis |
|---|---|---|
| Deliverable review and pull-request approval | 40 | 2 hours daily over 20 working days |
| Obtaining and verifying the municipal documents of both municipalities, including closing INC-01 against the direct portal download | 20 | Two entities, two genesis variants, dual registration by distinct roles |
| Report on costs and on the mechanism for the competent authorities: SGTD and both municipalities | 15 | Drafting, checking every figure against transaction hashes, and presentation |
| Acceptance of deliverables, pull-request approval of changes to the state machine, and closing report to the Chapter Lead | 12 | Three deliverables with evaluable criteria, plus sprint close |
| Interview guide and scheduling of the sprint-2 sessions with both planning and budget offices | 8 | Preparation, without running the sessions |
| **Total** | **95** | |

**Why review carries 40 hours.** That is 40 hours of review against 120 of development, a one-to-three ratio, higher than is usual in software development. The reason is ADR-001: in this iteration the contract's upgrade path is disabled or gated by more than one key, so a rule carried over incorrectly from the law cannot be fixed with a later patch. Every transition and every guard derives from an article of the law, and it is the Product Owner, not the developer, who verifies that correspondence. The review does not judge code quality: it checks that an automated test exists for every acceptance criterion, that the test's values match the specification's, and that no files enter the repository that no criterion asked for.

The report on costs and mechanism is a deliverable, not an annex. The project's argument is that a public entity can use Stellar without holding XLM; that only becomes an administrative decision once the authority receives the measured cost per transition and per cycle, together with the explanation of who pays, who signs, and what happens if the operator disappears. Without that report the sprint produces technical evidence nobody in the State can act on.

### By deliverable

| Deliverable | Development (h) | Product, review & institutional (h) | Team cost | Direct costs | Total |
|---|---|---|---|---|---|
| D1 — Signer Kit v1, complete | 30 | 15 | USD 900 | — | USD 900 |
| D2 — Registry T0–T4 with guards and both real openings | 60 | 42 | USD 2,040 | — | USD 2,040 |
| D3 — Verifier, fees and report to the authorities | 30 | 38 | USD 1,360 | — | USD 1,360 |
| Cross-cutting | — | — | — | USD 700 | USD 700 |
| **Total** | **120** | **95** | **USD 4,300** | **USD 700** | **USD 5,000** |

**On the network-fees and state-rent line (USD 150).** On testnet XLM comes from friendbot and fees carry no monetary cost: the measured fee of a role-authorized invocation is 13,666 stroops. The line covers what can actually cost money inside the sprint: the TTL extensions the state-rent policy requires when tested over a long horizon, refunding the operator account if a run has to be repeated after a testnet reset, and a possible mainnet smoke test if the readiness note recommends one and the Product Owner approves it. **If it is not used it is not spent, and it is reported as unexecuted at close**, with the detail of fees paid taken from `evidence/relayer/comisiones.jsonl`. No fee is ever paid with a public entity's funds: that is the point of the project.

**How this scope was set.** On the recommendation of the person who decides within the ambassador chapter which projects are submitted to the Instaward, the project was evaluated with Stellar Raven, the server that gives AI agents Stellar's documentation and ecosystem context. That review remains in the repository history with its sources (`docs/revision-postulacion.md`, commit `6bb92c6`), the verbatim quotes from the programme's rules are in `docs/instawards-reglas.md`, and it concluded that the earlier plan was oversized for 30 days. This version's scope answers that review: three deliverables instead of four, none whose closure depends on a third party's signature, and every withdrawn item reappears in section 7 with the sprint that recovers it.

**The agreement between the parties.** The relationship between TechGob and the developer is set out in a contribution-and-distribution agreement signed before work begins. It declares what each party contributes before any funding exists, how the amount is distributed if the Instaward is granted, the mechanics and deadline of that distribution, the authorship each party declares, the confidentiality of the working material with SGTD, and what happens if either party withdraws. It is not part of what the application requires, so it is kept outside the repository; it is available to the Chapter Lead or to SDF on request.

**Prior self-funded work, not charged to this Instaward.** About 45 hours designing the state machine and the data contract; the 15 hours of preparation sprint S00; and the construction of the policy-restricted relayer, its nine automated tests, the documented interface, the testnet run and the evidence rows of PR #11. **The hours of that last item are declared `SIN DATO`**: the only thing observable in the repository is the commit window of PR #11, 2 hours 18 minutes on 7 October 2026 for 17 files and 1,543 lines, of which close to 900 are documentation and evidence. That window is elapsed time between commits, not hours worked, so the figure comes from whoever did the work and not from this document.

---

## 5. 30-Day Execution Plan

Monday–Friday working calendar, Peru. The plan is kept as schema-validated data in `planning/` and checked in CI, like sprint S00.

### Week 1 — The two architecture decisions

The two tasks everything else depends on, and the only ones that cannot be corrected late.

- `sign-auth-entry` generalized to any contract function, which is how the registry authorizes by role
- The registry's storage decision, documented
- A vertical skeleton of T0 with G1, G2 and the milestone-certificate query, deployed on testnet **against a disposable test cycle**, never against a real municipal document
- The guards written as pure predicates with their test vectors

**Expected Output**
The storage model settled and exercised on the network. Because ADR-001 disables the contract's upgrade path, this is the last point at which the design admits change.

**Checkpoint (end of week 1):** if the storage decision or the T0 skeleton are not settled and tested on the network, the contract design is reconsidered with a month ahead rather than a week. No real opening is recorded before this point is cleared.

### Week 2 — The cycle and its guards

- T1 to T4 in order, with the signer the state machine prescribes for each step
- **G7 before G6.** G7 is the only guard that accepts the transition and raises an alert, so it requires an observation channel that is not a refusal; if the contract has none, that is a design change and it surfaces here
- G6 last, since it only needs the ledger timestamp
- Consumer contract that refuses to act unless the milestone exists

**Expected Output**
A skipped step, a duplicate cycle, a transition without a cycle and a wrong role, all rejected by the network, each guard with its refusal test and its valid-case test.

### Week 3 — The two real openings and the kit close-out

- Genesis variants A and B on the now-stable contract
- Tocache's cycle and La Punta's cycle opened on testnet, with two distinct role keys at 0 XLM
- INC-01 closed on direct portal downloads
- State-rent policy
- Kit close-out, which does not depend on the registry: testnet runs of the non-whitelisted-contract and rate-limit refusals, the invocation to a contract other than the example one, packaging and guides

**Expected Output**
Two real legal cycles opened and advanced to T4, each with its genesis variant; all five relayer refusal cases run on testnet; the kit installable from a clean clone.

**Checkpoint (end of week 3):** if a guard turns out not to be implementable as specified, the change is proposed by pull request with its justification and approved by the Product Owner. Rules derived from the law are not dropped for implementation convenience. If one municipality's opening is blocked by a missing document, it is reported as pending and never filled with assumptions: D1 and D3 are not cut.

### Week 4 — Verify, measure and report

- Live verifier over T0–T4 and updated walkthrough labels
- Fee measurement per transition, per cycle and per variant
- Report on costs and mechanism for SGTD and both municipalities
- End-to-end QA, documentation and updated video
- Mainnet readiness note
- Interview guide and scheduling of the sprint-2 sessions

**Expected Output**
A reviewer verifies the full T0–T4 chain in both municipalities from the repository and the walkthrough alone; fee report published; report on costs and mechanism delivered to the authorities.

---

## 6. Evidence of Completion

### Deliverable 1

- Tagged release of Signer Kit v1 in the repository
- Rows R-4 and R-5 of `evidence/transacciones.md`: non-whitelisted-contract and rate-limit refusals run on testnet, with their lines in `evidence/relayer/rechazos.jsonl`
- Testnet hash of the invocation to a contract other than the example contract, and of the third-party submission
- Conformance checker output (C1 to C6)

### Deliverable 2

- Testnet contract ID of the registry
- Hashes of both real openings and of the rejected duplicate opening
- Hash of a rejected skipped step
- Test report per guard, with the refusal case and the valid case, linked to CI
- Consumer contract hashes, with the milestone present and absent
- `evidence/documentos.md` with both fingerprints verified against the source
- State-rent policy document

### Deliverable 3

- Live verifier at signerkit.govtechpe.work for T0–T4
- Documented walkthrough of an independent verification per municipality
- Fee report per transition, cycle and variant
- Report on costs and mechanism, with delivery acknowledgement from SGTD and both municipalities
- Updated demo video
- Mainnet readiness note
- Interview guide and confirmation of the sessions scheduled for sprint 2
- Repository with CI green across its four jobs

### Evidence Verification Checklist

| Deliverable | Evidence Present | Partial | Missing |
|---|---|---|---|
| D1 — Signer Kit v1, complete | ☐ | ☐ | ☐ |
| D2 — Registry T0–T4 and both real openings | ☐ | ☐ | ☐ |
| D3 — Verifier, fees and report to the authorities | ☐ | ☐ | ☐ |

### Definition of Done (every deliverable)

- Reproducible from a clean clone by following the README
- No keys or secrets in the code, not even testnet ones
- No output contains personal data
- Every cited link opens and shows what the text claims; where the repository records no value, it says `SIN DATO` instead of estimating
- Anything proven against a network double is declared as such and never as run on testnet
- CI green on the release commit

---

## 7. Alignment with the Following Sprints

The programme's rules contemplate up to two follow-on disbursements, with a cumulative cap of USD 15,000 paid in XLM, each with its own sprint, the previous one completed and confirmed by the Chapter Lead. They are not automatic. The sequence TechGob proposes, with scope already specified in the repository:

| Sprint | Scope | What it enables |
|---|---|---|
| **1 — this Instaward** | Signer Kit v1 complete; registry T0–T4 with G1, G2, G6 and G7; both real openings; milestone certificate; verifier, fees and report to the authorities over T0–T4 | The reusable kit, the proof that the network can reject an invalid administrative step, and the measured cost in the hands of whoever decides |
| **2** | T5 to T8 with guards G8 and G10; ingestion of La Punta's five published cycles; field user research with both municipalities' planning and budget offices, with the interviews already scheduled in sprint 1 | The full cycle-level process, validated against a real historical series and against the requirements of those who operate it |
| **3** | Complete citizen verifier; project-level transitions T9 to T13 with substitution R1 to R7; Programa del Vaso de Leche profile | The registry reaches the executed project and extends to the first benefit programme, with deliveries attested by community committees, no money moving on-chain and no access to beneficiary rolls |

**Why the Vaso de Leche committees.** The programme's committees are the best possible witness: they do not need to interpret a case file to know whether a delivery arrived, and they are the only ones with a direct incentive to report when it does not.

Across all three sprints TechGob pays the fees. After that the operator role moves to the SGTD Digital Innovation Lab, and the handover already proven on testnet makes that a configuration change. The path to mainnet goes through an external audit and an SCF Build Award application.

---

## 8. Success Metrics

| Metric | Today | Target this sprint |
|---|---|---|
| Kit pieces built with passing automated tests | 4 of 4 | 4 of 4 |
| Relayer refusal cases run on testnet | 2 of 5 | 5 of 5 |
| Invocation to a contract other than the example contract | No | Yes, paid by the relayer and conformant C1 to C6 |
| Guards executed on testnet | 0 | 4 (G1, G2, G6, G7) |
| Genesis variants with a real opening on testnet | 0 | 2 (single ordinance; framework ordinance plus annual decree) |
| Distinct institutional role keys signing with 0 XLM | 1 | 2, one per municipality |
| Cycle transitions registered | T0 in ingestion only | T0 to T4 where the source document exists |
| Invalid transitions rejected by the network | 0 | 100% of test cases |
| Fee per transition, per cycle and per variant | One isolated measurement | Measured and published |
| Independent third-party verifications | 0 | ≥ 1 per municipality |
| Entities receiving the report on costs and mechanism | 0 | 3 (SGTD and both municipalities) |
| Personal data in anchored payloads | 0 | 0 |

---

## 9. Risks, Dependencies & Mitigations

| Risk or dependency | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Chapter and Chapter Lead unconfirmed.** The rules require identifying the Chapter Lead accompanying the application, and active chapter participation | High | Blocking | The two pending fields in section 2, chapter and Chapter Lead, are completed before submission. The 9 November start date is subject to that confirmation |
| **KYC before disbursement.** The rules require completing SDF's KYC before any disbursement, and may require repeating it, or the organization's KYB, during the award | Medium | High | The KYC link and the list of documents are requested from the Chapter Lead **before the application is submitted**, and the entity's documentation is assembled in advance. SDF does not publish that list, so it is confirmed rather than assumed. The work plan does not depend on disbursement to begin |
| Municipal documents delayed: publication record of the Tocache ordinance, public versions without an identity-document column | Medium | Medium | Requests issued at sprint start. Missing transitions are reported as pending and never filled with assumptions |
| Testnet reset breaking explorer links. Official documentation indicates 2 to 4 resets per year, at 17:00 UTC, announced at least two weeks ahead; the next scheduled one is 16 December 2026 | Low within the sprint | Low | The sprint closes before that date. Every run is scripted and dated, and the summaries with hashes, ledgers and fees are versioned in the repository, so a broken link does not erase the evidence |
| State-rent cost underestimated | Medium | High | The rent policy is part of D2 and its cost is measured in D3, with the fee line as backstop |
| A guard cannot be implemented as specified | Low | Medium | Change proposed by pull request and approved by the Product Owner; rules derived from the law are not dropped for convenience |
| Single operator concentrates power | Low | High | Entries are published and any third party can submit them; handover already proven; target operator is the SGTD lab |
| Personal data reaches the chain | Low | High | Admission rule per field, private by default, structural rejection, two-layer validator and a dedicated failing test |
| Early work declared proven to a different standard than the rest | Medium | Medium | No claim in this SOW declares as "run on testnet" what is only proven against a network double. Every run has its hash in `evidence/transacciones.md`, its automated test and CI green |

---

## 10. Data Protection & Security

- Only documents that are public by legal mandate are anchored. Never personal data, and never the hash of a personal identifier.
- Keys belong to roles and cycles, not to people.
- The schema enforces it: every field declares its admission rule; undeclared fields default to off-chain; unknown fields and field names suggesting personal data fail validation. The test case that tries to anchor personal data must fail, and does fail in CI.
- No secrets in the repository; scripts read keys from the Stellar CLI keystore.
- Framework: Peru Law N.° 29733 and Supreme Decree N.° 016-2024-JUS. The registry does not replace each entity's own data-protection assessment.

---

## Annex — Consistency with the public artifacts

| Claim in this SOW | Repository | Video | Walkthrough |
|---|---|---|---|
| Sign without holding XLM | README, HU-01 evidence | Title and opening | Pieces 1, 3, 4 marked proven |
| All four pieces built with passing tests | `signer-kit/relayer.py`, `signer-kit/test_relayer.py`, CI | — | **Piece 2: label to be updated** |
| Two relayer refusal cases still to be run on testnet | `evidence/transacciones.md`, R-1 to R-3; `signer-kit/README.md` | — | Piece 2, scope note |
| Scope T0–T4 with four guards | README, "Scope of this Instaward request" | "05 · next · the cycle registry, in development" | Milestones 1 to 3 |
| Skipped legal step rejected by the network | `docs/maquina-estados.md`, ADR-001 | "skips a legal step → rejected by the network" | Guard descriptions |
| Milestone certificate | `docs/statement-of-work.md` | "milestone certificate — a precondition a disbursement can require" | — |
| Two genesis variants | `docs/maquina-estados.md`, genesis section | — | Milestone 1 |
| Designed on real Peruvian municipal documents | `evidence/documentos.md`, data contract | "Está diseñado sobre documentos municipales reales del Perú" | 16 inconsistencies of the Tocache ordinance |

**Consistency items to settle before submitting.** This annex claims the SOW does not contradict the public artifacts. Five things must be aligned first:

1. `demo/index.html`, line 568: piece 2 is still labelled "No implementado · lo financia esta iteración". It must say it is built and tested, with the two refusal cases pending a testnet run.
2. The repository README declares the application's scope as T0–T8. It must say T0–T4 and point to section 7 for the rest.
3. `planning/` must carry this iteration's sprint with the T0–T4 scope and the hour distribution of section 4.2, validated by its schema, as S00 is. The contribution agreement ties the 120 development hours to the scope of the current work plan, so that file is what makes the limit enforceable.
4. `docs/acuerdo-aportes-y-distribucion.md` in the public repository is a half-filled template, with the split left blank. Section 4.2 states that the effective agreement is signed and kept outside the repository, so the template contradicts the SOW itself and must be removed from the repository. While it is there, a third party reads an incomplete agreement and takes it for the current one.
5. `docs/statement-of-work.md` in the repository is the previous version of this SOW, with the T0–T8 scope and four deliverables. It must be replaced with this version, because it is the file the walkthrough and this annex cite as the source.

---

## Resumen ejecutivo en español

**Institutional Signer Kit: firmar sin poseer.** Componente abierto que permite a una entidad pública firmar en Stellar sin tener XLM, sin partida presupuestal y sin custodiar activos. Soroban firma la autorización por separado del sobre de la transacción, así que quien autoriza y quien paga pueden ser cuentas distintas.

**Punto de partida.** Las cuatro piezas del kit están construidas y con pruebas automatizadas que pasan en integración continua. Trece transacciones quedan registradas en testnet. Del relayer con política restringida se corrieron en testnet tres casos —una invocación pagada y dos rechazos—; los rechazos por contrato no permitido y por límite de frecuencia están probados contra un doble de la red y les falta la corrida real. La máquina de estados (T0–T13, ocho hitos) está especificada; las guardas no tienen contrato desplegado y la ingesta solo está validada en T0, con 16 inconsistencias en la ordenanza real de Tocache.

**Lo que financia esta instaward (USD 5 000, 30 días, testnet):**

| Semana | Entregable | Criterio clave |
|---|---|---|
| 1 | Signer Kit v1 completo | Los cinco rechazos del relayer corridos en testnet; una invocación a un contrato distinto del de ejemplo, pagada por el relayer |
| 2 | Registro T0–T4 con G1, G2, G6 y G7 | Paso omitido, ciclo duplicado, transición sin ciclo y rol equivocado, rechazados por la red |
| 3 | Las dos aperturas reales y el certificado de hito | Dos ciclos legales abiertos en testnet, uno por variante de génesis, con dos claves de rol en 0 XLM |
| 4 | Verificador en vivo, medición de comisiones e informe a las autoridades | Un tercero verifica huella, compromiso y comisión sin intervención de TechGob; la SGTD y ambas municipalidades reciben el costo medido y el mecanismo |

**Presupuesto:** 215 horas a USD 20 (USD 4 300, 86 %) más infraestructura, comisiones de red y renta de estado, y contingencia (USD 700, 14 %). Las 120 horas de desarrollo son las acordadas entre las partes y no cambian; las 95 horas de producto, revisión de entregables y gestión institucional incluyen 40 de revisión de entregables y visado de pull requests, y 15 del informe de costos y del mecanismo para las autoridades. El reparto del acuerdo del 4 de octubre se mantiene: USD 2 400 y USD 2 600.

**Fuera de alcance de este sprint, y propuesto como sprints 2 y 3 dentro del tope acumulado de USD 15 000:** T5 a T13, ingesta de los cinco ciclos de La Punta, investigación de usuario, verificador ciudadano completo, tokenización, multifirma y el perfil del Vaso de Leche. Los comités del programa son el mejor testigo posible: no necesitan interpretar un expediente para saber si la entrega llegó, y son los únicos con incentivo directo para reportar cuando no llega.
