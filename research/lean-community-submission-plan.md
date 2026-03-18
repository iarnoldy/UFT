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

**Topic title:** `E₈ (248-dim) Lie algebra verified in Lean 4 — sparse Jacobi approach`

**Body:**

```
Hi all — I've been working on formalizing Lie algebra structures in Lean 4 with mathlib, and wanted to share what's emerged.

**What exists:**
- 88 proof files, ~2,900 declarations, zero sorry
- Five certified LieHoms composing: SU(5) →ₗ⁅ℝ⁆ SO(10) →ₗ⁅ℝ⁆ SO(14) →ₗ⁅ℝ⁆ SO(14)_matrix →ₗ⁅ℝ⁆ SO(16)
- E₈ as a 248-dimensional Lie algebra verified via sparse Jacobi identity (7,752 nonzero brackets, native_decide over all 248³ triples)
- SO(16) ⊂ E₈ subalgebra closure verified
- Lean v4.29.0-rc4, mathlib dependency

**The sparse Jacobi approach:**
Dense 248×248 matrix multiplication for Jacobi would be O(n⁵). Instead, we precompute only nonzero structure constants (7,752 out of 248² = 61,504) and check the Jacobi identity via direct lookup. This is 88× faster and O(n⁴). Each of the 16 verification chunks takes ~90 seconds.

**The type bridge pattern:**
We built Lie algebras by hand (flat structures with explicit brackets) and then proved LieHom into mathlib's matrix Lie algebra infrastructure. This "type bridge" pattern might be useful for anyone constructing new Lie algebras that need to interface with mathlib's typeclass hierarchy.

**One thing I think fills a gap:**
The Lie-Schur lemma (nonzero LieModuleHom between irreducible Lie modules is bijective) and its application to Killing form uniqueness. Mathlib has classical Schur for group representations but I couldn't find the Lie module version. Happy to extract this as a mathlib PR if useful.

Repo: https://github.com/iarnoldy/UFT
Key files:
- E₈ sparse defs: `src/lean_proofs/clifford/e8_sparse_defs.lean`
- Schur/Killing: `src/lean_proofs/spectral/schur_killing_uniqueness.lean`
- Type bridge: `src/lean_proofs/clifford/so14_to_matrix.lean`

Happy to answer questions or extract pieces for mathlib contribution.
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
