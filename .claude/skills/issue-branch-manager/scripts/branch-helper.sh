#!/bin/bash

# Branch Helper Script
# Provides common Git operations for issue-based branch management

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
error() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

success() {
    echo -e "${GREEN}$1${NC}"
}

warning() {
    echo -e "${YELLOW}Warning: $1${NC}"
}

info() {
    echo "$1"
}

# Check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        error "Not a git repository"
    fi
}

# Get current branch name
get_current_branch() {
    git branch --show-current
}

# Check if branch exists locally
branch_exists_local() {
    local branch=$1
    git show-ref --verify --quiet "refs/heads/$branch"
}

# Check if branch exists remotely
branch_exists_remote() {
    local branch=$1
    git ls-remote --heads origin "$branch" | grep -q "$branch"
}

# Validate branch name format (ecm-XXX)
validate_branch_name() {
    local branch=$1
    if [[ ! $branch =~ ^ecm-[0-9]+$ ]]; then
        error "Invalid branch name format. Expected: ecm-XXX (lowercase, numbers only)"
    fi
}

# Extract issue number from branch name
extract_issue_number() {
    local branch=$1
    echo "$branch" | grep -oP 'ecm-\K\d+'
}

# Check for uncommitted changes
check_uncommitted_changes() {
    if ! git diff-index --quiet HEAD --; then
        return 1  # Has uncommitted changes
    fi
    return 0  # No uncommitted changes
}

# Command: status
# Show current branch status and issue information
cmd_status() {
    check_git_repo

    local current_branch
    current_branch=$(get_current_branch)

    info "=== Branch Status ==="
    info "Current branch: $current_branch"

    # Check if it's an issue branch
    if [[ $current_branch =~ ^ecm-[0-9]+$ ]]; then
        local issue_num
        issue_num=$(extract_issue_number "$current_branch")
        info "Issue number: ECM-$issue_num"
    fi

    # Show git status
    info ""
    info "=== Working Tree Status ==="
    git status --short

    # Show commits ahead of master
    if [ "$current_branch" != "master" ]; then
        info ""
        info "=== Commits ahead of master ==="
        git log master..HEAD --oneline || warning "Unable to compare with master"
    fi
}

