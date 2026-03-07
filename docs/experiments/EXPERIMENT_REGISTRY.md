# Experiment Registry

All experiments must be pre-registered here before execution.
Each entry requires a hypothesis, falsification criteria, and track assignment.

---

## Experiment 0: Polyphase Formula Verification [BLOCKING]

**Status**: PRE-REGISTERED
**Track**: B
**Priority**: BLOCKING -- other polyphase work depends on this

**Hypothesis**: The universal polyphase formula k^n_N = exp(j*2*pi*n/N) is provable
in Lean 4 as a consequence of the nth roots of unity.

**Method**: Write Lean 4 proof in `src/lean_proofs/polyphase/` that:
1. Defines nth_root_unity(n, N) = exp(2*pi*i*n/N)
2. Proves (nth_root_unity(1, N))^n = nth_root_unity(n, N)
3. Proves nth_root_unity(N, N) = 1
4. Proves the 3-phase specialization: a^3 = 1 where a = exp(2*pi*i/3)

**Falsification**: If Lean rejects the proof, the polyphase claim needs
reinterpretation. Specifically, if the formula requires non-standard definitions
or axioms beyond mathlib, document what's needed.

**Expected outcome**: VERIFIED (this is standard roots-of-unity math, expected to
be trivial like the basic operator proofs).

**Dependencies**: None
**Downstream impact**: N-Phase system's Fortescue decomposition depends on this

---

## Experiment 1: h Operator Alternative Interpretations

**Status**: PRE-REGISTERED
**Track**: A + B

**Hypothesis**: There exists a non-trivial algebraic structure (beyond complex
numbers) where h satisfies h^2 = 1 and h^1 = -1 simultaneously, AND h != -1.

**Method**:
1. Survey algebraic structures: split-complex numbers, dual numbers, Clifford algebras
2. For each candidate, check if h properties hold with h != -1
3. If found, implement in Lean 4 and verify

**Falsification**: If no such structure exists, h = -1 is the only interpretation
and Dollard's "versor algebra" is isomorphic to Z_4 (the 4th roots of unity).
This would confirm Finding 1 of the audit.

**Expected outcome**: DISPROVED (likely no non-trivial structure exists, but the
search itself has methodological value for Track A).

**Dependencies**: None
**Downstream impact**: Determines whether versor algebra has novel algebraic content

---

## Experiment 2: Versor Form Repair

**Status**: PRE-REGISTERED
**Track**: B

**Hypothesis**: There exists a consistent modification of Dollard's versor form
ZY = h(XB+RG) + j(XG-RB) that preserves equivalence with the standard telegraph
equation ZY = (RG+XB) + j(XG-RB).

**Method**:
1. Enumerate possible repairs: replace h with 1, redefine h, change sign convention
2. For each candidate repair, attempt Lean 4 proof of equivalence
3. Check whether any repair preserves Dollard's other claimed properties

**Falsification**: If no repair preserves both equivalence and the h operator
properties (h^2=1, h^1=-1), the versor form is simply wrong and cannot be saved.

**Expected outcome**: The only "repair" is h=1, which contradicts h^1=-1.
The versor form is wrong.

**Dependencies**: None (uses existing disproof as starting point)
**Downstream impact**: N-Phase system must not depend on versor form equivalence

---

## Experiment 3: Dimensional Analysis Verification

**Status**: PRE-REGISTERED
**Track**: B + C

**Hypothesis**: Q = Psi * Phi with W = dQ/dt is dimensionally consistent,
where Psi has units of Coulomb and Phi has units of Weber.

**Method**:
1. Define dimensional type system in Lean 4
2. Verify: Weber * Coulomb = Joule * second
3. Verify: d/dt(Joule * second) = Joule = Watt * second
4. Check dimensional consistency of the full energy framework

**Falsification**: Dimensional inconsistency would invalidate the energy framework
claimed in Lone Pine Writings.

**Expected outcome**: VERIFIED (dimensional analysis is checkable and likely correct).

**Dependencies**: None
**Downstream impact**: Affects Track C physics claims about energy
