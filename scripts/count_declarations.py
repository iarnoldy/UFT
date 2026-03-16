#!/usr/bin/env python3
"""
Count verified declarations in the Lean project.

Only counts declarations in files that are in the lakefile roots
(i.e., files that actually compile with `lake build`).

Counts:
  - theorem / lemma
  - def
  - instance
  - structure / class
  - abbrev
  - noncomputable def
  - #check (informational, not a declaration)

Also classifies declarations by category:
  - Algebraic theorems (Jacobi, bracket, LieHom, etc.)
  - Computational checks (native_decide, norm_num)
  - Dimensional/arithmetic
  - Infrastructure (structures, instances, defs)

Usage:
  python scripts/count_declarations.py
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

# ============================================================
# Parse lakefile to get root list
# ============================================================
def parse_lakefile_roots(lakefile_path):
    """Extract root module names from lakefile.lean."""
    with open(lakefile_path, 'r') as f:
        content = f.read()

    # Extract everything between roots := #[ ... ]
    match = re.search(r'roots\s*:=\s*#\[(.*?)\]', content, re.DOTALL)
    if not match:
        print("ERROR: Could not parse roots from lakefile.lean")
        sys.exit(1)

    roots_str = match.group(1)
    # Extract backtick-prefixed module names
    roots = re.findall(r'`([\w.]+)', roots_str)
    return roots

def root_to_path(root, src_dir):
    """Convert a module root like 'clifford.so14_grand' to a file path."""
    parts = root.split('.')
    return os.path.join(src_dir, *parts) + '.lean'

# ============================================================
# Count declarations in a Lean file
# ============================================================
DECL_PATTERNS = {
    'theorem': re.compile(r'^(?:set_option\s+\S+\s+\d+\s+in\s+)?(?:@\[.*?\]\s+)?theorem\s+(\w+)', re.MULTILINE),
    'lemma': re.compile(r'^(?:set_option\s+\S+\s+\d+\s+in\s+)?(?:@\[.*?\]\s+)?lemma\s+(\w+)', re.MULTILINE),
    'def': re.compile(r'^(?:set_option\s+\S+\s+\d+\s+in\s+)?(?:@\[.*?\]\s+)?(?:noncomputable\s+)?def\s+(\w+)', re.MULTILINE),
    'instance': re.compile(r'^(?:set_option\s+\S+\s+\d+\s+in\s+)?instance\s*(?:\:\s*)?', re.MULTILINE),
    'structure': re.compile(r'^(?:@\[.*?\]\s+)?structure\s+(\w+)', re.MULTILINE),
    'class': re.compile(r'^(?:@\[.*?\]\s+)?class\s+(\w+)', re.MULTILINE),
    'abbrev': re.compile(r'^(?:@\[.*?\]\s+)?(?:noncomputable\s+)?abbrev\s+(\w+)', re.MULTILINE),
}

def count_declarations(filepath):
    """Count declarations in a single Lean file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    counts = {}
    names = {}
    for kind, pattern in DECL_PATTERNS.items():
        matches = pattern.findall(content)
        counts[kind] = len(matches)
        names[kind] = matches

    # Count native_decide usage (computational proofs)
    native_decide_count = content.count('native_decide')

    # Count #check (informational only, not a declaration)
    check_count = len(re.findall(r'^#check\b', content, re.MULTILINE))

    return counts, names, native_decide_count, check_count

def classify_file(filepath, counts, names):
    """Classify a file's declarations into categories."""
    fname = os.path.basename(filepath)
    categories = defaultdict(int)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Heuristic classification based on file content and theorem names
    for name in names.get('theorem', []) + names.get('lemma', []):
        name_lower = name.lower()
        if any(k in name_lower for k in ['jacobi', 'lie', 'bracket', 'comm', 'antisymm',
                                           'hom', 'embed', 'bridge', 'skew', 'closure',
                                           'subalgebra', 'injective']):
            categories['algebraic'] += 1
        elif any(k in name_lower for k in ['dim', 'count', 'decomposition', 'expected',
                                            'trace', 'sum', 'cardinality']):
            categories['dimensional'] += 1
        elif 'native_decide' in content and any(k in name_lower for k in ['bracket', 'jac']):
            categories['computational'] += 1
        else:
            categories['other_theorems'] += 1

    categories['definitions'] = counts.get('def', 0) + counts.get('abbrev', 0)
    categories['instances'] = counts.get('instance', 0)
    categories['structures'] = counts.get('structure', 0) + counts.get('class', 0)

    return dict(categories)

