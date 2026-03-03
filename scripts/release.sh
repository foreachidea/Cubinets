############################################
# RELEASE SCRIPT — USAGE & BEHAVIOR
############################################
#
# PURPOSE
# -------
# Automates semantic versioning, changelog generation,
# and git tagging based on structured commit messages.
#
# REQUIRED COMMIT FORMAT
# ----------------------
# Commits must start with one of:
#
#   add:  upd:  dep:  rem:  fix:  sec:  tes:  cle:
#
# Breaking changes must use:
#
#   type!:
#
# Examples:
#   add: new module
#   upd!: change public api
#   fix: bbox rotation bug
#
# NOTES:
# - Messages must be lowercase.
# - Only these types are included in releases:
#     add, upd, dep, rem, fix, sec
# - tes: and cle: are ignored for changelog and version bump.
#
#
# VERSIONING RULES (SemVer)
# --------------------------
# Breaking change (!):  MAJOR bump
# add: or upd:         MINOR bump
# fix:, dep:, rem:, sec:  PATCH bump
#
# Version is stored in:
#   VERSION
#
# Changelog is written to:
#   CHANGELOG.md
#
#
# PRERELEASE SUPPORT
# ------------------
# Usage:
#
#   ./scripts/release.sh
#   ./scripts/release.sh --pre alpha
#   ./scripts/release.sh --pre beta
#   ./scripts/release.sh --pre rc
#
# Produces versions like:
#   1.2.0-beta.1
#   1.2.0-beta.2
#
#
# SAFETY CHECKS
# -------------
# - Aborts if working tree is dirty.
# - Aborts if in detached HEAD.
# - Aborts if no release-worthy commits.
#
#
# TAGGING
# -------
# Creates annotated tag:
#   vX.Y.Z
#
# Example:
#   v1.4.0
#
#
# COMPARE LINKS
# -------------
# If remote.origin.url exists, generates:
#
#   [Full Changelog](repo/compare/prevTag...vNewTag)
#
# Supports HTTPS and SSH remotes.
#
#
# TYPICAL WORKFLOW
# ----------------
# 1. Make structured commits.
# 2. Ensure working tree clean.
# 3. Run release script.
# 4. Push:
#      git push origin main --tags
#
#
# TODO / UPCOMING FEATURES
# ------------------------
# - You can maintain a "TODO / Upcoming Features" section at the top of CHANGELOG.md.
# - The script will detect this section and leave it untouched.
# - New release sections are prepended *below* the TODO section automatically.
#
# Example layout:
#
# ## TODO / Upcoming Features
# - Add cabinet presets
# - Improve cloning speed
#
# ## [1.4.0] - 2026-03-03
# ### Added
# - add: cabinet module
# ### Fixed
# - fix: bbox rotation issue
############################################

#!/usr/bin/env bash
set -euo pipefail

############################################
# CONFIGURATION
############################################

# Commit types that are included in changelog
INCLUDE_TYPES="add|upd|dep|rem|fix|sec"

# Commit types excluded from changelog
EXCLUDED_TYPES="tes|cle"

VERSION_FILE="VERSION"
CHANGELOG_FILE="CHANGELOG.md"

############################################
# ARGUMENT PARSING (Prerelease Support)
############################################

PRERELEASE_LABEL=""
if [[ "${1:-}" == "--pre" ]]; then
  PRERELEASE_LABEL="${2:-}"
  if [[ -z "$PRERELEASE_LABEL" ]]; then
    echo "❌ You must specify prerelease label (alpha|beta|rc etc)."
    exit 1
  fi
fi

############################################
# HARDENING CHECKS
############################################

# Prevent release from detached HEAD
if ! git symbolic-ref --quiet HEAD > /dev/null; then
  echo "❌ Cannot release from detached HEAD."
  exit 1
fi

# Ensure working directory clean
if ! git diff-index --quiet HEAD --; then
  echo "❌ Working directory not clean."
  exit 1
fi

# Ensure VERSION file exists
if [[ ! -f "$VERSION_FILE" ]]; then
  echo "0.0.0" > "$VERSION_FILE"
fi

############################################
# DETERMINE CURRENT VERSION
############################################

CURRENT_VERSION=$(cat "$VERSION_FILE")

# Extract base version (strip prerelease if exists)
BASE_VERSION=$(echo "$CURRENT_VERSION" | cut -d'-' -f1)

IFS='.' read -r MAJOR MINOR PATCH <<< "$BASE_VERSION"

############################################
# DETERMINE LAST TAG
############################################

LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || true)

if [[ -z "$LAST_TAG" ]]; then
  RANGE=""
else
  RANGE="$LAST_TAG..HEAD"
fi

############################################
# COLLECT COMMITS
############################################

COMMITS=$(git log $RANGE --pretty=format:"%s")

# Filter release-worthy commits
RELEASE_COMMITS=$(echo "$COMMITS" | grep -E "^(${INCLUDE_TYPES})(!?)\:" || true)

if [[ -z "$RELEASE_COMMITS" ]]; then
  echo "ℹ No release-worthy commits found."
  exit 0
fi

############################################
# DETERMINE VERSION BUMP
############################################

BUMP="patch"

