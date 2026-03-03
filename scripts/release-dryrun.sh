#!/usr/bin/env bash
set -euo pipefail

############################################
# DRY-RUN RELEASE SCRIPT — USAGE & BEHAVIOR
############################################
#
# This script previews what commits would be included in a release,
# which version bump would occur, and what would appear in the changelog.
# 
# It DOES NOT commit, tag, or modify any files.
#
# Usage:
#   ./scripts/release-dryrun.sh           # dry-run using commits since last tag
#   ./scripts/release-dryrun.sh --all    # consider all commits in repo
#
# Commit message rules (release-worthy):
#   - Must start with one of:
#       add:  upd:  dep:  rem:  fix:  sec:
#   - Breaking change: add ! after type, e.g., upd!:
#   - Must be lowercase and include colon
# 
# Commits starting with:
#   tes:  cle:
# or any other format are ignored.
############################################

INCLUDE_TYPES="add|upd|dep|rem|fix|sec"
EXCLUDE_TYPES="tes|cle"

# Check if --all flag is used
USE_ALL=false
if [[ "${1:-}" == "--all" ]]; then
  USE_ALL=true
fi

############################################
# Determine range of commits to inspect
############################################
if $USE_ALL; then
  RANGE=""
  echo "🔹 Dry-run: considering ALL commits in the repository."
else
  LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || true)
  if [[ -z "$LAST_TAG" ]]; then
    RANGE=""
    echo "🔹 Dry-run: no tags found, considering all commits."
  else
    RANGE="$LAST_TAG..HEAD"
    echo "🔹 Dry-run: considering commits since last tag: $LAST_TAG"
  fi
fi

############################################
# Collect commit messages
############################################
COMMITS=$(git log $RANGE --pretty=format:"%s")

if [[ -z "$COMMITS" ]]; then
  echo "⚠️  No commits found in the range."
  exit 0
fi

echo ""
echo "=== All commits in range ==="
echo "$COMMITS"
echo "============================"
echo ""

############################################
# Classify commits
############################################
RELEASE_COMMITS=()
IGNORED_COMMITS=()

while IFS= read -r line; do
  if [[ "$line" =~ ^(${INCLUDE_TYPES})(!?)\: ]]; then
    RELEASE_COMMITS+=("$line")
  else
    IGNORED_COMMITS+=("$line")
  fi
done <<< "$COMMITS"

############################################
# Display grouped commits
############################################
echo "=== Release-worthy commits ==="
if [[ ${#RELEASE_COMMITS[@]} -eq 0 ]]; then
  echo "No release-worthy commits found."
else
  for TYPE in add upd dep rem fix sec; do
    TYPE_MATCHES=()
    for COMMIT in "${RELEASE_COMMITS[@]}"; do
      if [[ "$COMMIT" =~ ^(${TYPE})(!?)\: ]]; then
        TYPE_MATCHES+=("$COMMIT")
      fi
    done
    if [[ ${#TYPE_MATCHES[@]} -gt 0 ]]; then
      echo "### $TYPE"
      for COMMIT in "${TYPE_MATCHES[@]}"; do
        echo "- $COMMIT"
      done
      echo ""
    fi
  done
fi

############################################
# Display ignored commits
############################################
if [[ ${#IGNORED_COMMITS[@]} -gt 0 ]]; then
  echo "=== Ignored commits (not included in release) ==="
  for COMMIT in "${IGNORED_COMMITS[@]}"; do
    echo "- $COMMIT"
  done
  echo ""
fi

############################################
# Determine version bump
############################################
BUMP="patch"

# Breaking change triggers major
for COMMIT in "${RELEASE_COMMITS[@]}"; do
  if [[ "$COMMIT" =~ ^(${INCLUDE_TYPES})!\: ]]; then
    BUMP="major"
    break
  fi
done

# Minor bump if any add: or upd: and not already major
if [[ "$BUMP" == "patch" ]]; then
  for COMMIT in "${RELEASE_COMMITS[@]}"; do
    if [[ "$COMMIT" =~ ^(add|upd)(!?)\: ]]; then
      BUMP="minor"
      break
    fi
  done
fi

echo "=== Predicted version bump ==="
echo "Bump type: $BUMP"
echo ""

echo "✅ Dry-run complete. No files or tags were modified."