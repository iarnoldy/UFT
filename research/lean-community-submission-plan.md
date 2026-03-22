# Lean Community Submission Plan

> Step-by-step guide for Ian. Written explicitly — follow in order.

## Step 1: Create a Lean Zulip Account (5 minutes)

1. Open your browser
2. Go to: `https://leanprover.zulipchat.com`
3. Click "Sign up" (top right)
4. Use your email to create an account
5. Confirm your email
6. You're in

## Step 2: Post to Lean Zulip (10 minutes)

This is a low-barrier introduction. You're not asking for anything — just sharing what you built.

### Where to post

1. In Zulip, click "All channels" on the left sidebar
2. Search for: **"Is there code for X?"**
3. Click that channel
4. Click "New topic" (bottom of the page)

### What to write

Copy-paste this EXACTLY (you can edit later if you want):

---

**Topic title:** `E₈ (248-dim) Lie algebra verified in Lean 4 — sparse Jacobi, scalability lessons`

**Body:**

```
Hi all — I've been formalizing Lie algebra structures in Lean 4 with mathlib and wanted to share what came out of it, including some scalability lessons that might be useful to others working with large algebraic structures.

**Disclosure:** This project was built in collaboration with Claude (Anthropic's AI). I'm an aviation electronics technician by background, not a mathematician — Claude served as an intellectual partner throughout, helping with proof strategy, mathlib API navigation, and code generation. Every proof compiles and is machine-verified, but I want to be upfront about how it was made. The mathematical direction and project decisions are mine; the Lean implementation was collaborative.

**Context on the repo:** The repo name ("UFT") reflects the physics motivation — I started from Eric Dollard's electrical engineering work and built upward through standard Lie algebra embeddings to see how far formal verification could take it. The physics interpretation is speculative and clearly marked as such in the repo. What I'm sharing here is the pure mathematics and the Lean engineering — the proofs stand regardless of the physics framing.

**What exists:**
- 91 compiled proof files (3,076 declarations, zero sorry)
- Four certified LieHoms: SU(5) →ₗ⁅ℝ⁆ SO(10) →ₗ⁅ℝ⁆ SO(14), plus SO(4) →ₗ⁅ℝ⁆ SO(14) and a type bridge SO(14) →ₗ⁅ℝ⁆ SO(14)_matrix. SO(14) → SO(16) exists as source but does not compile (ADR-006)
- E₈ as a 248-dimensional Lie algebra verified via sparse Jacobi identity (7,752 nonzero brackets, native_decide over all 248³ triples)
- SO(16) ⊂ E₈ subalgebra closure verified
- Lie-Schur lemma and Killing form uniqueness (I couldn't find an existing formalization in Coq, Isabelle, or Mizar — but I haven't done an exhaustive search)
- Lean v4.29.0-rc4, mathlib dependency

**The sparse Jacobi approach:**
Dense 248×248 matrix multiplication for Jacobi would be O(n⁵). Instead, we precompute only nonzero structure constants (7,752 out of 248² = 61,504) and check the Jacobi identity via direct lookup — O(n⁴) instead of O(n⁵). At dimension 50, the sparse approach was 88× faster than dense in our benchmarks. Each of the 16 E₈ verification chunks takes ~40 minutes to compile (parallelizable via `lake build`).

**Scalability lessons (hitting Lean's limits with E₈):**
Getting E₈ to compile taught us a lot about what Lean can and can't handle at scale:
- Our first attempt used dense 248×248 matrices. The generated .lean files were too large and compilation ran out of memory.
- We moved to a sparse representation: only the 7,752 nonzero structure constants, stored as a lookup function. This cut file size dramatically.
- Even sparse, the Jacobi verification over 248³ ≈ 15.3M triples had to be chunked into 16 separate files to stay within compilation limits. Each chunk handles a range of the first index.
- `native_decide` was essential — `decide` alone couldn't handle the scale.
- The .olean files are enormous: SO(16) is 2.1 GB, SO(14) is 1.1 GB, SO(10) is 198 MB, E₈ sparse defs is 32 MB. Incremental compilation is essential — a full rebuild is painful.
- SageMath served as an oracle for structure constants (Chevalley basis), which were then hard-coded into Lean for verification.

If anyone else is working with large finite algebraic structures in Lean, happy to share more details on what worked and what didn't.

**The type bridge pattern:**
We built Lie algebras by hand (flat structures with explicit brackets) and then proved LieHom into mathlib's matrix Lie algebra infrastructure. This "type bridge" pattern might be useful for anyone constructing new Lie algebras that need to interface with mathlib's typeclass hierarchy.

**Adding mathlib instances to hand-built algebras:**
We developed a repeatable recipe for upgrading flat Lie algebra definitions to full mathlib `LieRing` + `LieAlgebra ℝ` instances. Tested on Bivector (6 gens), SL₃ (8), SL₅ (24), SU₅ (24), SO₁₀ (45), SO₁₄ (91), SO₁₆ (120). The pattern: define the bracket as a bilinear map, prove antisymmetry and Jacobi, then provide the instances. If there's interest I can write this up more formally.

**Things I think fill gaps in mathlib:**
1. **Lie-Schur lemma** — nonzero LieModuleHom between irreducible Lie modules is bijective. Mathlib has classical Schur for group representations but I couldn't find the Lie module version (I may have missed it — please correct me if it exists). Application: Killing form uniqueness (invariant bilinear form on simple Lie algebra is proportional to Killing form).
2. **Antisymmetric trace identity** — Tr(A{B,C}) = 0 for antisymmetric matrices A, B, C in any ring. Small standalone lemma, useful for anomaly computations in gauge theory.

Repo: https://github.com/iarnoldy/UFT
Key files:
- E₈ sparse defs: `src/lean_proofs/clifford/e8_sparse_defs.lean`
- E₈ Jacobi chunks: `src/lean_proofs/clifford/e8_sparse_jac_00.lean` through `_15.lean`
- Schur/Killing: `src/lean_proofs/spectral/schur_killing_uniqueness.lean`
- Type bridge: `src/lean_proofs/clifford/so14_to_matrix.lean`
- Anomaly trace: `src/lean_proofs/clifford/anomaly_trace.lean`
- mathlib instance pattern: `src/lean_proofs/clifford/su5c_compact.lean`

Happy to answer questions, share the SageMath oracle scripts, or extract pieces for mathlib PRs.
```

