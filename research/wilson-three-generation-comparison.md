---
date: 2026-03-16
agent: general-purpose (research)
status: complete
context: Comparison of Wilson's vs our three-generation work
---

# Wilson vs. Arnoldy: Three-Generation Comparison

## Robert A. Wilson (Queen Mary University of London)

### Publications on Three Generations

1. **"Octions: An E_8 description of the Standard Model"** (with Manogue & Dray)
   - J. Math. Phys. 63, 081703 (2022), arXiv:2204.05310
   - ONLY peer-reviewed physics paper

2. **"Chirality in an E_8 model of elementary particles"**
   - arXiv:2210.06029 (2022), preprint only
   - Argues Distler-Garibaldi doesn't apply to massive theories

3. **"Tetrions: a discrete approach to the standard model"**
   - arXiv:2301.11727 (2023), preprint only
   - Binary tetrahedral group 2T for chirality and generations

4. **"On possible embeddings of the standard models"**
   - arXiv:2404.18938 (2024), preprint only
   - A1+G2+C3 decomposition. Acknowledges only 120/180 spinor DOF

5. **"Uniqueness of an E_8 model of elementary particles"**
   - arXiv:2407.18279 (2024), preprint only
   - Type 5 Z3 element, centralizer SU(9)/Z3, most rigorous paper

6. **"Embeddings of the Standard Model in E_8"**
   - arXiv:2507.16517 (July 2025), preprint only
   - Modified octions, SM in so(7,3), mixing angle calculations

All solo physics papers on physics.gen-ph (lowest scrutiny arXiv category).
None published in peer-reviewed journals.

### Wilson's Three-Generation Argument

- Four conjugacy classes of Z3 elements in E8 (types 1, 2, 3, 5)
- Types 1, 2: centralizers contain U(1) -> physically problematic
- Type 3: centralizer SU(3) x E6 -> assigned to color
- Type 5: centralizer SU(9)/Z3 -> UNIQUE remaining option
- 3 enters as INPUT (assumed Z3), not OUTPUT
- Physical content in Lambda^3(C^9) (dim 84 complex = 168 real)
- "If you require a discrete order-3 generation symmetry in E8, then
  type 5 is the unique option" -- consistency, not derivation

### What Wilson Has NOT Proved

- WHY nature requires exactly 3 generations (3 is assumed via Z3)
- Ghost decoupling in non-compact forms
- Dynamical mechanism for symmetry breaking
- Particle mass predictions from first principles
- Post-hoc fitting of PMNS angles from mass ratios (not predictions)

---

## Our Work (Arnoldy, Lean 4 formalization)

### What We Machine-Verified [MV]

- 248 = 80 + 84 + 84* (SU(9) decomposition of E8)
- J-eigenspace anomaly independence: Tr(Y) = 0 per sector
- Spinor parity obstruction: 3 does not divide 2, SO(14) CANNOT give 3 generations
- Seven alternative mechanisms KILLED by formalization (B1-B7 in friction catalog)
- All in Lean 4, 86 files, ~2,900 declarations, zero sorry

### Key Differences

| Aspect | Wilson | Us |
|--------|--------|-----|
| Medium | Prose arguments, arXiv preprints | Machine-verified Lean 4 proofs |
| Publication | 1 peer-reviewed (co-authored), 5 solo preprints unpublished | Papers 1-2 submitted, 3-4 ready |
| Epistemics | Argued (case analysis) | Verified (type-checked) |
| Alternatives killed | Some mentioned, not formalized | 7 killed mechanically |
| Derivation vs consistency | Consistency only | Consistency only (honest) |
| SU(9)/Z3 | Proposed the mechanism | Verified the algebra compiles |
| Yukawa structure | Claims mixing angles from E8 geometry (2025 paper) | Not yet computed |

### The Irony

Wilson withdrew arXiv endorsement for our papers because they "read as
AI-generated." But our formalization of HIS mechanism is more rigorous than
his preprints. The machine doesn't care about prose style.

### Bibliography Error (FIXED 2026-03-16)

Paper 3 cited wilson2024 with journal ref "J. Math. Phys. 63, 081703 (2022)"
which is the Octions paper (Manogue-Dray-Wilson), NOT the Uniqueness paper
(arXiv:2407.18279). Fixed: now correctly cites arXiv:2407.18279.

Paper 3 cited wilson2024b as "On the problem of interacting particles" which
is not a real Wilson paper title. Fixed: now correctly cites "Chirality in an
E_8 model" (arXiv:2210.06029).
