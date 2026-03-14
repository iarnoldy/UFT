# Dollard Formal Verification

Machine-verified dimensional scaffold from Dollard's versor algebra through Clifford algebras
to SO(16) and E₈, built in Lean 4 with mathlib. 69 proof files, ~2,750+ verified
declarations, zero sorry gaps. Four certified LieHoms composing:
SU(5) →ₗ⁅ℝ⁆ SO(10) →ₗ⁅ℝ⁆ SO(14) →ₗ⁅ℝ⁆ SO(16), plus SO(4) →ₗ⁅ℝ⁆ SO(14).
Remaining chain link (E₈) is dimensional consistency with algebraic upgrade
in progress (see `docs/PROJECT_ROADMAP.md`).
Paper 1 submitted to CICM 2026. Paper 2 submitted to AACA.
Papers 3 & 4 held pending anomaly traces + E₈ chain (ADR-004).

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
11. **Mathlib typeclasses for new Lie algebras.** New Lie algebra constructions MUST include
    `LieRing` and `LieAlgebra ℝ` instances via `Mathlib.Algebra.Lie.Basic`. Use the pattern
    in the `mathlib-lie-upgrade` skill. Existing algebras (Bivector, SL3, SL5, SU5C, SO10) already
    have these instances. SU5C has the project's first certified `LieHom` (→ SO10).

## Upstream (Evidence Source)

- **N-Phase Patent Ready** (separate repository, read-only reference)
- 1194 passing tests (confirmed live 2026-03-07). Provisional patent 63/996,504.
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
| Prose-proof coherence crisis | `docs/decisions/ADR-003-prose-proof-coherence-crisis.md` |
| **Physics-math friction catalog** | `docs/PHYSICS_MATH_FRICTION_CATALOG.md` |
| Paper & proof strategy (Berlinski) | `docs/decisions/ADR-004-berlinski-paper-strategy.md` |
| SO(14) literature survey | `research/so14-gut-literature.md` |
| SO(14) matter decomposition | `src/experiments/so14_matter_decomposition.py` |
| RG coupling unification | `src/experiments/so14_rg_unification.py` |
| Paper 1 (CICM 2026, submitted) | `paper/paper1.tex` |
| Paper 2 (AACA, submitted) | `paper/paper2.tex` |
| Paper 3 (PRD, drafted) | `paper/paper3.tex` |
| Paper 4 (LMP, drafted) | `paper/paper4.tex` |
| Epistemological map | `docs/WHAT_WE_PROVED.md` |
| Mass gap council synthesis | `docs/MASS_GAP_COUNCIL_SYNTHESIS.md` |
| E₈ three-generation proofs | `src/lean_proofs/clifford/` (9 files: spinor_parity_obstruction through massive_chirality_definition) |
| Chirality definition | `src/lean_proofs/clifford/massive_chirality_definition.lean` |
| Proof classification | `docs/PROOF_CLASSIFICATION.md` |
| Signature analysis | `docs/SIGNATURE_ANALYSIS.md` |
| Schur → Killing uniqueness | `src/lean_proofs/spectral/schur_killing_uniqueness.lean` |
| Differential forms (d²=0 from mathlib) | `src/lean_proofs/dynamics/differential_forms.lean` |
| SU(5) compact form (LieAlgebra ℝ) | `src/lean_proofs/clifford/su5c_compact.lean` |
| SU(5) →ₗ⁅ℝ⁆ SO(10) LieHom | `src/lean_proofs/clifford/su5c_so10_liehom.lean` |
| SU(5) as LieSubalgebra of SO(10) | `src/lean_proofs/clifford/su5_subalgebra.lean` |
| **Project roadmap (Papers 3 & 4)** | `docs/PROJECT_ROADMAP.md` |
| SO(14) as LieAlgebra ℝ | `src/lean_proofs/clifford/so14_grand.lean` |
| SO(10) →ₗ⁅ℝ⁆ SO(14) LieHom | `src/lean_proofs/clifford/so10_so14_liehom.lean` |
| SO(4) compact gravity type | `src/lean_proofs/clifford/so4_gravity.lean` |
| SO(4) →ₗ⁅ℝ⁆ SO(14) LieHom | `src/lean_proofs/clifford/so4_so14_liehom.lean` |
| SO(14) bracket generator | `scripts/so14_bracket_gen.py` |
| SU5C bracket generator | `scripts/su5c_bracket_gen.py` |
| Anomaly trace identity [MV] | `src/lean_proofs/clifford/anomaly_trace.lean` |
| SO(16) as LieAlgebra ℝ (120 gens) | `src/lean_proofs/clifford/so16_grand.lean` |
| SO(14) →ₗ⁅ℝ⁆ SO(16) LieHom | `src/lean_proofs/clifford/so14_so16_liehom.lean` |
| SO(16) bracket generator | `scripts/so16_bracket_gen.py` |

