# src/tests/ -- Test Classification Rules

## Test Categories

Every test must be classified as one of:

- **REAL**: Tests a falsifiable property. If the test passes, it provides evidence.
  If it fails, something is wrong. Example: "Lean proof compiles without sorry."

- **PROPERTY**: Tests an invariant or structural property. Example: "All .lean files
  in polyphase/ import the foundations module."

- **SMOKE**: Quick sanity check. Example: "Python metadata module imports without error."

## Rules

1. Every test file must have a comment at the top declaring its classification
2. REAL tests must have falsification criteria (what failure means)
3. Tests that always pass are not REAL tests -- classify as SMOKE
4. Integration tests go in `integration/` subdirectory

## Naming Convention

```
test_{category}_{what_it_tests}.py
```

Example: `test_real_lean_compilation.py`, `test_smoke_imports.py`