# Command: create
# Create a new issue branch from master
cmd_create() {
    check_git_repo

    if [ $# -lt 1 ]; then
        error "Usage: $0 create <issue-identifier>\nExample: $0 create ECM-105"
    fi

    local issue_id=$1
    local branch_name

    # Convert to lowercase and extract number
    issue_id=$(echo "$issue_id" | tr '[:upper:]' '[:lower:]')

    # Extract branch name (ecm-XXX)
    if [[ $issue_id =~ ^ecm-([0-9]+)$ ]]; then
        branch_name="ecm-${BASH_REMATCH[1]}"
    elif [[ $issue_id =~ ^([0-9]+)$ ]]; then
        branch_name="ecm-${BASH_REMATCH[1]}"
    else
        error "Invalid issue identifier. Expected: ECM-105 or 105"
    fi

    validate_branch_name "$branch_name"

    # Check if branch already exists
    if branch_exists_local "$branch_name"; then
        warning "Branch $branch_name already exists locally"
        read -p "Switch to existing branch? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git switch "$branch_name"
            success "Switched to existing branch: $branch_name"
        fi
        exit 0
    fi

    # Check for uncommitted changes
    if ! check_uncommitted_changes; then
        error "You have uncommitted changes. Please commit or stash them first."
    fi

    # Switch to master and pull latest
    info "Switching to master and pulling latest changes..."
    git checkout master || error "Failed to checkout master"
    git pull origin master || warning "Failed to pull from origin/master"

    # Create and switch to new branch
    info "Creating branch: $branch_name"
    git switch -c "$branch_name" || error "Failed to create branch"

    success "Created and switched to branch: $branch_name"
    info "You can now start working on issue ECM-$(extract_issue_number "$branch_name")"
}

# Command: publish
# Publish current branch to remote
cmd_publish() {
    check_git_repo

    local current_branch
    current_branch=$(get_current_branch)

    if [ "$current_branch" = "master" ]; then
        error "Cannot publish master branch with this command. Use 'git push' directly."
    fi

    # Check for uncommitted changes
    if ! check_uncommitted_changes; then
        warning "You have uncommitted changes"
        read -p "Commit them before publishing? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git add .
            read -p "Enter commit message: " commit_msg
            git commit -m "$commit_msg"
        else
            error "Please commit or stash changes before publishing"
        fi
    fi

    # Check if branch exists remotely
    if branch_exists_remote "$current_branch"; then
        info "Branch already exists remotely. Pushing updates..."
        git push || error "Failed to push to remote"
    else
        info "Publishing branch to remote..."
        git push -u origin "$current_branch" || error "Failed to publish branch"
    fi

    success "Branch published: $current_branch"
}

# Command: merge
# Merge current branch to master
cmd_merge() {
    check_git_repo

    local current_branch
    current_branch=$(get_current_branch)

    if [ "$current_branch" = "master" ]; then
        error "Already on master branch"
    fi

    # Validate it's an issue branch
    if [[ ! $current_branch =~ ^ecm-[0-9]+$ ]]; then
        warning "Current branch doesn't follow ecm-XXX naming convention"
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi

    # Check for uncommitted changes
    if ! check_uncommitted_changes; then
        error "You have uncommitted changes. Please commit or stash them first."
    fi

    info "Merging $current_branch to master..."

    # Save current branch name
    local feature_branch=$current_branch

    # Switch to master
    git checkout master || error "Failed to checkout master"

    # Pull latest changes
    info "Pulling latest changes from master..."
    git pull origin master || error "Failed to pull from origin/master"

    # Merge feature branch
    info "Merging $feature_branch..."
    if git merge "$feature_branch"; then
        success "Merge successful"

        # Ask to push
        read -p "Push merged changes to origin/master? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git push origin master || error "Failed to push to origin/master"
            success "Changes pushed to origin/master"
        fi
    else
        error "Merge failed. Please resolve conflicts and complete merge manually."
    fi
}

# Command: cleanup
# Delete feature branch (local and optionally remote)
cmd_cleanup() {
    check_git_repo

    local branch
    if [ $# -lt 1 ]; then
        # Use current branch if no argument provided
        branch=$(get_current_branch)
        if [ "$branch" = "master" ]; then
            error "Cannot cleanup master branch"
        fi
    else
        branch=$1
    fi

    # Validate branch name format
    if [[ ! $branch =~ ^ecm-[0-9]+$ ]]; then
        warning "Branch doesn't follow ecm-XXX naming convention"
        read -p "Continue cleanup anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi

    # Switch to master if currently on the branch to be deleted
    local current_branch
    current_branch=$(get_current_branch)
    if [ "$current_branch" = "$branch" ]; then
        info "Switching to master..."
        git checkout master || error "Failed to checkout master"
    fi

    # Delete local branch
    if branch_exists_local "$branch"; then
        info "Deleting local branch: $branch"
        git branch -d "$branch" 2>/dev/null || {
            warning "Branch not fully merged. Force delete?"
            read -p "Force delete local branch? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                git branch -D "$branch" || error "Failed to delete local branch"
            else
                exit 0
            fi
        }
        success "Local branch deleted: $branch"
    else
        warning "Local branch does not exist: $branch"
    fi

    # Delete remote branch
    if branch_exists_remote "$branch"; then
        read -p "Delete remote branch origin/$branch? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git push origin --delete "$branch" || error "Failed to delete remote branch"
            success "Remote branch deleted: $branch"
        fi
    fi

    success "Cleanup complete for branch: $branch"
}

# Command: help
# Show usage information
cmd_help() {
    cat << EOF
Branch Helper Script - Issue-based branch management

Usage: $0 <command> [arguments]

Commands:
    status              Show current branch status and issue info
    create <issue-id>   Create new issue branch from master
                        Example: $0 create ECM-105
    publish             Publish current branch to remote
    merge               Merge current branch to master
    cleanup [branch]    Delete branch (local and optionally remote)
                        Example: $0 cleanup ecm-105
    help                Show this help message

Branch Naming Convention:
    ecm-{number}        Example: ecm-105, ecm-208

Examples:
    $0 status
    $0 create ECM-105
    $0 publish
    $0 merge
    $0 cleanup ecm-105

For more information, see the skill documentation.
EOF
}

# Main command dispatcher
main() {
    if [ $# -lt 1 ]; then
        cmd_help
        exit 1
    fi

    local command=$1
    shift  # Remove command from arguments

    case $command in
        status)
            cmd_status "$@"
            ;;
        create)
            cmd_create "$@"
            ;;
        publish)
            cmd_publish "$@"
            ;;
        merge)
            cmd_merge "$@"
            ;;
        cleanup)
            cmd_cleanup "$@"
            ;;
        help|--help|-h)
            cmd_help
            ;;
        *)
            error "Unknown command: $command\nRun '$0 help' for usage information"
            ;;
    esac
}

# Run main function
main "$@"
