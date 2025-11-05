# Branch Workflow Guide

Comprehensive Git branching strategies and workflows for issue-based development.

## Branch Naming Convention

### Standard Format

```
ecm-{issue-number}
```

**Rules:**
- Always lowercase
- Use hyphen (-) as separator
- No other special characters
- Derived from Linear issue identifier

**Examples:**
- `ecm-105` - Feature branch for issue ECM-105
- `ecm-208` - Bug fix branch for issue ECM-208
- `ecm-1024` - Task branch for issue ECM-1024

**Invalid:**
- `ECM-105` - Uppercase not allowed
- `ecm_105` - Underscore not allowed
- `ecm/105` - Slash not allowed
- `feature/ecm-105` - No prefix needed

### Branch Lifecycle

```
master (main branch)
  ↓
  git switch -c ecm-105 (create feature branch)
  ↓
  [work commits]
  ↓
  git push -u origin ecm-105 (publish)
  ↓
  git merge ecm-105 (merge to master)
  ↓
  git branch -d ecm-105 (cleanup)
```

## Git Workflow Steps

### 1. Starting Work (Branch Creation)

**Pre-checks:**
```bash
# Check current status
git status

# Ensure you're on master
git branch --show-current

# Pull latest changes
git pull origin master
```

**Branch Creation:**
```bash
# Create and switch to feature branch
git switch -c ecm-105

# Verify branch created
git branch --show-current
# Output: ecm-105
```

**Handle Uncommitted Changes:**

**Option 1: Commit**
```bash
git add .
git commit -m "WIP: save current progress"
git switch master
git pull origin master
git switch -c ecm-105
```

**Option 2: Stash**
```bash
git stash push -m "Temporary work save"
git switch master
git pull origin master
git switch -c ecm-105
git stash pop
```

**Option 3: Discard (CAUTION)**
```bash
git checkout -- .
git switch master
git pull origin master
git switch -c ecm-105
```

### 2. Working on Issue (Commits)

**Commit Strategy:**
- Commit frequently
- Keep commits atomic (single logical change)
- Write descriptive commit messages
- Reference issue number

**Commit Message Format:**
```
<type>: <description> (<issue-ref>)

Types:
- feat: New feature
- fix: Bug fix
- refactor: Code refactoring
- test: Adding tests
- docs: Documentation
- chore: Maintenance
- perf: Performance improvement
- style: Code style changes
```

**Examples:**
```bash
git commit -m "feat: add user search API endpoint (ECM-105)"
git commit -m "fix: handle null values in search results (ECM-105)"
git commit -m "test: add search functionality unit tests (ECM-105)"
git commit -m "docs: update API documentation for search (ECM-105)"
```

**Commit Process:**
```bash
# Stage specific files
git add src/api/search.py
git add src/tests/test_search.py

# Commit with message
git commit -m "feat: implement search API (ECM-105)"

# Or stage all and commit
git add .
git commit -m "feat: complete search feature (ECM-105)"
```

### 3. Publishing Branch

**First Push:**
```bash
# Push and set upstream
git push -u origin ecm-105
```

**Subsequent Pushes:**
```bash
# Simple push
git push
```

**Handle Push Errors:**

**Remote branch exists:**
```bash
# Fetch to see remote state
git fetch origin

# Check if remote has different commits
git log ecm-105..origin/ecm-105

# If safe, force push (CAUTION)
git push --force-with-lease origin ecm-105
```

**Authentication failed:**
- Check Git credentials
- Verify repository access
- Re-authenticate if needed

**Network issues:**
- Check internet connection
- Try again after delay
- Check Git remote URL

### 4. Merging to Master

**Pre-merge Checks:**
```bash
# Run tests
npm run test  # or python -m pytest, etc.

# Run build
npm run build

# Check for uncommitted changes
git status

# View what will be merged
git diff master...ecm-105
```

**Merge Process:**
```bash
# Switch to master
git checkout master

# Pull latest changes
git pull origin master

# Merge feature branch
git merge ecm-105

# Push merged changes
git push origin master
```

**Merge Strategies:**

**Fast-Forward (preferred when possible):**
```bash
# Default merge with fast-forward
git merge ecm-105

# Result: Linear history
```

**No Fast-Forward (explicit merge commit):**
```bash
# Create merge commit even if fast-forward possible
git merge --no-ff ecm-105

# Result: Merge commit in history
# Benefit: Clear feature boundaries
```

**Rebase Before Merge:**
```bash
# Switch to feature branch
git checkout ecm-105

# Rebase on master
git rebase master

# Resolve conflicts if any

# Switch back to master
git checkout master

# Merge (will be fast-forward)
git merge ecm-105
```

### 5. Branch Cleanup

**Delete Local Branch:**
```bash
# Safe delete (only if merged)
git branch -d ecm-105

# Force delete (even if not merged)
git branch -D ecm-105
```

**Delete Remote Branch:**
```bash
# Delete from remote
git push origin --delete ecm-105

# Or alternative syntax
git push origin :ecm-105
```

**Verify Deletion:**
```bash
# List local branches
git branch

# List remote branches
git branch -r
```

## Conflict Resolution

### Identifying Conflicts

```bash
# After merge/rebase, Git will show:
CONFLICT (content): Merge conflict in src/api/search.py
Automatic merge failed; fix conflicts and then commit the result.
```

### Conflict Markers

```python
<<<<<<< HEAD
# Current branch version
def search(query):
    return database.search(query)
=======
# Incoming branch version
def search(query, filters=None):
    return database.search(query, filters)
>>>>>>> ecm-105
```

### Resolution Steps

