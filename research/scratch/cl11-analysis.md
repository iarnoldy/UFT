# Cl(1,1) Rehabilitation Analysis

## The Question
If we drop Dollard's constraint h^1 = -1 and instead keep only h^2 = 1 with h != +/-1,
what algebra results? Does Cl(1,1) offer a non-trivial versor algebra? Would the versor
form equivalence work?

## Construction of Cl(1,1)

Cl(1,1) is the Clifford algebra of R^2 with signature (1,1): one basis vector squares to +1,
the other to -1.

Generators: e1, e2
Relations:
  e1^2 = +1
  e2^2 = -1
  e1*e2 = -e2*e1  (anticommutativity of distinct basis vectors)

Basis elements: {1, e1, e2, e12} where e12 = e1*e2

Dimension: 2^2 = 4 (as a vector space over R)

Key properties of e12:
  e12^2 = (e1*e2)(e1*e2) = e1*(e2*e1)*e2 = e1*(-e1*e2)*e2 = -(e1^2)*(e2^2) = -(+1)(-1) = +1
  e12^2 = +1

So e12 squares to +1, just like e1. And e12 != +/-1 (it is linearly independent from 1).

## Mapping to Dollard's Versors

Proposed identification:
  1  <-->  1    (scalar unit)
  j  <-->  e2   (e2^2 = -1, so e2 plays the role of the imaginary unit)
  h  <-->  e1   (e1^2 = +1, e1 != +/-1 -- this is the non-trivial "h")
  k  <-->  e12  (e12 = e1*e2, and e12^2 = +1)

Check Dollard's axioms:
  j^2 = e2^2 = -1  YES
  h^2 = e1^2 = +1  YES
  h*j = e1*e2 = e12 = k  YES
  j*k = e2*(e1*e2) = e2*e1*e2 = (-e1*e2)*e2 = -e1*(e2^2) = -e1*(-1) = e1  WAIT
    j*k = e1 = h, not 1. FAILS Dollard's axiom jk = 1.

Alternative: j*k in Dollard's system = 1. Let's check what jk gives in Cl(1,1):
  j*k = e2 * e12 = e2 * (e1*e2) = (e2*e1)*e2 = -(e1*e2)*e2 = -e1*(e2^2) = -e1*(-1) = e1

So jk = e1 = h != 1. Dollard requires jk = 1. This FAILS.

## Why It Fails: Commutativity

Dollard's versor algebra is COMMUTATIVE (Z_4 is abelian).
Cl(1,1) is NON-COMMUTATIVE: e1*e2 = -e2*e1.

This is the fundamental incompatibility. In Z_4:
  jk = i * (-i) = 1 (commutative)

In Cl(1,1):
  e2 * e12 = e1 (not 1, and not even e2 * e1*e2 in the commutative sense)

## Alternative Mapping: Using e12 as j

What if we try:
  j <--> e12  (e12^2 = +1... no, that gives j^2 = +1, not -1)

Actually, let me recompute. In Cl(1,1):
  e12^2 = e1*e2*e1*e2 = -e1*e1*e2*e2 = -(+1)(-1) = +1

So e12^2 = +1. There is NO element in Cl(1,1) that squares to -1 among the basis!

Wait -- general elements can square to -1. Consider a = a1*e1 + a2*e2:
  a^2 = a1^2*e1^2 + a1*a2*e1*e2 + a2*a1*e2*e1 + a2^2*e2^2
       = a1^2 - a2^2 + a1*a2*(e12 - e12) = a1^2 - a2^2

So a^2 = a1^2 - a2^2. For this to equal -1: a1^2 - a2^2 = -1, e.g., a1 = 0, a2 = 1 gives
a = e2 with a^2 = -1. Good -- e2 still works as j.

## The Core Problem: No 4-Element Abelian Subgroup Isomorphic to Z_4

