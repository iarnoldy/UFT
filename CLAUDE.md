# Dollard Formal Verification

Formal verification of Eric Dollard's versor algebra using Lean 4.
Separates verified mathematics from unsubstantiated claims.

## Research Tracks

- **Track A (Primary)**: Methodology -- Lean 4 as a tool for verifying alternative/fringe math
- **Track B**: Mathematical analysis -- where Dollard = standard math, where he errs
- **Track C**: Physics claims -- documented, requires extraordinary evidence, not centered

## Directory Structure

| Directory | Contains | Boundary |
|-----------|----------|----------|
| `src/lean_proofs/` | Lean 4 proof files | Only checked-in code that compiles |
| `src/experiments/` | Python experiment runners | Pre-registered before execution |
| `src/tests/` | Test suite | REAL/PROPERTY/SMOKE classification |
| `source_materials/` | Dollard PDFs + N-Phase evidence catalog | Read-only reference |
| `analysis/` | Claim triage, verification results | Updated only with evidence |
| `docs/` | Architecture, audit, decisions | Living documentation |
| `research/` | Polymathic research notebooks | Created by polymathic-researcher |

## Build & Run

```bash
# Check basic operator proofs
lake build   # requires lakefile.lean at project root

# Run individual proof files
lake env lean src/lean_proofs/foundations/basic_operators.lean
lake env lean src/lean_proofs/telegraph/telegraph_equation.lean
```

## Development Rules

1. **Pre-register before executing.** No experiment runs without a registered hypothesis
   and falsification criteria in `docs/experiments/EXPERIMENT_REGISTRY.md`.
2. **Falsification > confirmation.** Design experiments to disprove, not to confirm.
3. **No inflated language.** "Verified" means Lean accepted the proof. "Consistent"
   means no contradiction found. Never "EXTRAORDINARY SUCCESS" for standard arithmetic.
4. **Claims cite proofs or are marked UNVERIFIED.** Every claim in analysis/ must link
   to a Lean proof file, N-Phase test evidence, or carry an explicit UNVERIFIED/DISPROVED/UNFALSIFIABLE tag.
5. **Honest error reporting.** When Lean rejects a proof, that is a finding, not a failure.
6. **Track C claims require extraordinary evidence.** Physics claims (aether, over-unity,
   E=mc2 replacement) stay in Track C with UNFALSIFIABLE or EXTRAORDINARY tags.

## Upstream (Evidence Source)

- **N-Phase Patent Ready** (`C:\Users\ianar\Documents\CODING\March_2026\N_Phase_Patent_Ready`)
- READ-ONLY. 1194 passing tests (confirmed live 2026-03-07). Provisional patent 63/996,504.
- Provides computational validation (tests) and empirical validation (real datasets)
- Evidence catalog: `source_materials/N_PHASE_EVIDENCE.md`

## Downstream (Dependency)

- **N-Phase signal processing system**: depends on Track B verified mathematics
- Sync protocol: VERIFIED claims safe to depend on, DISPROVED claims must remove dependency

## Where Truth Lives

| Question | File |
|----------|------|
| What claims survive audit? | `analysis/CLAIM_TRIAGE.md` |
| What did verification actually prove? | `analysis/VERIFICATION_RESULTS.md` |
| What are the Lean proofs? | `src/lean_proofs/` |
| Why did we reframe? | `docs/decisions/ADR-001-honest-reframing.md` |
| Full audit report | `docs/audit/AUDIT_FINDINGS.md` |
| What experiments are planned? | `docs/experiments/EXPERIMENT_REGISTRY.md` |
| Primary sources | `source_materials/` |
| N-Phase computational evidence | `source_materials/N_PHASE_EVIDENCE.md` |
| Original claim inventory | `analysis/MATHEMATICAL_CLAIMS_EXTRACTION.md` |
