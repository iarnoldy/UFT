# Web Research Results

## Search 1: Flux x Charge as Action
Query: "magnetic flux" times "electric charge" action integral Lagrangian electromagnetic units joule-seconds
Results:
- Weber * Coulomb = V*s * A*s = J*s = units of action. CONFIRMED.
- The product of magnetic flux (Wb) and electric charge (C) has dimensions of J*s, which are the units of action.
- In Lagrangian circuit theory, charge and flux linkage serve as generalized coordinates.
- The Lagrangian for an LC circuit: L = T - V = (1/2)Li^2 - q^2/(2C), with q as generalized coordinate, Li as conjugate momentum (which has units of flux linkage).
- Sources: [Lagrangian for Circuits](https://pmc.ncbi.nlm.nih.gov/articles/PMC7514363/), [UCSD Lagrangian EM](https://quantummechanics.ucsd.edu/ph130a/130_notes/node452.html)

## Search 2: Lagrangian Circuit Theory Details
Query: Lagrangian circuit theory charge flux linkage generalized coordinates coenergy
Results:
- In circuit Lagrangian mechanics, charge q is the generalized coordinate and flux linkage lambda is the conjugate momentum (or vice versa depending on formulation).
- Cherry and Miller (1951) introduced energy and coenergy for reactive elements.
- The Lagrangian is L = coenergy(inductors) - energy(capacitors) = (1/2)Li^2 - q^2/(2C).
- Generalized momentum: p = dL/dq_dot = Li = flux linkage lambda.
- Action S = integral(L dt) has units of J*s.
- The product q*lambda = charge * flux linkage has units of J*s = action.
- Sources: [MDPI Lagrangian Circuits](https://www.mdpi.com/1099-4300/21/11/1059), [n-Category Cafe Coenergy](https://golem.ph.utexas.edu/category/2010/01/coenergy.html)

## Search 3: Flux Quantum and Action
Query: Planck constant magnetic flux quantum charge action
Results:
- Magnetic flux quantum: Phi_0 = h/(2e) = 2.068e-15 Wb
- Therefore: Phi_0 * (2e) = h (Planck's constant)
- flux * charge = action is EXACTLY the relationship Phi_0 * 2e = h
- This is not Dollard's discovery -- it is fundamental to quantum electrodynamics and superconductivity.
- Sources: [Wikipedia Magnetic Flux Quantum](https://en.wikipedia.org/wiki/Magnetic_flux_quantum), [Wikipedia Planck Constant](https://en.wikipedia.org/wiki/Planck_constant)

## Search 4: Theorem Provers on Fringe Math
Query: theorem prover formal verification alternative science fringe mathematics
Results:
- NO prior art found for using theorem provers specifically to verify fringe/alternative mathematical claims.
- Terence Tao used Lean to formalize proofs and discovered small mistakes in published work (PFR conjecture formalization).
- Proof assistants have found errors in established mathematics during formalization.
- This project (dollard-formal-verification) may be the FIRST instance of using a theorem prover to formally verify claims from an alternative/fringe mathematical framework.
- Sources: [Lean Forward](https://lean-forward.github.io/), [Tao Mastodon](https://mathstodon.xyz/@tao/111206761117553482)

## Search 5: Split-Complex Numbers
Query: split-complex numbers h^2=1 Clifford algebra hyperbolic unit
Results:
- Split-complex numbers (hyperbolic numbers): z = a + bj where j^2 = +1 (NOT j^2 = -1).
- Isomorphic to Clifford algebra Cl(1,0)(R).
- Contains zero divisors and idempotents: e1 = (1+j)/2, e2 = (1-j)/2.
- William Kingdon Clifford used them for sums of spins.
- Related to Lorentz transformations in 1+1D spacetime.
- NOT a field (unlike complex numbers) due to zero divisors.
- KEY FINDING: In split-complex numbers, j^2 = 1 but j != +/-1. This is exactly the algebraic structure Dollard wants for h!
- But: Dollard also requires h^1 = -1, which forces h = -1 in ANY number system. The split-complex unit j satisfies j^2 = 1 but j^1 = j, not -1.
- Sources: [Wikipedia Split-Complex](https://en.wikipedia.org/wiki/Split-complex_number), [Oregon State](https://books.physics.oregonstate.edu/GELG/csplit.html)

## Search 6: Steinmetz-Fortescue History
Query: Steinmetz Fortescue symmetrical components history
Results:
- Fortescue (1918): "Method of Symmetrical Co-Ordinates Applied to the Solution of Polyphase Networks" at 34th AIEE convention.
- Demonstrated any N unbalanced phasors = sum of N balanced sets (for prime N).
- Steinmetz contributed 25 pages extending the work. Steinmetz was earlier (complex phasor analysis of AC).
- Timeline: Tesla (discovery, 1880s) -> Steinmetz (complex analysis of AC, 1890s) -> Fortescue (symmetrical components, 1918) -> Dollard (claims theoretical basis, ~2000s).
- Dollard claims there was "never a theoretical basis" for Fortescue's method until he created it. This is false -- Fortescue's paper IS the theoretical basis, and it is standard DFT.
- Sources: [Iowa State EE](https://home.engineering.iastate.edu/~jdm/ee457/SymmetricalComponents1.pdf), [MDPI 100 Years](https://www.mdpi.com/1996-1073/12/3/450)

## Search 7: Fortescue in Non-EE Domains
Query: Fortescue symmetrical components signal processing neuroscience non-electrical
Results:
- NO evidence found of Fortescue symmetrical components being applied in signal processing, neuroscience, or non-EE domains.
- The method remains confined to electrical engineering, specifically power systems.
- The N-Phase project's application to EEG (E007, p=0.033) may be a GENUINE FIRST application of Fortescue-type decomposition to neuroscience data.
- Sources: [MDPI 100 Years](https://www.mdpi.com/1996-1073/12/3/450), [Wikipedia Symmetrical Components](https://en.wikipedia.org/wiki/Symmetrical_components)

## Search 8: Lean 4 Physics Formalization
Query: Lean 4 mathlib formalize physics electrodynamics Maxwell
Results:
- PhysLib: community-driven Lean4 formal physics reasoning (unit systems, basic mechanics).
- HepLean: high-energy physics formalization using Lean 4 and mathlib.
- Lean4Physics: comprehensive reasoning framework for college-level physics.
- Mathlib does NOT yet have div/grad/curl formalized (needed for Maxwell's equations).
- Formalizing Chemical Physics: Lean used for molecular dynamics formalization.
- State of art: physics formalization in Lean is nascent. No one has formalized Maxwell's equations.
- Sources: [Lean4Physics](https://arxiv.org/html/2510.26094v1), [HepLean](https://arxiv.org/html/2411.07667v1)