---

### After posting

- Wait 1-3 days for responses
- People may say "cool" or "we already have X" or "yes please make a PR for Y"
- The Schur/Killing proof is the most likely PR candidate
- If someone engages positively, that's your potential arXiv endorser

## Step 3: Prepare mathlib PR (do AFTER Zulip response, ~2-3 hours)

Only do this if the Zulip community signals interest in the Schur/Killing proof.

### 3a. Fork mathlib4

1. Go to: `https://github.com/leanprover-community/mathlib4`
2. Click "Fork" (top right)
3. This creates your copy at `https://github.com/iarnoldy/mathlib4`

### 3b. Clone and branch

Open your terminal:
```bash
cd ~/Documents/CODING
git clone https://github.com/iarnoldy/mathlib4.git
cd mathlib4
git checkout -b feat-lie-schur
```

### 3c. Extract the proof

I (Claude) will help you:
- Copy `schur_killing_uniqueness.lean` content
- Clean project-specific imports
- Restructure to follow mathlib conventions
- Add mathlib-style docstrings
- Place at `Mathlib/Algebra/Lie/Schur.lean`

### 3d. Test

```bash
lake build Mathlib.Algebra.Lie.Schur
```

### 3e. Open PR

```bash
git add Mathlib/Algebra/Lie/Schur.lean
git commit -m "feat(Algebra.Lie): Lie-Schur lemma and Killing form uniqueness"
git push origin feat-lie-schur
```

Then go to GitHub and create a PR with:
- Title: `feat(Algebra.Lie): Lie-Schur lemma and Killing form uniqueness`
- Body: Link to your Zulip post, explain what it proves and why it's missing from mathlib

## Step 4: arXiv Endorsement (organic path)

If your Zulip post gets engagement:

1. Reply to someone who seems interested
2. Say: "I have a couple papers on this formalization work that I'd like to put on arXiv. Would you happen to have endorsement in math.RT or math-ph? I'd be grateful for an endorsement."
3. Most active Lean community members have arXiv accounts with endorsement capability
4. This solves the Wilson problem without needing Wilson

### What you need from an endorser

- They go to `https://arxiv.org/auth/endorse`
- They enter your arXiv username
- They click "Endorse"
- That's it — takes them 30 seconds

## Timeline

| When | What | Effort |
|------|------|--------|
| Today/tomorrow | Zulip account + post | 15 min |
| Wait 1-3 days | Read responses | 5 min |
| If positive | Prepare Schur PR (with Claude) | 2-3 hours |
| When relationship built | Ask for endorsement | 1 message |

## What NOT to Do

- Don't post to multiple channels at once (looks spammy)
- Don't mention physics/UFT/Dollard in the Zulip post (the math community cares about the math, not the physics motivation)
- Don't oversell — "I formalized X" is better than "GROUNDBREAKING RESULT"
- Don't ask for endorsement in the first message (build relationship first)