## Project Agents and Skills

These agents and skills are specifically built for this project. Use them.

| Task | Agent/Skill | What it does |
|------|-------------|-------------|
| Audit paper claims vs proofs | `paper-integrity-auditor` agent | Maps prose claims to Lean theorems, classifies ACCURATE/OVERCLAIMED/etc. |
| Verify citations against APIs | `citation-verifier` agent | Queries INSPIRE-HEP/Semantic Scholar/CrossRef, detects hallucinated/misattributed citations, populates DOIs |
| Rewrite paper after audit | `paper-rewrite-workflow` skill | 5-layer discipline: Lean speaks, reasoning-as-prose, Ian writes narrative, citations verified, Claude formats |
| Final paper proofread | `paper-proofreader` agent | 5-gate protocol: compilation, math, consistency, bibliography, submission readiness |
| Formal proof writing | `lean4-theorem-proving` skill | Lean 4 patterns, mathlib tactics, proof strategies |
| Lie algebra upgrades | `mathlib-lie-upgrade` skill | Pattern for adding LieRing/LieAlgebra instances |
| Dollard theory questions | `dollard-theorist` agent | PhD-level math: gradients, decomposition properties, versor algebra |
| Clifford algebra construction | `clifford-unification-engineer` agent | so(10), E₈, Lie algebras in Lean 4, Jacobi identities |
| SO(14) breaking chains | `so14-breaking-architect` agent | Symmetry breaking SO(14) → Standard Model |
| SO(14) generations | `so14-generation-specialist` agent | Three-generation problem, spinor decomposition |
| SO(14) Lagrangian | `so14-lagrangian-engineer` agent | Full Lagrangian construction, beta functions |
| SO(14) predictions | `so14-phenomenologist` agent | Proton decay, coupling unification, testable predictions |
| SO(14) signatures | `so14-signature-analyst` agent | Compact vs Lorentzian, Distler ghost objection |
| SO(14) paper writing | `so14-paper-architect` agent | Paper 3 integration, claim tagging, honesty review |
| Chirality problem | `massive-chirality-definition` skill | Open problem: chirality for massive fermions in E₈(-24) |
| Research coordination | `research-orchestrator` agent | Multi-agent workflows, test coverage, git version control |

**Routing rule**: For ANY paper work, follow the pipeline below. For Lean proof work,
use the theorem-proving skill. For physics construction, use the SO(14) specialists.
For cross-cutting coordination, use the research-orchestrator.

## Paper Integrity Pipeline (MANDATORY)

The full pipeline for paper quality is: **AUDIT → CITE-VERIFY → REWRITE → PROOFREAD**.

### Step 1: Integrity Audit
**Delegate to `paper-integrity-auditor` agent BEFORE any paper rewrite or submission.**
The agent runs the `paper-integrity-audit` skill: maps every prose claim to its
supporting Lean theorem, classifies as ACCURATE/OVERCLAIMED/TAUTOLOGICAL/UNSUPPORTED/
SCOPE BLUR/CHAIN GAP/INFLATED/AI TELLTALE/HOLLOW REASONING. Produces a coherence
report + clean skeleton.

### Step 2: Citation Verification
**Delegate to `citation-verifier` agent to verify every citation against live APIs.**
Queries INSPIRE-HEP, Semantic Scholar, CrossRef, arXiv. Classifies each citation as
VERIFIED/METADATA_MISMATCH/NOT_FOUND/HALLUCINATED/MISATTRIBUTED/UNVERIFIABLE.
Populates missing DOIs. Produces corrected .bib entries.

### Step 3: Rewrite (if needed)
Follow the `paper-rewrite-workflow` skill. Five layers:
1. Lean proofs speak (theorem statements extracted accurately)
2. Physics-math reasoning stated plainly (passes Reasoning Test)
3. Ian writes narrative/introduction/conclusion in his voice
4. Citations back the reasoning (verified in Step 2)
5. Claude formats LaTeX, structure only

### Step 4: Proofread
**Delegate to `paper-proofreader` agent for the final check.**
Five-gate protocol (`latex-paper-proofread` skill): compilation, mathematical
correctness, internal consistency, bibliography, submission readiness.
ONE pass, COMPLETE report.
