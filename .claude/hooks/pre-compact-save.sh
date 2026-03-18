#!/bin/bash
# Pre-compaction hook: archive transcript before context window compresses
# Fires on both manual /compact and automatic compaction

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path')
TRIGGER=$(echo "$INPUT" | jq -r '.trigger')
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)

BACKUP_DIR="$HOME/.claude/session-backups"
mkdir -p "$BACKUP_DIR"

# Archive the full transcript (the raw conversation before compaction)
if [ -f "$TRANSCRIPT_PATH" ]; then
  cp "$TRANSCRIPT_PATH" "$BACKUP_DIR/${TIMESTAMP}-${TRIGGER}-compact.jsonl"
fi

# Log the compaction event
echo "[$TIMESTAMP] Session $SESSION_ID: $TRIGGER compaction. Transcript saved." \
  >> "$BACKUP_DIR/compaction-log.txt"

exit 0
