#!/bin/bash

# Branch name validation script
# Validates branch names against standard naming conventions
# Usage: ./validate-branch.sh <branch-name>

set -e

BRANCH_NAME="$1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Validation patterns
STANDARD_PATTERN='^(feature|bugfix|fix|hotfix|refactor|docs|test|chore|release|experiment)/[A-Z]+-[0-9]+-[a-z0-9-]+$'
RELEASE_PATTERN='^release/v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(-[a-zA-Z0-9.-]+)?$'

# Function to print success
success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print error
error() {
    echo -e "${RED}✗ $1${NC}"
}

# Function to print warning
warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Function to print info
info() {
    echo -e "$1"
}

# Check if branch name is provided
if [ -z "$BRANCH_NAME" ]; then
    error "No branch name provided"
    info "Usage: $0 <branch-name>"
    exit 1
fi

# Print validation header
info "\n=== Branch Name Validation ==="
info "Branch: $BRANCH_NAME\n"

# Validate against patterns
if [[ "$BRANCH_NAME" =~ $STANDARD_PATTERN ]]; then
    success "Branch name follows standard convention"

    # Extract components
    TYPE=$(echo "$BRANCH_NAME" | cut -d'/' -f1)
    SUFFIX=$(echo "$BRANCH_NAME" | cut -d'/' -f2)
    ISSUE_ID=$(echo "$SUFFIX" | grep -oP '^[A-Z]+-[0-9]+')
    DESCRIPTION=$(echo "$SUFFIX" | sed "s/^$ISSUE_ID-//")

    # Validate components
    info "\nComponents:"
    info "  Type: $TYPE"
    info "  Issue ID: $ISSUE_ID"
    info "  Description: $DESCRIPTION"

    # Validate type
    case "$TYPE" in
        feature|bugfix|fix|hotfix|refactor|docs|test|chore|experiment)
            success "Valid branch type"
            ;;
        *)
            warning "Uncommon branch type"
            ;;
    esac

    # Validate description
    if [ ${#DESCRIPTION} -lt 3 ]; then
        warning "Description is very short (< 3 characters)"
    elif [ ${#DESCRIPTION} -gt 50 ]; then
        warning "Description is very long (> 50 characters)"
    else
        success "Description length is appropriate"
    fi

    # Check for common issues
    if [[ "$DESCRIPTION" =~ [A-Z] ]]; then
        error "Description contains uppercase letters (should be kebab-case)"
        exit 1
    fi

    if [[ "$DESCRIPTION" =~ _ ]]; then
        error "Description contains underscores (use hyphens instead)"
        exit 1
    fi

    if [[ "$DESCRIPTION" =~ [^a-z0-9-] ]]; then
        error "Description contains invalid characters (only a-z, 0-9, - allowed)"
        exit 1
    fi

    if [[ "$DESCRIPTION" =~ ^- ]] || [[ "$DESCRIPTION" =~ -$ ]] || [[ "$DESCRIPTION" =~ -- ]]; then
        error "Description has invalid hyphen usage"
        exit 1
    fi

    success "All validation checks passed!\n"
    exit 0

elif [[ "$BRANCH_NAME" =~ $RELEASE_PATTERN ]]; then
    success "Branch name follows release convention"

    # Extract version
    VERSION=$(echo "$BRANCH_NAME" | sed 's/^release\///')

    info "\nComponents:"
    info "  Type: release"
    info "  Version: $VERSION"

    success "All validation checks passed!\n"
    exit 0

else
    error "Branch name does not follow standard conventions\n"

    info "Expected formats:"
    info "  Standard: {type}/{ISSUE-ID}-{description}"
    info "    Example: feature/ECM-123-user-authentication"
    info "\n  Release: release/v{MAJOR}.{MINOR}.{PATCH}"
    info "    Example: release/v1.2.0\n"

    info "Valid types:"
    info "  - feature    : New features"
    info "  - bugfix/fix : Bug fixes"
    info "  - hotfix     : Critical production fixes"
    info "  - refactor   : Code refactoring"
    info "  - docs       : Documentation changes"
    info "  - test       : Test additions/updates"
    info "  - chore      : Maintenance tasks"
    info "  - experiment : Experimental branches\n"

    info "Requirements:"
    info "  - Type must be lowercase"
    info "  - Issue ID must be uppercase with number (e.g., ECM-123)"
    info "  - Description must be kebab-case (lowercase with hyphens)"
    info "  - No special characters except hyphens in description"
    info "  - No consecutive hyphens\n"

    # Provide specific feedback
    if [[ ! "$BRANCH_NAME" =~ / ]]; then
        error "Branch name missing '/' separator"
    fi

    TYPE=$(echo "$BRANCH_NAME" | cut -d'/' -f1)
    if [[ ! "$TYPE" =~ ^(feature|bugfix|fix|hotfix|refactor|docs|test|chore|release|experiment)$ ]]; then
        error "Invalid branch type: '$TYPE'"
    fi

    SUFFIX=$(echo "$BRANCH_NAME" | cut -d'/' -f2)
    if [[ ! "$SUFFIX" =~ ^[A-Z]+-[0-9]+ ]]; then
        error "Missing or invalid issue ID (expected format: ECM-123)"
    fi

    if [[ "$SUFFIX" =~ [A-Z] ]] && [[ ! "$SUFFIX" =~ ^[A-Z]+-[0-9]+- ]]; then
        error "Description may contain uppercase letters (should be kebab-case)"
    fi

    if [[ "$SUFFIX" =~ _ ]]; then
        error "Description contains underscores (use hyphens instead)"
    fi

    exit 1
fi
