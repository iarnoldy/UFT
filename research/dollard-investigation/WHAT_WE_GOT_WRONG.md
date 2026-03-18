# What We Got Wrong — Honest Account

**Date**: 2026-03-17
**Author**: Sophia 3.1 (Claude), with correction by Ian Michael Arnoldy

## The Error

We analyzed the wrong mathematical construction for three research councils, then claimed
the investigation was complete.

### What Dollard Actually Writes (Versor Algebra, eq 67-77)

Dollard decomposes epsilon^(j*theta) into four groups by operator:

```
epsilon^(j*theta) = 1*u(theta) + j*x(theta) + h*nu(theta) + k*y(theta)    [eq 77]
```

Where u, x, nu, y are SCALAR PARTS (all positive for theta > 0):
- u(theta) = Sum theta^(4n) / (4n)!
- x(theta) = Sum theta^(4n+1) / (4n+1)!
- nu(theta) = Sum theta^(4n+2) / (4n+2)!
- y(theta) = Sum theta^(4n+3) / (4n+3)!

And {1, j, h, k} = {1, j, -1, -j} are the OPERATORS that carry sign structure.

### What We Analyzed Instead

We stripped the operators and treated (u, x, nu, y) as a bare real 4-vector in R^4.
We then analyzed cyclic convolution on this bare vector — which has a circulant matrix
with eigenvalues {e^theta, e^(j*theta), e^(-theta), e^(-j*theta)}. The spectral radius
is e^theta > 1, causing exponential error growth.

This analysis is mathematically correct. But it tests the STRIPPED version, not Dollard's
operator-valued construction.

### How the Error Propagated

1. **Parent session** (2026-03-17-0253): Discovered gross/net energy structure.
   Correctly identified that u, x, v, y are all positive for real t > 0.
   **But**: attributed this to "Dollard's quaternary expansion" when Dollard's actual
   expansion (epsilon^j) groups by operator, not by bare scalar.

2. **Council 1** (quaternary-performance): Tested stride-4 Taylor and projection quality
   for the mod-4 real subseries. Found stride-4 saves 40% FLOPs, projection is 15-68x
   worse. **Correct analysis of the wrong thing.**

3. **Council 2** (lifted-representation): Tested whether staying in the (u,x,v,y) basis
   avoids singularities. Round 3 (Dollard Theorist) proved fatal flaw: circulant spectral
   radius e^theta > 1. K4/K5/K8 fire. KILLED.
   **Correct analysis of the wrong thing — again.**

4. **The QA catch**: Ian asked to verify the agent/skill against Dollard's source text.
   Reading eq (76) directly revealed: the scalar parts ARE all positive, but they're
   coefficients of OPERATORS {1, j, h, k}. The full algebraic element constrains the
   result differently than the bare 4-vector.

5. **The exact construction**: Implementing Dollard's actual process (eq 18-82, with
   operators, Z4 algebra multiplication) shows unexpected zero-error at specific chain
   lengths. This was NOT predicted by the council analysis and remains unexplained.

### Root Cause

**We projected our framework onto Dollard instead of following his instructions.**

The first council warned: "we keep projecting OUR frameworks onto Dollard." We then
proceeded to do exactly that — taking his structural pattern (mod-4 grouping), applying
it to a different argument (real e^t instead of his epsilon^j), finding a property
(all-positive terms without operators), and building an entire hypothesis (DPQA) on
our modified version while claiming to test his construction.

### The Lesson

This is now a hardcoded feedback memory (feedback_follow_source_text.md):

> Before ANY analysis of an external author's mathematical system:
> 1. Open the source text
> 2. Copy their equations verbatim
> 3. Implement step by step in their notation
> 4. Only THEN analyze properties
> 5. If you find yourself saying "this is equivalent to..." STOP

### What the Error Cost

- Three research councils (~4 hours of computation, ~130KB of analysis)
- Incorrect "STOP" verdicts that almost terminated the investigation
- The correct investigation (exact construction from source text) happened only because
  Ian insisted on QA against the source text

### What the Error Revealed

- The exact construction with operators shows different numerical behavior than predicted
- Zero-error at n=500, 1000 while standard rotation accumulates error
- This finding would not have been discovered if we hadn't caught the error
- The investigation is now OPEN, not closed

### The Silver Lining

The councils' work is not wasted:
- The Z4 algebraic classification (council 1) is correct and settled
- The stride-4 Taylor advantage (council 2) is real and niche
- The compensated arithmetic analysis (council 3) is valid reference material
- The eigenvalue analysis of the STRIPPED circulant is correct mathematics
- The error itself is documented as a case study in research methodology