1. **Open conflicting file**
2. **Choose resolution:**
   - Keep HEAD version (current branch)
   - Keep incoming version (feature branch)
   - Combine both versions
   - Write new solution

3. **Remove conflict markers:**
```python
# After resolution
def search(query, filters=None):
    if filters:
        return database.search(query, filters)
    return database.search(query)
```

4. **Mark as resolved:**
```bash
git add src/api/search.py
```

5. **Complete merge:**
```bash
# If merging
git commit

# If rebasing
git rebase --continue
```

### Conflict Resolution Tools

**View conflict status:**
```bash
# List conflicted files
git status

# Show conflicts
git diff
```

**Abort if needed:**
```bash
# Abort merge
git merge --abort

# Abort rebase
git rebase --abort
```

**Use merge tool:**
```bash
# Launch configured merge tool
git mergetool
```

## Advanced Workflows

### Multi-Issue Development

**Scenario:** Working on multiple issues simultaneously

**Workflow:**
```bash
# Working on ECM-105
git switch -c ecm-105
# ... make changes ...
git add .
git commit -m "WIP: partial implementation (ECM-105)"

# Need to switch to ECM-108
git switch -c ecm-108
# ... make changes ...
git commit -m "feat: implement feature (ECM-108)"

# Back to ECM-105
git switch ecm-105
# ... continue work ...
git commit -m "feat: complete implementation (ECM-105)"
```

**Tips:**
- Commit WIP before switching
- Use descriptive commit messages
- Keep branches focused on single issues
- Track which branch is which issue

### Dependent Issues

**Scenario:** ECM-108 depends on ECM-105

**Workflow:**
```bash
# Complete ECM-105 first
git switch ecm-105
# ... implement ...
git merge ecm-105 into master

# Then start ECM-108
git switch master
git pull origin master
git switch -c ecm-108
# ... implement ...
```

**Alternative (parallel development):**
```bash
# Start ECM-105
git switch -c ecm-105

# Create ECM-108 from ECM-105
git switch -c ecm-108

# Work on ECM-108 (includes ECM-105 changes)
# ... implement ...

# When merging:
# 1. Merge ECM-105 to master first
# 2. Rebase ECM-108 on master
# 3. Merge ECM-108 to master
```

### Long-Running Feature Branches

**Keep branch updated with master:**
```bash
# Regularly merge master into feature branch
git checkout ecm-105
git merge master

# Or rebase feature branch on master
git checkout ecm-105
git rebase master
```

**When to sync:**
- Daily for long-running branches
- Before major changes
- Before merging back to master

### Emergency Hotfix

**Scenario:** Critical bug needs immediate fix

**Workflow:**
```bash
# From master, create hotfix branch
git checkout master
git pull origin master
git switch -c ecm-999

# Implement fix
# ... changes ...
git commit -m "fix: critical bug (ECM-999)"

# Fast-track merge
git checkout master
git merge ecm-999
git push origin master

# Update any active feature branches
git checkout ecm-105
git merge master
```

## Best Practices

### Branch Management
1. Keep branches short-lived (days, not weeks)
2. Merge or delete stale branches
3. One issue per branch
4. Always start from updated master
5. Rebase to keep history clean
6. Delete after merge

### Commit Management
1. Commit frequently
2. Write clear messages
3. Include issue reference
4. Keep commits atomic
5. Test before committing
6. Don't commit secrets

### Merge Management
1. Test before merging
2. Review your own changes
3. Handle conflicts carefully
4. Don't force push to master
5. Push immediately after merge
6. Update Linear issue

### Safety Practices
1. Always pull before creating branch
2. Never force push to shared branches
3. Backup before dangerous operations
4. Use --force-with-lease instead of --force
5. Verify merges before pushing
6. Keep master stable

## Troubleshooting

### Branch Not Found
```bash
# List all branches
git branch -a

# Fetch from remote
git fetch origin

# Create from remote
git checkout -b ecm-105 origin/ecm-105
```

### Accidental Commit to Master
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Create proper branch
git switch -c ecm-105

# Commit again
git commit -m "feat: implement feature (ECM-105)"
```

### Lost Commits
```bash
# View reflog
git reflog

# Find lost commit
# Restore it
git checkout <commit-hash>
git switch -c ecm-105-recovered
```

### Merge Gone Wrong
```bash
# If not pushed yet
git reset --hard HEAD~1

# If pushed (CAUTION - coordinate with team)
git revert -m 1 <merge-commit-hash>
```

## Git Commands Reference

### Branch Operations
```bash
git branch                    # List local branches
git branch -r                 # List remote branches
git branch -a                 # List all branches
git switch -c <name>          # Create and switch to branch
git switch <name>             # Switch to existing branch
git branch -d <name>          # Delete local branch
git push origin --delete <name>  # Delete remote branch
```

### Viewing Changes
```bash
git status                    # Show working tree status
git diff                      # Show unstaged changes
git diff --staged             # Show staged changes
git diff master...ecm-105     # Compare branches
git log                       # Show commit history
git log master..HEAD          # Commits ahead of master
```

### Undoing Changes
```bash
git checkout -- <file>        # Discard changes to file
git reset HEAD <file>         # Unstage file
git reset --soft HEAD~1       # Undo last commit, keep changes
git reset --hard HEAD~1       # Undo last commit, discard changes
git revert <commit>           # Create new commit undoing changes
```

### Stashing
```bash
git stash push -m "message"   # Stash changes with message
git stash list                # List all stashes
git stash pop                 # Apply and remove latest stash
git stash apply               # Apply latest stash, keep in list
git stash drop                # Remove latest stash
```
