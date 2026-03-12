# UFT Private Mirror

Private backup of the [UFT public repository](https://github.com/iarnoldy/UFT).

## What's Here That Isn't Public

| File | Why Private |
|------|-------------|
| `paper/paper4.tex` + `.pdf` | Three-Generation Letter — draft, not yet submitted |
| `paper/AACA-S-26-00059.pdf` | Springer submission confirmation for Paper 2 |
| `paper/paper4Notes.bib` | Bibliography notes for Paper 4 |
| `.claude/sessions/` | Development session logs |
| `docs/HANDOFF_GROK_QUESTIONS.md` | Internal research notes |

## Workflow

Default push goes to **private** (safe). Public push requires explicit command.

```bash
git push                  # -> private (safe default)
git push private main     # -> private (explicit)
git push origin main      # -> PUBLIC (intentional only)
```

## When to Move Files Public

| File | Push to Public When |
|------|-------------------|
| Paper 4 | After submission to PRL/LMP |
| AACA confirmation | Never |
| Paper 1 updates | Before April 1 CICM deadline |
| Session logs | Never (no value to public) |

## Remotes

- `origin` = `https://github.com/iarnoldy/UFT` (PUBLIC)
- `private` = `https://github.com/iarnoldy/UFT-private` (PRIVATE)

## Status

- **59 proof files, ~2,537 verified declarations, 0 sorry, 0 errors**
- First machine-verified so(10) spinor rep homomorphism in any ITP (1,980 bracket equations)
- 4 Lie algebras have mathlib `LieRing` + `LieAlgebra ℝ` instances (Bivector, SL3, SL5, SO10)
- Papers 1-2 submitted. Paper 3 blocked (arXiv endorsement). Paper 4 private draft.
- F2 Phase 2.1 (spinor rep) COMPLETE. F1 Phase 1.0 partially done. F2.0 + F3 remaining.
- d²=0 is now a theorem (from mathlib), not an axiom
- Clifford relation Cl(1,3) verified from 256-term multiplication table
- Killing form computed, Lie bracket proved metric-independent
- **ARCHITECTURAL DEBT**: 3 spinor rep files use different bases — needs Phase 2.1.5 unification