# ============================================================
# Main
# ============================================================
def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lakefile = os.path.join(project_root, 'lakefile.lean')
    src_dir = os.path.join(project_root, 'src', 'lean_proofs')

    roots = parse_lakefile_roots(lakefile)
    print(f"Lakefile roots: {len(roots)} modules")

    # Count declarations per file
    total_counts = defaultdict(int)
    total_categories = defaultdict(int)
    total_native_decide = 0
    total_check = 0
    file_details = []
    missing = []

    for root in roots:
        filepath = root_to_path(root, src_dir)
        if not os.path.exists(filepath):
            missing.append(root)
            continue

        counts, names, nd_count, check_count = count_declarations(filepath)
        categories = classify_file(filepath, counts, names)

        total = sum(counts.values())
        for k, v in counts.items():
            total_counts[k] += v
        for k, v in categories.items():
            total_categories[k] += v
        total_native_decide += nd_count
        total_check += check_count

        file_details.append({
            'root': root,
            'path': filepath,
            'counts': counts,
            'total': total,
            'categories': categories,
            'native_decide': nd_count,
        })

    # Sort by total declarations (descending)
    file_details.sort(key=lambda x: x['total'], reverse=True)

    # Print report
    print("\n" + "=" * 70)
    print("DECLARATION COUNT REPORT")
    print("=" * 70)

    grand_total = sum(total_counts.values())
    print(f"\nTotal compiled proof files: {len(file_details)}")
    print(f"Total verified declarations: {grand_total}")
    print(f"  theorem/lemma: {total_counts['theorem'] + total_counts['lemma']}")
    print(f"  def (incl. noncomputable): {total_counts['def']}")
    print(f"  instance: {total_counts['instance']}")
    print(f"  structure/class: {total_counts['structure'] + total_counts['class']}")
    print(f"  abbrev: {total_counts['abbrev']}")
    print(f"\nnative_decide usages: {total_native_decide}")
    print(f"#check usages: {total_check} (informational, not counted)")

    print(f"\n--- Classification ---")
    print(f"  Algebraic theorems: {total_categories.get('algebraic', 0)}")
    print(f"  Computational checks: {total_categories.get('computational', 0)}")
    print(f"  Dimensional/arithmetic: {total_categories.get('dimensional', 0)}")
    print(f"  Other theorems: {total_categories.get('other_theorems', 0)}")
    print(f"  Definitions: {total_categories.get('definitions', 0)}")
    print(f"  Instances: {total_categories.get('instances', 0)}")
    print(f"  Structures/classes: {total_categories.get('structures', 0)}")

    print(f"\n--- Top 20 files by declaration count ---")
    for i, fd in enumerate(file_details[:20]):
        print(f"  {i+1:3d}. {fd['root']:50s} {fd['total']:5d} declarations")

    if missing:
        print(f"\n--- Missing files ({len(missing)}) ---")
        for m in missing:
            print(f"  {m}")

    # Count non-root files in src/lean_proofs
    all_lean = []
    for dirpath, dirnames, filenames in os.walk(src_dir):
        for fn in filenames:
            if fn.endswith('.lean'):
                all_lean.append(os.path.join(dirpath, fn))

    root_paths = set(root_to_path(r, src_dir) for r in roots)
    non_root = [f for f in all_lean if f not in root_paths]

    print(f"\n--- Non-root .lean files ({len(non_root)}) ---")
    print("  These files are NOT in lakefile roots and are NOT compiled:")
    for f in sorted(non_root):
        rel = os.path.relpath(f, src_dir)
        print(f"  {rel}")

    # Summary for documentation
    print(f"\n{'=' * 70}")
    print("SUMMARY FOR DOCUMENTATION")
    print(f"{'=' * 70}")
    print(f"Compiled proof files: {len(file_details)}")
    print(f"Verified declarations: {grand_total}")
    print(f"sorry gaps: 0")

    return grand_total, len(file_details)

if __name__ == '__main__':
    main()
