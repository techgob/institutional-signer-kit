# Institutional Signer Kit

**A public institution signs on Stellar without ever holding XLM.**

[Español](README.es.md) · [Statement of Work](docs/statement-of-work.md) · Apache-2.0

---

## The problem

No Peruvian municipality can buy, custody or account for a crypto asset just to pay network fees. Doing so requires a procurement process, a budget line, key-custody rules and reporting to the Comptroller, and it conflicts with the single-treasury-account principle. The administrative cost of enabling the payment exceeds the payment itself by orders of magnitude.

That is where most public-sector blockchain pilots die — before any architecture discussion.

## What this does

Soroban solves it at the protocol level: authorization entries are signed independently from the transaction envelope, so the authorizer and the fee payer can be different accounts.

This repository packages that property as a reusable component:

- **role-and-cycle signing** — keys belong to offices and terms, not to people;
- **policy-restricted relayer** — the payer can only submit whitelisted contract calls, with spend caps;
- **fee-to-authorization traceability** — every fee paid is linked to the signed entry behind it;
- **portable authorization** — signed entries are published, so any third party can submit them. The operator runs the registry; it cannot censor it.

For the institution: zero XLM, no budget line, no asset custody, and an authorization bounded in scope and time.

## Proof it works

| | |
|---|---|
| Fee-payer separation on testnet | [`8ba16039…7e5f`](https://stellar.expert/explorer/testnet/tx/8ba160396082e0ac29dc0324e96a119a90f99c2e9fd9a10aa2941746c14e7e5f) |
| Role-signed authorization, published as XDR and relayed by a third party | [`fb284c5b…b8dd`](https://stellar.expert/explorer/testnet/tx/fb284c5b28ce79738db571107c0f8ce0906fd7d48bb39b09e1282d0c2a64b8dd) |
| Interactive walkthrough of the cycle, with the real evidence | [signerkit.govtechpe.work](https://signerkit.govtechpe.work) |
| Demo video (1:41) | [youtu.be/Pel8UScd8x4](https://youtu.be/Pel8UScd8x4) |

## Validated on a real case

Two Peruvian municipalities running the legally mandated participatory budget, chosen as opposite extremes:

| | Tocache (province) | La Punta (district) |
|---|---|---|
| Publication | No minutes or final reports | Five consecutive cycles online |
| Signature | Handwritten, then scanned | Seven digital certificates |
| Investment budget 2025 | S/ 41.3M | S/ 2.7M |
| 2025 execution | 74.9 % | 90.9 % |

Neither lacks spending capacity. Both lack a chain of evidence linking what citizens agreed to with what was actually done.

## Run it

```bash
pip install "jsonschema[format]"

# data contract: 7 test cases, must all pass
python3 data-contract/validar_ingesta.py --pruebas

# validate a real ordinance against the schema
python3 data-contract/validar_ingesta.py data-contract/ejemplo_ordenanza_001-2026-MPT.json

# local verifier and conformance: 7 test cases
python3 -m unittest discover verifier
```

The second command reports the ordinance as `observado` and lists 16 inconsistencies found in the real document. That is the expected result: the validator blocks anchoring until the hash is verified against the official source.

To reproduce the signature without XLM on testnet (HU-01), an operator handover and passkey rotation per cycle, follow `signer-kit/README.md`. To check that an operator's transactions conform, see `verifier/README.md`. To check a document against its commitment, see `verifier/README.md`.

## Repository map

| Path | Contents |
|---|---|
| `signer-kit/` | The component: authorization signing and relayer |
| `contracts/` | Soroban contracts: cycle genesis and guards |
| `data-contract/` | JSON Schema with per-field admission rules, two-layer validator, test cases |
| `planning/` | Sprint plan as validated data, not prose |
| `evidence/` | Hashes and links to official documents and transactions |
| `docs/` | Statement of Work, state machine, data protection rule, architecture decisions |
| `demo/` | Static walkthrough of the eight milestones, built from the specification and the recorded evidence |

## Status

**Done, self-funded (~45 design hours):** state machine derived article by article from both municipalities' regulations; data contract with per-field admission rules; two-layer validator with 7 test cases; forensic analysis of both entities' documents; testnet proof of concept of fee-payer separation.

**Scope of this Instaward request:** Signer Kit v1 packaged and documented; cycle registry T0–T8 on testnet with guards; ingestion v2 handling both document profiles; citizen verifier; user research with both municipalities.

**Not in scope yet:** tokenization, project substitution, role-and-cycle multisig, Programa del Vaso de Leche profile, mainnet, external audit.

## Data protection by design

Only documents that are public by legal mandate are anchored. Never personal data. Keys belong to roles and cycles, not to persons. The schema enforces this structurally: unknown fields are rejected, and field names suggesting personal data fail validation. See [docs/proteccion-datos.md](docs/proteccion-datos.md).

## License and credits

Apache-2.0. See [AUTHORS.md](AUTHORS.md).

Built by [TechGob](https://techgob.cl) — TECH GOB CONSULTORA EN TRANSFORMACIÓN DIGITAL Y TECNOLOGÍAS EMERGENTES SpA, Chile.
