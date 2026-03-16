# SO(14) Breaking Chains Research -- Recovered from Session Transcripts

## Source
Recovered from JSONL session transcripts on 2026-03-14.
Primary sessions: `22571151-c83d-482c-8ee8-1d07656f6997`, `6223dc4c-d8a5-484d-babb-b751340a8840`,
`66eca1d1-a5c7-4f46-99ab-03b03068bb3a`, `c90c995a-d4f6-456e-b329-bf5894b05d9a`.
Also: `research/so14-gut-literature.md` (comprehensive literature survey, 2026-03-08).

## Summary

The `so14-breaking-architect` agent was defined in session `c90c995a` and registered in CLAUDE.md as
responsible for "Symmetry breaking SO(14) -> Standard Model." No dedicated subagent runs of this
agent were found in the JSONL transcripts -- the breaking chain research was conducted primarily
through the polymathic-researcher agent (producing `research/so14-gut-literature.md`) and through
the main session thread in `22571151` (the Bridge implementation session).

## Findings

### 1. SO(14) Adjoint Decomposition under SO(10) x SO(4)

The adjoint representation (91-dimensional) decomposes as:
```
91 = (45, 1) + (1, 6) + (10, 4)
```
- **(45, 1)**: SO(10) adjoint -- 45 gauge bosons (GUT sector)
- **(1, 6)**: SO(4) adjoint -- 6 gauge bosons (gravity sector in GraviGUT interpretation)
- **(10, 4)**: Mixed representation -- 40 bosons coupling gauge and gravity

This decomposition is verified in Lean (`so14_unification.lean`) as arithmetic: 45 + 6 + 40 = 91.
The algebraic closure (bracket closure of the subalgebras) requires the certified LieHoms
`SO10 ->_{L[R]} SO14` and `SO4 ->_{L[R]} SO14`, both of which now exist.

### 2. Breaking Chain Structure

No systematic phenomenological study of SO(14) breaking chains exists in the literature
(as noted in `so14-gut-literature.md`, Section 3). The inferred chains are:

**Chain A (conventional Higgs):**
```
SO(14) --[adjoint 91]--> SO(10) x SO(4) --[spinor 16]--> SU(5) x U(1) --[adjoint 24]--> SM
```

**Chain B (GraviGUT geometric):**
```
SO(3,11) --[vielbein]--> SO(3,1) x SO(10) --[standard SO(10) breaking]--> SM x Lorentz
```
(Nesti-Percacci approach: breaking is geometric, not Higgs-based)

**Chain C (orbifold):**
```
SO(14) in 5D/6D --[orbifold BCs]--> 3 generations x SO(10) in 4D --[standard breaking]--> SM
```
(Kawamura-Miura approach: three generations from orbifold compactification)

### 3. Higgs Representations

From `so14-gut-literature.md`, Section 3:
- A Higgs in the adjoint 91 could break SO(14) --> SO(10) x SO(4)
- Further breaking to SM requires additional Higgs in spinor (64) or vector (14) representations
- Krasnov's approach uses an octonionic Higgs field (bi-doublet of left-right symmetric model)
- **Gap**: No dedicated study of Higgs potentials for compact SO(14) exists

### 4. Breaking-Direction Morphisms (Open Problem)

The Bridge blueprint (`22571151`) explicitly noted:
> "Breaking-direction morphisms: We prove SO(10) -> SO(14), not SO(14) -> SO(10) x SO(4).
> The breaking direction requires quotient/projection maps or Higgs mechanism formalization.
> Future work."

The Lean proofs certify EMBEDDING morphisms (inclusion direction), not BREAKING morphisms
(quotient/projection direction). This is a structural limitation documented in the project roadmap.

### 5. Intermediate Scale Unknowns

From `so14-gut-literature.md`, Kill Conditions:
- KC-2 (gauge coupling unification): UNKNOWN -- no computation exists for SO(14)
- KC-3 (proton decay): UNKNOWN -- no proton decay calculation exists
- KC-5 (Landau poles): UNKNOWN but unlikely fatal for minimal matter content
- From `PHYSICS_MATH_FRICTION_CATALOG.md`, D5: SO(14) provides NO improvement over SO(10)
  for coupling unification; mixed (10,4) bosons contribute equally to all three SM beta functions

### 6. Maximal Subgroups of SO(14)

From standard group theory (referenced in literature survey):
- SO(10) x SO(4) -- the primary breaking investigated
- SO(12) x SO(2) -- alternative, less studied
- SO(7) x SO(7) -- symmetric, not phenomenologically motivated
- SU(7) x U(1) -- from the D_7 root system structure
- Pati-Salam SU(4) x SU(2) x SU(2) -- accessible through SO(10) intermediate

### 7. What Was NOT Found

- No subagent run of `so14-breaking-architect` was found in the JSONL transcripts
- No detailed Higgs potential analysis for SO(14)
- No explicit computation of proton decay rates for SO(14)
- No two-loop RG running for SO(14)
- The breaking chain research remains at the survey/assessment level, not at the
  computational level

## Cross-References

- `research/so14-gut-literature.md` -- Comprehensive literature survey (the primary source)
- `docs/PHYSICS_MATH_FRICTION_CATALOG.md` -- D5: coupling unification equivalence with SO(10)
- `src/lean_proofs/clifford/so14_unification.lean` -- 91 = 45 + 6 + 40 (arithmetic)
- `src/lean_proofs/clifford/so10_so14_liehom.lean` -- SO(10) -> SO(14) certified LieHom
- `src/lean_proofs/clifford/so4_so14_liehom.lean` -- SO(4) -> SO(14) certified LieHom
- `src/lean_proofs/clifford/so14_breaking_chain.lean` -- Breaking chain dimension arithmetic
- `src/lean_proofs/unification/symmetry_breaking.lean` -- VEV analysis (algebraic)
- `docs/PROJECT_ROADMAP.md` -- Remaining work items
