# Dollard Formal Verification -- Where Truth Lives

Formal verification of Eric Dollard's versor algebra using Lean 4 theorem prover.

## What This Project Is

A methodology study: can Lean 4 rigorously evaluate mathematical claims from
alternative/fringe sources? We apply it to Dollard's versor algebra and telegraph
equation framework.

## What This Project Found

| Claim | Verdict | Evidence |
|-------|---------|----------|
| h,j,k are 4th roots of unity | VERIFIED (trivial) | `src/lean_proofs/foundations/basic_operators.lean` |
| Telegraph expansion (R+jX)(G+jB) | VERIFIED (standard) | `src/lean_proofs/telegraph/telegraph_equation.lean` |
| Four-factor independence | VERIFIED (standard) | `src/lean_proofs/telegraph/telegraph_equation.lean` |
| Versor form equivalence | DISPROVED | `src/lean_proofs/telegraph/telegraph_equation.lean:85-92` |
| Polyphase/Fortescue formula | NOT YET VERIFIED | Experiment 0 (blocking) |
| Physics claims (aether, over-unity) | UNFALSIFIABLE | No formal backing |

## What This Project Is Not

- Not a validation of Dollard's Unified Field Theory
- Not evidence for aether, over-unity, or E=mc2 replacement
- Not an academic paper (yet) -- it's a research scaffold

## Quick Start

```bash
# Requires Lean 4 + mathlib
lake build
lake env lean src/lean_proofs/foundations/basic_operators.lean
```

## Navigation

| Question | File |
|----------|------|
| Project rules and north star | `../CLAUDE.md` |
| Architecture overview | `ARCHITECTURE.md` |
| How to contribute | `CONTRIBUTING.md` |
| Full audit report | `audit/AUDIT_FINDINGS.md` |
| Claim-by-claim triage | `../analysis/CLAIM_TRIAGE.md` |
| Why we reframed | `decisions/ADR-001-honest-reframing.md` |
| Experiment registry | `experiments/EXPERIMENT_REGISTRY.md` |

## Research Tracks

- **Track A**: Lean 4 methodology for alternative math verification (primary, novel)
- **Track B**: Mathematical content analysis (where Dollard = standard math, where he errs)
- **Track C**: Physics claims (documented, not centered, requires extraordinary evidence)
