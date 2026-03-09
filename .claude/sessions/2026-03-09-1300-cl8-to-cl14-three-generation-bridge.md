---
version: 2
id: 2026-03-09-1300
name: cl8-to-cl14-three-generation-bridge
started: 2026-03-09T13:00:00-04:00
parent_session: 2026-03-09-0520-paper2-cross-domain-identities.md
tags: [cl8, cl14, three-generations, s3-symmetry, gresnigt, sedenions, falsifiable]
status: completed
---

# Development Session - 2026-03-09 13:00 - Cl(8) → Cl(14) Three-Generation Bridge

**Started**: 2026-03-09T13:00:00-04:00
**Project**: UFT (dollard-formal-verification)
**Parent Session**: 2026-03-09-0520-paper2-cross-domain-identities.md

## Goals

- [x] Read Gresnigt 2024/2026 papers to extract the precise S₃ action on Cl(8) [completed @ 13:30]
- [x] Construct explicit Cl(8) → Cl(14) embedding in Python (128×128 gamma matrices) [completed @ 14:15]
- [x] Build Gresnigt's primitive idempotent in Cl(8) and verify the 3-way splitting [completed @ 14:00]
- [x] Compute S₃ generators as explicit matrices on the 64-dim semi-spinor of SO(14) [completed @ 14:30]
- [x] Test: does S₃ decompose the 64 (or 3×64) into three gauge-equivalent copies of 16? [completed @ 14:45]
- [x] Determine outcome: SUCCESS / PARTIAL / FAILURE (KC-5 resolution) [completed @ 15:00]
- [ ] ~~If success: formalize key results in Lean 4~~ (N/A — KC-5 fired)
- [ ] Write up results (positive or negative) for potential publication

## Kill Conditions

- **KC-5**: If S₃ does not extend to a gauge-preserving action on the Cl(14) semi-spinor → mechanism fails for SO(14), fall back to orbifold
- **KC-9**: If the three Cl(6) subalgebras within Cl(8) don't map to distinct SO(10) representations under the Cl(8) ⊂ Cl(14) embedding → structural incompatibility

## Key References

- Gresnigt 2024: arXiv:2407.01580 (S₃ from Cl(8), EPJC)
- Gresnigt 2026: arXiv:2601.07857 (electroweak + S₃)
- Gillard & Gresnigt 2019: EPJC 79, 446 (sedenion three-generation origin)
- Our survey: docs/SO14_THREE_GENERATIONS.md (Section 6)

## Progress Log

### Update - 2026-03-09 13:30 — Paper extraction complete

Downloaded and read Gresnigt 2024 (arXiv:2407.01580) in full. Extracted:
- Eq. (9): Witt basis construction a_k = ½(-e_k + ie_{k+4})
- Eq. (22): ψ map on Cl(8) generators (the S₃ order-3 element)
- Eq. (33): ε action (the S₃ order-2 element, V = e₁e₂...e₇)
- Appendix A: Full 16×16 sedenion multiplication table
- Eqs. (16-18): SU(4) generators and U(1) charge

### Update - 2026-03-09 14:45 — COMPUTATION COMPLETE, KC-5 FIRES

Script: `src/experiments/cl8_cl14_bridge.py` (7 phases, ~450 lines)

**Phase 1-3**: All Cl(8) results verified. Gresnigt's mechanism works perfectly within Cl(8):
- Primitive idempotent v₁ = a₁a₂a₃a₄·a₄†a₃†a₂†a₁† is rank-1, v₁²=v₁
- S₃ generators ψ (order 3) and ε (order 2) satisfy all Cl(8) relations
- Inner automorphism U found via SVD null space: U³=I, Ue_iU⁻¹=ψ(e_i)

