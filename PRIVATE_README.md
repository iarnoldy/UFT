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

- **47 proof files, ~1,940 verified declarations, 0 sorry, 0 errors**
- Papers 1-3 on public repo. Paper 4 private only.
- KC-E3 (chirality): REFINED. Massive chirality definition machine-verified.
