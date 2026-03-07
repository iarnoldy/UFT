#!/usr/bin/env bash
# run-tests-on-src-change.sh -- Auto-run tests when src/ files change
#
# Runs Python tests if any exist. Lean compilation check is manual
# (requires lake, which may not be installed).

TESTS_DIR="src/tests"

if [ -d "$TESTS_DIR" ] && ls "$TESTS_DIR"/test_*.py 1>/dev/null 2>&1; then
    echo "Running tests..."
    python -m pytest "$TESTS_DIR" -q --tb=short 2>/dev/null || true
else
    echo "No test files found in $TESTS_DIR -- skipping."
fi