# Breaking change → major
if echo "$RELEASE_COMMITS" | grep -qE "^(${INCLUDE_TYPES})!\:"; then
  BUMP="major"

# Feature change → minor
elif echo "$RELEASE_COMMITS" | grep -qE "^(add|upd)(!?)\:"; then
  BUMP="minor"
fi

# Only bump base version if NOT prerelease continuation
if [[ -z "$PRERELEASE_LABEL" ]]; then
  case $BUMP in
    major)
      ((MAJOR++))
      MINOR=0
      PATCH=0
      ;;
    minor)
      ((MINOR++))
      PATCH=0
      ;;
    patch)
      ((PATCH++))
      ;;
  esac
fi

NEW_BASE_VERSION="$MAJOR.$MINOR.$PATCH"

############################################
# HANDLE PRERELEASE LOGIC
############################################

if [[ -n "$PRERELEASE_LABEL" ]]; then
  # Count existing prereleases for same base + label
  COUNT=$(git tag -l "v${NEW_BASE_VERSION}-${PRERELEASE_LABEL}.*" | wc -l | tr -d ' ')
  NEXT=$((COUNT + 1))
  NEW_VERSION="${NEW_BASE_VERSION}-${PRERELEASE_LABEL}.${NEXT}"
else
  NEW_VERSION="$NEW_BASE_VERSION"
fi

############################################
# GENERATE CHANGELOG SECTION
############################################

DATE=$(date +%Y-%m-%d)

TMP_RELEASE_SECTION=$(mktemp)

echo "## [$NEW_VERSION] - $DATE" >> "$TMP_RELEASE_SECTION"
echo "" >> "$TMP_RELEASE_SECTION"

for TYPE in add upd dep rem fix sec
do
  TYPE_COMMITS=$(echo "$RELEASE_COMMITS" | grep -E "^(${TYPE})(!?)\:" || true)

  if [[ -n "$TYPE_COMMITS" ]]; then
    case $TYPE in
      add) echo "### Added" >> "$TMP_RELEASE_SECTION" ;;
      upd) echo "### Updated" >> "$TMP_RELEASE_SECTION" ;;
      dep) echo "### Deprecated" >> "$TMP_RELEASE_SECTION" ;;
      rem) echo "### Removed" >> "$TMP_RELEASE_SECTION" ;;
      fix) echo "### Fixed" >> "$TMP_RELEASE_SECTION" ;;
      sec) echo "### Security" >> "$TMP_RELEASE_SECTION" ;;
    esac

    echo "$TYPE_COMMITS" | sed 's/^/- /' >> "$TMP_RELEASE_SECTION"
    echo "" >> "$TMP_RELEASE_SECTION"
  fi
done

############################################
# GENERATE COMPARE LINK (GitHub/GitLab)
############################################

REMOTE_URL=$(git config --get remote.origin.url || true)

if [[ -n "$REMOTE_URL" ]]; then
  # Normalize SSH → HTTPS
  REPO_URL=$(echo "$REMOTE_URL" \
    | sed -E 's/git@([^:]+):/https:\/\/\1\//' \
    | sed -E 's/\.git$//')

  if [[ -n "$LAST_TAG" ]]; then
    COMPARE_URL="$REPO_URL/compare/$LAST_TAG...v$NEW_VERSION"
    echo "[Full Changelog]($COMPARE_URL)" >> "$TMP_RELEASE_SECTION"
    echo "" >> "$TMP_RELEASE_SECTION"
  fi
fi

############################################
# PREPEND TO CHANGELOG
############################################

# Extract TODO section if exists
TODO_SECTION=$(awk '/## TODO/{flag=1;next}/## \[/{flag=0}flag==1' "$CHANGELOG_FILE")

# Extract existing changelog below TODO
EXISTING_CHANGELOG=$(awk '/## \[/{flag=1}flag{print}' "$CHANGELOG_FILE")

# Prepend new release section after TODO
TMP_FILE=$(mktemp)

# Start with TODO
echo "# Changelog" >> "$TMP_FILE"
echo "" >> "$TMP_FILE"
if [[ -n "$TODO_SECTION" ]]; then
  echo "## TODO / Upcoming Features" >> "$TMP_FILE"
  echo "$TODO_SECTION" >> "$TMP_FILE"
  echo "" >> "$TMP_FILE"
fi

# New release at top of releases
cat "$TMP_RELEASE_SECTION" >> "$TMP_FILE"
echo "" >> "$TMP_FILE"

# Append existing releases (older first → preserves order)
if [[ -n "$EXISTING_RELEASES" ]]; then
  echo "$EXISTING_RELEASES" >> "$TMP_FILE"
fi

# Append legacy commits if they exist
awk '/## Early Development/{flag=1} flag' "$CHANGELOG_FILE" >> "$TMP_FILE"

mv "$TMP_FILE" "$CHANGELOG_FILE"

# Clean up temporary files
rm -f "$TMP_RELEASE_SECTION"

############################################
# UPDATE VERSION FILE
############################################

echo "$NEW_VERSION" > "$VERSION_FILE"

############################################
# COMMIT + TAG
############################################

git add "$VERSION_FILE" "$CHANGELOG_FILE"
git commit -m "cle: release v$NEW_VERSION"

git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"

echo "✔ Released v$NEW_VERSION"