**Phase 4 — THE CRITICAL TEST**: ψ MIXES Cl(8) chirality
- [U, Γ₈] norm = 1.732051 (non-zero → doesn't commute)
- {U, Γ₈} norm = 1.000000 (non-zero → doesn't anticommute)
- U block norms: U++ = 1.414, U+- = 2.449 (large off-diagonal mixing)
- **This is structurally inherent**: sedenion automorphisms mix the Z₂ grading

**Phase 5-6**: Cl(14) built via tensor product Cl(8) ⊗ Cl(6), all 14 generators verified (128×128).
Extension U₁₂₈ = U ⊗ I₈ has:
- Eigenvalues: {1, ω²} each ×64 (only 2-fold, not 3-fold split)
- Leakage |P₋UP₊| = 6.928 (massive mixing between 64+ and 64-)
- SO(10) Casimir on 64+: single eigenvalue 11.25 ×64 (no sub-splitting)

**Phase 7**: Vacuum vectors ψ_k = U^k|0⟩ have chirality expectation values +1, -0.5, -0.5 and overlaps 0.5 (not orthogonal).

### VERDICT: KC-5 FIRES — PARTIAL FAILURE

The Gresnigt S₃ three-generation mechanism is **verified in Cl(8)** but **does NOT extend to SO(14) semi-spinors**. The fundamental obstruction: sedenion automorphisms mix the Z₂ grading of Cl(8), which is entangled with the SO(14) chirality operator via the tensor product construction Cl(14) = Cl(8) ⊗ Cl(6).

**Consequences for Paper 3:**
- Three-generation section must use orbifold mechanism (Kawamura-Miura) as primary
- Gresnigt mechanism documented as investigated and ruled out for SO(14)
- This is an honest negative result — publishable in its own right
- The three-generation problem for SO(14) remains OPEN

---

## Session Summary

**Completed**: 2026-03-09T15:15:00-04:00
**Duration**: ~2 hours 15 minutes

### Accomplishments

1. **Extracted Gresnigt's full S₃ construction from published paper**
   - Downloaded arXiv:2407.01580 (20 pages), read and extracted all key equations
   - Witt basis, ψ map (Eq. 22), ε action (Eq. 33), sedenion multiplication table (Appendix A)
   - SU(4) generators (Eq. 16), U(1) charge (Eq. 18), S₃-invariant charge (Eq. 30)

2. **Built complete Cl(8) from sedenion left multiplication**
   - 16×16 complex matrices for all 8 generators
   - Verified all anticommutation relations {e_i, e_j} = -2δ_ij
   - Constructed Witt basis, fermionic oscillators, primitive idempotent

3. **Verified Gresnigt's S₃ mechanism within Cl(8)**
   - ψ (order-3 automorphism) preserves all Clifford relations
   - Found inner automorphism matrix U via SVD null space: U³=I, Ue_iU⁻¹=ψ(e_i)
   - ε (order-2) = V = e₁e₂...e₇, V²=+I
   - S₃ relation V·U = U²·V confirmed

4. **Discovered the chirality obstruction (the key result)**
   - U neither commutes nor anticommutes with Γ₈ = e₁e₂...e₈
   - Off-diagonal blocks U+- = 2.449 (massive chirality mixing)
   - This is structurally inherent in sedenion automorphisms

5. **Built Cl(14) = Cl(8) ⊗ Cl(6) and tested the bridge**
   - 128×128 gamma matrices, all 14 generators verified
   - Bug fix: Cl(6) generators needed factor of i for correct sign convention
   - Extension U₁₂₈ = U ⊗ I₈ has leakage |P₋UP₊| = 6.928

6. **KC-5 resolved: FIRES (negative result)**
   - S₃ does NOT extend to gauge-preserving action on SO(14) semi-spinors
   - Three-generation problem for SO(14) remains OPEN
   - Fallback to orbifold mechanism for Paper 3

### Added Files

- `src/experiments/cl8_cl14_bridge.py` — 7-phase computation script (~450 lines)
- `.claude/sessions/2026-03-09-1300-cl8-to-cl14-three-generation-bridge.md` — this session

### Tasks Completed

- ✓ Paper extraction (Gresnigt 2024)
- ✓ Cl(8) construction and verification
- ✓ S₃ generator computation (ψ and ε)
- ✓ Chirality preservation test
- ✓ Cl(14) tensor product construction
- ✓ Bridge extension test
- ✓ Vacuum vector analysis
- ✓ KC-5 resolution (FIRES)

**Remaining Tasks**:
- [ ] Write up negative result for Paper 3 three-generation section
- [ ] Update `docs/SO14_THREE_GENERATIONS.md` with computation results

### Problems & Solutions

1. **Problem**: Cl(6) generators had wrong sign convention (g² = +I instead of -I)
   **Solution**: Multiplied by factor of `1j` so `(ig)² = -g² = -I`
   **Why**: Standard Pauli tensor construction gives positive-definite, but sedenion Cl(8) is negative-definite

2. **Problem**: Chirality test gave misleading scalar ratio (-0.5 with error 0.866)
   **Solution**: Replaced ratio test with direct commutator/anticommutator checks
   **Why**: `psi_Gamma8 @ Gamma8_inv` is NOT scalar when U doesn't commute with Γ₈

3. **Problem**: WebFetch on arXiv abstract page returned only metadata
   **Solution**: Used PDF URL directly, then Read tool with `pages` parameter
   **Why**: Abstract page is HTML with minimal content; PDF is the actual paper

### Lessons Learned

- **Sedenion automorphisms inherently mix Clifford grading.** The S₃ ⊂ Aut(S₁₆) maps between even and odd elements of Cl(8). This is not a fixable implementation detail — it's structural. Any attempt to use sedenion-derived S₃ for SO(14) semi-spinors faces the same obstruction.
- **Kill conditions work.** KC-5 was designed to catch exactly this failure mode. Pre-registering falsification criteria BEFORE running the computation prevented us from rationalizing around the negative result.
- **Negative results are publishable.** The chirality mixing obstruction is a genuine mathematical finding about the incompatibility of Gresnigt's mechanism with SO(14). Worth a remark in Paper 3 and potentially a short note.
- **Eigenvalue analysis is more informative than norm checks.** The 2-fold (not 3-fold) eigenvalue split of U₁₂₈ immediately shows the bridge can't produce three generations.

### Future Work

- [ ] Update Paper 3 three-generation section to use orbifold mechanism (Kawamura-Miura)
- [ ] Document Gresnigt obstruction as a remark in Paper 3 (1-2 paragraphs)
- [ ] Consider whether a MODIFIED ψ (not from sedenions) could preserve chirality
- [ ] Investigate if the full 128 (not just 64+) admits a useful 3-fold split
- [ ] Paper 2 submission to AACA (separate session)

### Tips for Future Developers

- `cl8_cl14_bridge.py` is self-contained — runs with only numpy, no external deps
- The sedenion multiplication table is hardcoded from Gresnigt's Appendix A
- SVD null space method for finding inner automorphism matrix is numerically robust
- If testing alternative S₃ actions, check `[U, Γ₈]` FIRST — it's the cheapest test

---

**Session File**: `.claude/sessions/2026-03-09-1300-cl8-to-cl14-three-generation-bridge.md`
