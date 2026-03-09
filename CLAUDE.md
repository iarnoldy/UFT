# Dollard Formal Verification

Formal verification of Eric Dollard's versor algebra using Lean 4.
Separates verified mathematics from unsubstantiated claims.

## Research Tracks

- **Track A (Primary)**: Methodology -- Lean 4 as a tool for verifying alternative/fringe math
- **Track B**: Mathematical analysis -- where Dollard = standard math, where he errs
- **Track C**: Physics claims -- documented, requires extraordinary evidence, not centered
- **Track D**: Candidate Theory Construction -- SO(14) phenomenology
  - GATE-CONTROLLED: explicit gates between phases (Ian decides go/stop)
  - KILL-CONDITION-FIRST: cheapest falsification before expensive construction
  - HONEST FRAMING: every claim tagged [MV], [CO], [CP], [SP], or [OP]
  - Pre-registered as Experiment 4 in `docs/experiments/EXPERIMENT_REGISTRY.md`

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

### First-time setup (free, open-source)
```bash
# Install elan (Lean version manager) -- Linux/macOS/WSL
curl https://elan-init.lean-lang.org/elan-init.sh -sSf | sh

# Fetch mathlib (takes a few minutes first time)
lake update
```

### Building
```bash
lake build                    # compile all proofs
lake env lean src/lean_proofs/foundations/basic_operators.lean  # single file
```

### Key files
- `lakefile.lean` -- build configuration (srcDir: `src/lean_proofs`)
- `lean-toolchain` -- pins Lean version

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
7. **Kill conditions execute.** If a pre-registered kill condition fires, the experiment
   is OVER. Document as negative result and stop. No rationalizing.
8. **Candidate physics is NOT verified math.** Never conflate [CP] with [MV]. The scaffold
   proves algebraic identities; it does NOT prove that SO(14) describes nature.
9. **Signature matters.** SO(14,0) (compact, Cl(14,0)) vs SO(11,3) (Lorentzian) must be
   explicitly addressed in any physics construction. The Lean proofs use compact signature.
10. **Three-generation problem.** If theory predicts N != 3 generations, this requires
    explanation with a concrete mechanism, not hand-waving.

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
| Why construct a candidate theory? | `docs/decisions/ADR-002-candidate-theory-construction.md` |
| SO(14) literature survey | `research/so14-gut-literature.md` |
| SO(14) matter decomposition | `src/experiments/so14_matter_decomposition.py` |
| RG coupling unification | `src/experiments/so14_rg_unification.py` |
| Proton decay predictions | `src/experiments/so14_proton_decay.py` |
| SO(14) Lagrangian | `docs/so14_lagrangian.md` |
| Selection principle (why SO(14)?) | `docs/so14_selection_principle.md` |
| Candidate theory paper | `paper/so14_candidate_theory.tex` |
