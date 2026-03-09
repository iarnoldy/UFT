# ADR-002: SO(14) Candidate Theory Construction

## Status

Proposed (Phase 0 in progress)

## Context

The machine-verified algebraic scaffold (35 Lean 4 files, 878 theorems, 0 sorry)
establishes SO(14) as a mathematically well-defined structure with dimension 91,
decomposing as 45 (gauge/SO(10)) + 6 (gravity/SO(4)) + 40 (mixed). The natural
question: can we construct a candidate physical theory from this scaffold?

Key tensions identified during planning:

1. **SO(14,0) vs SO(11,3)**. The proofs use compact SO(14,0) (Clifford algebra
   Cl(14,0)), but physics requires Lorentzian signature for the gravity sector.
   The `so14_unification.lean` file (line 200) notes this explicitly. This is
   itself a kill condition (KC-3).

2. **Generation count**. The 128-spinor of Spin(14) likely gives 4 copies of
   the 16-spinor under SO(10) × SO(4), not the observed 3 generations. This
   must be confronted honestly (KC-4).

3. **Claim conflation risk**. Machine-verified algebra [MV] must never be
   conflated with candidate physics [CP]. The scaffold proves algebraic
   identities; it does NOT prove that SO(14) describes nature.

## Decision

Construct an SO(14) candidate theory using gate-controlled, kill-condition-first
methodology (Experiment 4 in the registry).

### Methodology

- **Kill conditions first**: Test the cheapest falsification before investing in
  expensive construction. Coupling unification (Phase 1) costs one Python script.
  If it fails, we stop before writing a Lagrangian.

- **Gate-controlled**: Ian makes go/stop decisions at each phase boundary.
  No proceeding past a gate without explicit approval.

- **Honest tagging**: Every claim tagged with its epistemic status:
  - [MV] Machine-verified (Lean 4 proof compiles)
  - [CO] Computed (Python/SymPy, reproducible)
  - [CP] Candidate physics (proposed, not verified)
  - [SP] Standard physics (textbook result)
  - [OP] Open problem (acknowledged gap)

- **Negative results are publishable**: If a kill condition fires, the documented
  negative result ("SO(14) fails coupling unification because...") is itself a
  contribution.

### What this is NOT

- NOT a claim that SO(14) is correct
- NOT a promotion of fringe physics
- NOT an extension of Dollard's algebra (which collapsed to Z_4)
- NOT ignoring known problems (generations, signature, gravity action)

### What this IS

- A systematic exploration of whether SO(14)'s algebraic properties translate
  to viable phenomenology
- An application of the machine-verified scaffold to a concrete physics question
- An exercise in honest, kill-condition-first theory construction

## Consequences

### If successful (all gates pass):
- Publishable candidate theory paper (arXiv:hep-ph)
- Track D added to research program
- Novel contribution: SO(14) with Clifford-algebraic scaffold + Fortescue-Coxeter connection

### If killed:
- Publishable negative result documenting which kill condition fired
- Still validates the methodology (Lean 4 + kill-condition-first)
- Scaffold remains valid mathematics regardless of physics outcome

### Risks:
- Overclaiming: mitigated by tagging system and kill conditions
- Wasted effort: mitigated by cheapest-first ordering
- Confirmation bias: mitigated by pre-registered falsification criteria

## Related

- ADR-001: Honest Reframing (establishes the intellectual honesty standard)
- Experiment 4 in EXPERIMENT_REGISTRY.md (pre-registered protocol)
- Mass Gap Council findings (docs/MASS_GAP_COUNCIL_SYNTHESIS.md)