In Cl(1,1), the multiplicative structure of basis elements:
  1*1 = 1    e1*e1 = 1    e2*e2 = -1   e12*e12 = 1
  e1*e2 = e12   e2*e1 = -e12   e1*e12 = e2   e12*e1 = -e2
  e2*e12 = e1   e12*e2 = -e1

The basis elements do NOT form an abelian group. The set {1, e2, -1, -e2}
forms Z_4 (abelian), but this is just the complex numbers embedded in Cl(1,1),
and h = -1 again.

## Conclusion on Cl(1,1) Rehabilitation

Cl(1,1) does NOT rehabilitate Dollard's versor algebra for the following reason:

1. If we want h*j = k (product rule), j^2 = -1, h^2 = 1, AND jk = 1 (all Dollard axioms
   except h = -1), the requirement jk = 1 forces commutativity on {1,j,h,k}, and the
   only abelian group of order 4 with an element of order 4 is Z_4, which forces h = j^2 = -1.

2. Cl(1,1) is non-commutative, so it cannot contain Z_4 as a subalgebra in the way Dollard
   needs. It can contain Z_4 = {1, e2, -1, -e2} but this makes h = -1 again.

3. If we relax the jk = 1 requirement (allow non-commutativity), we get the full Cl(1,1)
   algebra, which IS genuinely interesting for electromagnetism (published papers confirm this)
   but is NO LONGER Dollard's versor algebra -- it is a fundamentally different structure.

## What WOULD Work (If Dollard Changed His Axioms)

If Dollard's axioms were changed to:
  j^2 = -1 (keep)
  h^2 = +1 (keep)
  hj = -jh (NEW: anticommutativity instead of hj = k, jk = 1)
  k = hj (keep as definition)

Then the resulting algebra IS Cl(1,1), which:
- Is isomorphic to Mat(2,R) (2x2 real matrices)
- Has genuine applications in electromagnetism (published: Springer, MDPI)
- Is non-commutative
- Contains zero divisors
- Is 4-dimensional over R (like quaternions, but different signature)

This would be a genuinely non-trivial mathematical framework. But it is NOT what Dollard describes.

## Versor Form Equivalence in Cl(1,1)

In Cl(1,1), the telegraph equation product would be:
ZY = (R + e2*X)(G + e2*B) where e2 plays the role of j

Expanding (with e2^2 = -1):
= RG + Re2*B + e2*XG + e2*e2*XB
= RG + e2*RB + e2*XG + (-1)*XB
= (RG - XB) + e2*(RB + XG)

This is just standard complex multiplication (same as before, because e2 acts like i).

Now, could we write this as e1*(something) + e2*(something)?
(RG - XB) + e2*(RB + XG)

The real part (RG - XB) is not naturally expressed as e1*(...) because e1 is not a scalar.
We could write:
= 1*(RG - XB) + e2*(RB + XG)

There is no reason to involve e1 (the "h" analog) in this expression. The standard complex
multiplication does not produce e1 terms.

However, if we had a DIFFERENT physical setup where e1-components arose naturally
(e.g., a circuit with hyperbolic-signature coupling), then Cl(1,1) could provide
a richer decomposition. This connects to the published work on hyperbolic quaternion
formulations of electromagnetism (Springer 2010).

## Summary

| Question | Answer |
|----------|--------|
| Does Cl(1,1) give a non-trivial h? | Yes: e1 with e1^2 = 1, e1 != +/-1 |
| Does Cl(1,1) satisfy ALL of Dollard's axioms? | NO: jk = h, not 1 (non-commutativity breaks Z_4) |
| Can Dollard's axioms be modified to get Cl(1,1)? | Yes: replace commutativity with anticommutativity |
| Would the versor form work in Cl(1,1)? | Not directly: complex multiplication doesn't produce e1 terms |
| Is Cl(1,1) useful for electromagnetism? | Yes: published applications in EM curve theory and hyperbolic EM |
| Is this what Dollard describes? | No: fundamentally different algebra |
