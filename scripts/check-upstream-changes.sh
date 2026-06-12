#!/usr/bin/env bash
#
# check-upstream-changes.sh
#
# Non-destructive check for upstream humanizer changes since last sync.
# Reads prose/.humanizer-sync tracking file, queries upstream state via
# gh api (preferred) or shallow git clone (fallback), and reports
# changes without modifying local files.
#
# Usage: scripts/check-upstream-changes.sh
#
# Exit codes:
#   0 - Success (changes found or no changes)
#   1 - Error (missing tracking file, network failure, etc.)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TRACKING_FILE="$REPO_ROOT/prose/.humanizer-sync"
UPSTREAM_REPO="blader/humanizer"
UPSTREAM_FILE="SKILL.md"

# Cleanup handler for temp directories
TEMP_DIR=""
cleanup() {
    if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
}
trap cleanup EXIT

# Colors (disabled if not a terminal)
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    RED='\033[0;31m'
    BOLD='\033[1m'
    RESET='\033[0m'
else
    GREEN=''
    YELLOW=''
    RED=''
    BOLD=''
    RESET=''
fi

info()  { echo -e "${GREEN}$*${RESET}"; }
warn()  { echo -e "${YELLOW}$*${RESET}"; }
error() { echo -e "${RED}ERROR: $*${RESET}" >&2; }

# Check required tools
if ! command -v jq &>/dev/null; then
    error "jq is required but not installed. Install it: brew install jq (macOS) or apt install jq (Linux)"
    exit 1
fi

# Check tracking file exists
if [ ! -f "$TRACKING_FILE" ]; then
    error "Tracking file not found: $TRACKING_FILE"
    echo ""
    echo "No sync baseline exists. Run /update-humanizer to establish the initial baseline."
    exit 1
fi

# Read tracking file
LAST_COMMIT=$(jq -r '.last_sync_commit' "$TRACKING_FILE")
LAST_DATE=$(jq -r '.last_sync_date' "$TRACKING_FILE")

if [ -z "$LAST_COMMIT" ] || [ "$LAST_COMMIT" = "null" ]; then
    error "Invalid tracking file: missing last_sync_commit"
    exit 1
fi

if ! [[ "$LAST_COMMIT" =~ ^[0-9a-f]{40}$ ]]; then
    error "Invalid commit SHA in tracking file: must be 40 hex characters"
    exit 1
fi

if [ -z "$LAST_DATE" ] || [ "$LAST_DATE" = "null" ]; then
    error "Invalid tracking file: missing last_sync_date"
    exit 1
fi

if ! [[ "$LAST_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    error "Invalid date format in tracking file: expected YYYY-MM-DD"
    exit 1
fi

echo -e "${BOLD}Humanizer Upstream Check${RESET}"
echo "Upstream: https://github.com/$UPSTREAM_REPO"
echo "Last sync: $LAST_COMMIT (${LAST_DATE})"
echo ""

# Try gh api first (faster, no clone needed)
get_upstream_via_gh() {
    if ! command -v gh &>/dev/null; then
        return 1
    fi

    # Get latest commit on main
    local latest_sha
    latest_sha=$(gh api "repos/$UPSTREAM_REPO/commits/main" --jq '.sha' 2>/dev/null) || return 1

    if [ "$latest_sha" = "$LAST_COMMIT" ]; then
        info "No upstream changes since last sync ($LAST_DATE)."
        return 0
    fi

    warn "Upstream has new changes."
    echo ""

    # Get comparison between last sync and current HEAD
    local compare_json
    compare_json=$(gh api "repos/$UPSTREAM_REPO/compare/${LAST_COMMIT}...main" 2>/dev/null) || {
        # Compare API failed; fall back to git clone for better diagnostics
        return 1
    }

    local total_commits
    total_commits=$(echo "$compare_json" | jq -r '.total_commits')
    echo -e "${BOLD}Commits since last sync: $total_commits${RESET}"
    echo ""

    # Show commit messages
    echo -e "${BOLD}Commit log:${RESET}"
    echo "$compare_json" | jq -r '.commits[] | "  \(.sha[0:7]) \(.commit.message | split("\n")[0])"'
    echo ""

    # Show changes to SKILL.md specifically
    local skill_changes
    skill_changes=$(echo "$compare_json" | jq -r '.files[] | select(.filename == "'"$UPSTREAM_FILE"'") | "  Status: \(.status)\n  Additions: +\(.additions)\n  Deletions: -\(.deletions)\n  Changes: \(.changes)"')

    if [ -n "$skill_changes" ]; then
        echo -e "${BOLD}Changes to $UPSTREAM_FILE:${RESET}"
        echo -e "$skill_changes"
    else
        echo -e "${BOLD}No changes to $UPSTREAM_FILE${RESET} (changes are in other files only)."
    fi

    echo ""
    echo "Current upstream HEAD: ${latest_sha:0:12}"
    echo ""
    echo "To merge these changes, run: /update-humanizer"

    return 0
}

# Fallback: shallow git clone
get_upstream_via_git() {
    if ! command -v git &>/dev/null; then
        error "Neither gh nor git is available. Cannot check upstream."
        exit 1
    fi

    TEMP_DIR=$(mktemp -d)
    echo "Using git clone fallback (gh CLI not available)..."
    echo ""

    git clone --depth 50 --quiet "https://github.com/$UPSTREAM_REPO.git" "$TEMP_DIR" || {
        error "Failed to clone upstream repository. Check network connectivity."
        exit 1
    }

    local latest_sha
    latest_sha=$(git -C "$TEMP_DIR" rev-parse HEAD)

    if [ "$latest_sha" = "$LAST_COMMIT" ]; then
        info "No upstream changes since last sync ($LAST_DATE)."
        return 0
    fi

    # Check if the last sync commit exists in the cloned history
    if ! git -C "$TEMP_DIR" cat-file -e "$LAST_COMMIT" 2>/dev/null; then
        error "Last sync commit $LAST_COMMIT not found in recent upstream history."
        echo "This may be because:"
        echo "  - The upstream repo was force-pushed or rebased"
        echo "  - More than 50 commits have been made since last sync"
        echo "Install the GitHub CLI (gh) for full history access, or"
        echo "delete prose/.humanizer-sync and run /update-humanizer to reset the baseline."
        exit 1
    fi

    warn "Upstream has new changes."
    echo ""

    local commit_count
    commit_count=$(git -C "$TEMP_DIR" rev-list --count "$LAST_COMMIT..HEAD")
    echo -e "${BOLD}Commits since last sync: $commit_count${RESET}"
    echo ""

    echo -e "${BOLD}Commit log:${RESET}"
    git -C "$TEMP_DIR" log --oneline "$LAST_COMMIT..HEAD" | sed 's/^/  /'
    echo ""

    # Show diff stats for SKILL.md
    local diff_stat
    diff_stat=$(git -C "$TEMP_DIR" diff --stat "$LAST_COMMIT..HEAD" -- "$UPSTREAM_FILE" 2>/dev/null)

    if [ -n "$diff_stat" ]; then
        echo -e "${BOLD}Changes to $UPSTREAM_FILE:${RESET}"
        echo "$diff_stat" | sed 's/^/  /'
    else
        echo -e "${BOLD}No changes to $UPSTREAM_FILE${RESET} (changes are in other files only)."
    fi

    echo ""
    echo "Current upstream HEAD: ${latest_sha:0:12}"
    echo ""
    echo "To merge these changes, run: /update-humanizer"

    return 0
}

# Try gh first, fall back to git
if get_upstream_via_gh; then
    exit 0
fi

get_upstream_via_git
