#!/usr/bin/env bash
# protect-results.sh -- Block direct edits to experiment results
#
# Results in src/experiments/results/ are append-only.
# New results must be written via metadata.save(), not edited directly.
# Only .gitkeep and results_schema.json are exempt.

FILE="$1"
BASENAME=$(basename "$FILE")

if [[ "$BASENAME" == ".gitkeep" || "$BASENAME" == "results_schema.json" ]]; then
    exit 0
fi

echo "BLOCKED: Experiment results are append-only."
echo "Use src/experiments/metadata.py:save() to write new results."
echo "To modify existing results, delete and re-run the experiment."
exit 1
