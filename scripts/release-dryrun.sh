#!/usr/bin/env bash
set -euo pipefail

INCLUDE_TYPES="add|upd|dep|rem|fix|sec"
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || true)
RANGE="$LAST_TAG..HEAD"

COMMITS=$(git log $RANGE --pretty=format:"%s")
RELEASE_COMMITS=$(echo "$COMMITS" | grep -E "^(${INCLUDE_TYPES})(!?)\:" || true)

if [[ -z "$RELEASE_COMMITS" ]]; then
  echo "No release-worthy commits since last tag."
  exit 0
fi

echo "=== Dry Run Release Preview ==="
echo "Commits that would go into the release:"
echo "$RELEASE_COMMITS"