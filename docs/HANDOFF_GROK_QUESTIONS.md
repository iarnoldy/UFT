# Handoff: Grok's Stress-Test Questions for SO(14)

**Date:** 2026-03-10
**Source:** Grok posed these as criteria for any three-generation / unification claim
**Ian's note:** "A real solution would likely be Nobel-level (or more) and revolutionary for unification."
**Status:** OPEN — to be addressed when Ian returns

---

## The Questions & Our Honest Current Answers

### Q1. Fermion masses, CKM/PMNS, mixing angles without free parameters?

**Answer: No.**
- Yukawa coupling structure is axiomatized, not derived (`yukawa_couplings.lean`)
- Gauge invariance of Yukawa interaction is [MV], but coupling constants are free parameters
- Zero predictions for any mass ratio, mixing angle, or CKM/PMNS element
- Same as every other GUT — this is an unsolved problem across the field
- **Grade: F** (same F as SO(10), SU(5), E₆)

**TODO:** Decide if this is even in scope for our framework, or if it's inherently beyond algebraic scaffold work.

### Q2. Why exactly three generations?

**Answer: Partially — our strongest novel result, but with gaps.**
- PROVED: SO(14) cannot produce 3 generations intrinsically [MV] — `three_gen_excluded`, `spinor_parity_obstruction.lean`
- SHOWED: E₈ → SU(9)/Z₃ → SU(5) × SU(3)_family gives exactly 3 via Wilson's mechanism
- The "3" comes from Λ³(C⁹) = 84, under SU(5)×SU(3) gives the **3** of SU(3)_family
- Five Lean files: `spinor_parity_obstruction` → `e8_embedding` → `e8_su9_decomposition` → `e8_generation_mechanism` → `three_generation_theorem`
- **Gap:** E₈ embedding is axiomatized at dimensional level [MV for dims, CP for physics]. Branching rules use standard rep theory [CO], not machine-verified decompositions.
- **Grade: B-** for mechanism, **C** for rigor

**TODO:** Can we strengthen the E₈ branching rules to [MV]? What would that require in Lean?

### Q3. Consistent with all data (Z width, LHC, proton stability)?

**Answer: Compatible, but "compatible" ≠ "predicted."**
- Z width (N_ν = 3): Compatible — E₈ mechanism gives exactly 3 light generations [CO]
- LHC limits on extra generations: Compatible — exotics (36 dims) predicted heavy at GUT scale [CP]
- Proton stability: τ_p ≈ 10^38.9 years >> Super-K bound 10^34.4 years [CO]
- No fourth-family particles: Consistent with 3-generation structure
- **Grade: B** — nothing falsified, nothing uniquely predicted

**TODO:** Sharpen proton decay estimate. Is two-loop calculation feasible [CO]?

### Q4. New testable predictions in 5-20 years?

**Answer: Weak.**
- Proton decay: τ_p ~ 10^38.9 years — Hyper-K won't reach this (probes ~10^35)
- Coupling unification: 0.88% miss, within threshold corrections, not a sharp prediction
- No accessible-energy particles distinguishing SO(14) from SO(10)
- No unique cosmological signal identified
- Paper 3 honestly says: "INTERESTING, not compelling. No accessible-energy distinction from SO(10)."
- **Grade: D**

**TODO:** This is the weakest point. Brainstorm: are there ANY signatures unique to SO(14) vs SO(10)? Gravitational wave spectrum from phase transitions? Exotic scalar signatures? Dark matter candidates from the 40 mixed generators?

### Q5. Mathematically rigorous, renormalizable, unitary, gravity, UV-complete?

**Answer: Mixed.**
- **Rigorous:** YES — 43 Lean files, ~1400 theorems, 0 sorry. Unprecedented for a GUT. [MV] **Grade: A**
- **Renormalizable:** Higgs sector (177 scalar components) renormalizable by power counting [CO]. Perturbative unitarity at all scales: not proved.
- **Unitary:** Distler ghost objection for SO(3,11) is UNRESOLVED [OP]. Compact SO(14) fine; physical Lorentzian SO(3,11) might have ghosts.
- **Gravity:** 91 = 45+6+40 includes SO(4) ⊃ SO(1,3), but algebraic containment only. NO dynamical gravity theory. Einstein's equations do not emerge.
- **UV-complete:** No. E₈ embedding exists algebraically but no UV completion mechanism.
- **Overall Grade: A for algebra, C for physics**

**TODO:** The ghost problem is the most pressing physics blocker. Review Krasnov's chiral resolution. Contact Krasnov/Percacci after Paper 1 acceptance.

### Q6. Dark matter, neutrino masses, strong CP, hierarchy problem?

**Answer: Mostly unaddressed.**
- **Dark matter:** No candidate identified. 40 mixed generators + exotic scalars could contain one [CP speculation].
- **Neutrino masses:** SO(10) includes right-handed neutrinos (in the 16), seesaw available [SP]. No mass computed.
- **Strong CP:** Not addressed.
- **Hierarchy problem:** Not addressed. 177 scalar components arguably make it worse.
- **Grade: D** — standard SO(10) inheritance, nothing novel

**TODO:** Can any of the exotic scalars serve as dark matter candidates? This might be low-hanging fruit for a novel prediction.

### Q7. Peer-reviewed? Step-by-step derivations available?

**Answer: Submitted, not yet reviewed.**
- Paper 1 (methodology): Submitted to CICM 2026 (Submission #9090), awaiting review
- Paper 2 (mathematical identities): Submitted to AACA, awaiting editorial
- Paper 3 (SO(14) physics): Draft, not submitted
- Independent stress-testing: None yet
- Code: Public on GitHub (https://github.com/iarnoldy/UFT), Lean proofs independently verifiable
- Step-by-step: YES — every theorem mechanically checkable with `lake build`
- **Grade: C** — submitted but not accepted, no expert physics review yet

**TODO:** After Paper 1 acceptance, solicit physics review from Krasnov, Percacci, or Lisi.

### Bonus: Why is first generation light (atoms possible) while third is heavy?

**Answer: No.** Zero mechanism for mass hierarchies. Requires Yukawa structure we don't derive.

**TODO:** Is this even addressable without a complete flavor theory?

---

## Strategic Assessment

**What we genuinely have:**
1. Machine-verified algebraic scaffold for a GUT — first of its kind
2. Clean impossibility proof (SO(14) can't → 3 gen) + concrete mechanism (E₈ does)
3. Honest tagging system ([MV]/[CO]/[CP]/[OP]) unique among GUT papers

**What we don't have:**
1. Any prediction distinguishing us from SO(10) at accessible energies
2. Any fermion mass or mixing angle
3. Ghost problem resolution
4. Peer review of physics content
5. Dynamical gravity
6. UV completion

**The uncomfortable truth:** This is an algebraic scaffold, not a physical theory in the Weinberg-Salam sense. Machine verification makes the skeleton unimpeachable, but an unimpeachable skeleton is not a body.

**Ian's instinct is correct:** A real solution to the generation problem would be Nobel-level. We have a *mechanism* that gives the right number — necessary but not sufficient.

## Priority Actions When Ian Returns

1. **Ghost problem** — most pressing physics blocker (Q5)
2. **Unique predictions** — any SO(14)-specific observable? (Q4)
3. **Dark matter candidate** — low-hanging fruit from exotic sector? (Q6)
4. **E₈ branching rigor** — can we push [CO] → [MV]? (Q2)
5. **Paper 3 submission** — after addressing Q4 weakness
6. **Expert review** — Krasnov/Percacci/Lisi after Paper 1 acceptance (Q7)
