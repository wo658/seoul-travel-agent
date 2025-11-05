---
name: issue-branch-manager
description: Manages the complete lifecycle of Linear issues through Git branch workflows. Automatically creates feature branches from issue identifiers, executes issue requirements, and handles branch publishing, merging, and issue completion reporting. Use this skill when users want to start work on a Linear issue, complete work on an issue, or manage the Git workflow for issue-based development.
---

# Issue Branch Manager

## Overview

Complete issue lifecycle management through Git branch workflows. Automatically handles branch creation from Linear issues, work execution, branch publishing, develop merging, and issue completion documentation.

## Core Capabilities

### 1. Issue Start Workflow

Automatically initiates work on a Linear issue with proper branch management.

**Trigger Patterns:**
- "BLOG-15 이슈 시작해줘"
- "Start working on BLOG-18"
- "Begin issue BLOG-23"
- "작업 시작: BLOG-15"

**Workflow Steps:**

#### Step 1: Validate Current State
Check for uncommitted changes and current branch:

```bash
# Check git status
git status

# If uncommitted changes exist, prompt user:
# "커밋되지 않은 변경사항이 있습니다. 선택하세요:"
# 1. 지금 commit하기
# 2. Stash하기
# 3. 변경사항 버리기
# 4. 작업 취소
```

#### Step 2: Fetch Linear Issue Details
Use Linear MCP to retrieve issue information:

```javascript
// Get issue by identifier
const issue = await linear_get_issue({ identifier: "BLOG-15" });

// Extract key information:
// - issue.title
// - issue.description
// - issue.priority
// - issue.labels
// - issue.state
// - issue.assignee
```

#### Step 3: Create Feature Branch
Create branch following naming convention `{type}/BLOG-{N}-{description}`:

```bash
# Ensure on develop and up to date
git checkout develop
git pull origin develop

# Create and switch to feature branch
# Extract type from issue label (Feature/Bug/Improvement/Chore)
git switch -c feature/BLOG-15-bookmark-feature
```

**Branch Naming Rules:**
- Type prefix based on label: `feature/`, `fix/`, `improve/`, `chore/`
- Issue number in uppercase: `BLOG-15` not `blog-15`
- Kebab-case description: `bookmark-feature`
- Format: `{type}/BLOG-{N}-{description}`

#### Step 4: Display Issue Context
Present issue details to understand requirements:

```markdown
## Issue: BLOG-15

**Title:** [issue.title]

**Priority:** [priority level]

**Description:**
[Full issue description with all sections]

**Labels:** [Feature/Bug/Improvement/Chore]

**Project:** [Frontend/Backend/Infrastructure]

**Current State:** [state name]
```

#### Step 5: Analyze and Execute
Analyze issue requirements and execute work:

1. **Parse Issue Type:**
   - Bug → Focus on reproduction, fix, testing
   - Feature → Implement functionality, add tests, update docs
   - Task → Complete checklist items, verify completion
   - Improvement → Measure baseline, implement, measure improvement

2. **Extract Requirements:**
   - Read acceptance criteria
   - Identify affected files/components
   - Note testing requirements
   - Check for dependencies

3. **Execute Work:**
   - Follow issue requirements systematically
   - Commit work incrementally with descriptive messages
   - Run tests to verify functionality
   - Update documentation as needed

4. **Track Progress:**
   - Use TodoWrite to track implementation steps
   - Mark items complete as work progresses
   - Update user on status

**Commit Message Format:**
```bash
# Conventional Commits 형식 준수 (기술 용어는 영어, 설명은 한글)
# type: 간단한 설명 (이슈번호)

git commit -m "feat: 북마크 기능 구현 (BLOG-15)"
git commit -m "fix: 한국어 검색 버그 수정 (BLOG-16)"
git commit -m "improve: 블로그 카드 렌더링 최적화 (BLOG-17)"
git commit -m "chore: TypeScript 5.3 업데이트 (BLOG-18)"
git commit -m "docs: 배포 가이드 업데이트 (BLOG-19)"

# 영어로 작성해도 무방한 경우 (기술 표준 용어 중심)
git commit -m "feat: add bookmark feature to blog cards (BLOG-15)"
git commit -m "fix: resolve Korean search filtering issue (BLOG-16)"
```

Reference `references/issue-execution.md` for detailed execution patterns by issue type.

### 2. Issue Completion Workflow

Handles branch publishing, merging, and issue completion documentation.

**Trigger Patterns:**
- "작업 완료했어"
- "Complete this issue"
- "Finish BLOG-15"
- "이슈 완료 처리해줘"
- "Ready to merge"

**Workflow Steps:**

#### Step 1: Verify Work Completion
Check that all requirements are met:

```bash
# Run tests
npm run test  # or appropriate test command

# Check build
npm run build  # or appropriate build command

# Verify no uncommitted changes
git status
```

**Validation Checklist:**
- [ ] All tests passing
- [ ] Build successful
- [ ] No uncommitted changes
- [ ] Code reviewed (self-review)
- [ ] Documentation updated
- [ ] Acceptance criteria met

#### Step 2: Prepare Completion Summary
Analyze commits and changes to create summary:

```bash
# Get commit history for this branch
git log develop..HEAD --oneline

# Get file changes
git diff develop...HEAD --stat

# Get detailed changes
git diff develop...HEAD
```

**Summary 생성 가이드:**
- **무엇을 변경했는가**: 수정된 파일, component, module
- **어떻게 구현했는가**: 기술적 approach, 주요 설계 결정사항
- **왜 이렇게 변경했는가**: 해결한 문제, 충족한 요구사항
- **테스트 수행 내역**: Unit/Integration/E2E test 결과
- **Breaking Changes**: migration 필요 여부 및 가이드

#### Step 3: Publish Branch
Push branch to remote repository:

```bash
# Push feature branch to remote
git push -u origin feature/BLOG-15-bookmark-feature
```

**Handle Push Errors:**
- Branch already exists → Verify it's the correct branch
- No upstream → Use `-u` flag as shown above
- Push rejected → Pull and merge if needed (never rebase)

#### Step 4: Create Pull Request
Create PR to merge feature branch into develop/master:

```bash
# Create PR using GitHub CLI
gh pr create --title "[Issue Title]" --body "[PR Description]" --base develop
```

**PR Description Format:**
```markdown
## Summary
[Brief description of changes]

## Changes
- [Change 1]
- [Change 2]

## Testing
- [Test 1]
- [Test 2]

## Related Issue
Closes BLOG-15
```

**CRITICAL - PR Guidelines:**
- **NO EMOJIS**: Never use emojis in PR title or description
- **NO ATTRIBUTION**: Do not include "Generated with Claude Code" or similar text
- **PROFESSIONAL TONE**: Use plain, professional language
- **NO REBASE**: Never use git rebase - always use merge workflow

#### Step 5: Merge Pull Request
Merge PR and clean up branches:

```bash
# Merge PR using GitHub CLI (squash merge recommended)
gh pr merge [PR_NUMBER] --squash --delete-branch

# Switch to develop/master
git checkout develop  # or master

# Pull merged changes
git pull origin develop

# Delete local feature branch
git branch -d feature/BLOG-15-bookmark-feature
```

**Merge Strategy:**
- Use squash merge for clean history
- Never use rebase (prohibited)
- Delete remote branch after merge
- Delete local branch after sync

**Merge Conflict Handling:**
If conflicts occur:
1. Show conflicting files
2. Ask user to resolve conflicts manually
3. After resolution, verify and commit
4. Continue merge process
5. Never suggest rebase as solution

#### Step 6: Update Linear Issue
Add completion comment to Linear issue:

```javascript
// 완료 보고서 작성 (한글 기반, 기술 용어는 영어 유지)
const completionReport = `
## 작업 완료 내역

### 변경 사항
[수정된 파일 및 component 요약]

### 구현 방식
[이슈 해결 approach 및 주요 기술 결정사항]

### 테스트
[수행한 테스트 및 결과]
- Unit test: [결과]
- Integration test: [결과]
- E2E test: [결과]

### Commit 이력
[Commit 메시지 목록]

### 수정된 파일
[변경된 파일 목록 및 변경 내용]

### Breaking Changes
[있는 경우 migration 가이드 포함]
`;

// Linear issue에 comment 추가
await linear_create_comment({
  issueId: issue.id,
  body: completionReport
});

// 선택적으로 issue 상태를 "Done"으로 업데이트
await linear_edit_issue({
  issueId: issue.id,
  stateId: doneState.id
});
```

**Note:** Branch cleanup is handled automatically in Step 5 (gh pr merge --delete-branch and local branch deletion). No separate cleanup step needed.

Reference `references/branch-workflow.md` for detailed branching strategies and best practices.

### 3. Branch Status Check

Quick status check for current work:

**Trigger Patterns:**
- "지금 어떤 이슈 작업 중이야?"
- "현재 branch 상태 보여줘"
- "작업 진행상황 확인"
- "What issue am I working on?"
- "Current branch status"
- "Show my progress"

**제공 정보:**
- 현재 branch 이름 및 연결된 issue
- Commit되지 않은 변경사항
- Develop보다 앞선 commit 수
- Issue 완료 상태

```bash
# Get current branch
BRANCH=$(git branch --show-current)

# Get issue number from branch name (e.g., feature/BLOG-15-bookmark → BLOG-15)
ISSUE_NUM=$(echo $BRANCH | grep -oP 'BLOG-\d+')

# Show status
git status
git log develop..HEAD --oneline
```

## Advanced Features

### Multi-Issue Workflow

When working on multiple related issues:

1. **Switch Between Issues:**
   ```bash
   # Save current work
   git add .
   git commit -m "WIP: progress on BLOG-15"

   # Switch to other issue branch
   git switch feature/BLOG-18-other-feature
   ```

2. **Track Dependencies:**
   - Link issues in Linear using "blocked by" relationships
   - Complete dependencies before dependent issues

3. **Coordinate Merges:**
   - Merge dependencies first
   - Merge (not rebase) dependent branches to incorporate changes

### Branch Recovery

If branch creation or merge fails:

1. **Uncommitted Changes Recovery:**
   ```bash
   # Stash changes
   git stash push -m "Work on BLOG-15"

   # Later restore
   git stash pop
   ```

2. **Failed Merge Recovery:**
   ```bash
   # Abort merge
   git merge --abort

   # Reset to previous state
   git reset --hard HEAD
   ```

3. **Lost Commits Recovery:**
   ```bash
   # Find lost commits
   git reflog

   # Restore from reflog
   git checkout <commit-hash>
   ```

## Error Handling

### Common Errors and Solutions

**Error: Branch already exists**
```bash
# Check if branch exists locally
git branch -l feature/BLOG-15-bookmark-feature

# If exists, switch to it instead
git switch feature/BLOG-15-bookmark-feature

# Or delete and recreate
git branch -D feature/BLOG-15-bookmark-feature
git switch -c feature/BLOG-15-bookmark-feature
```

**Error: Uncommitted changes prevent branch switch**
```bash
# Option 1: Commit changes
git add .
git commit -m "WIP: current progress"

# Option 2: Stash changes
git stash push -m "Temporary save"

# Option 3: Discard changes (CAUTION)
git checkout -- .
```

**Error: Linear issue not found**
- Verify issue identifier is correct (e.g., BLOG-15 not blog-15)
- Check Linear access token is valid
- Ensure issue exists in the tech-blog team workspace

**Error: Merge conflicts**
1. Show conflicting files
2. Guide user through conflict resolution
3. Verify resolution with `git diff`
4. Complete merge with `git commit`

**Error: Push rejected (non-fast-forward)**
```bash
# Pull and rebase
git pull --rebase origin develop

# Resolve conflicts if any
# Then push
git push origin develop
```

## Helper Script Usage

The skill includes a helper script for common operations:

```bash
# Check branch status
./scripts/branch-helper.sh status

# Create issue branch
./scripts/branch-helper.sh create BLOG-15

# Publish branch
./scripts/branch-helper.sh publish

# Merge to develop
./scripts/branch-helper.sh merge

# Cleanup branch
./scripts/branch-helper.sh cleanup feature/BLOG-15-bookmark-feature
```

Reference the script at [scripts/branch-helper.sh](scripts/branch-helper.sh) for implementation details.

## Resources

### references/branch-workflow.md
Comprehensive Git branching strategies, best practices, merge strategies, and conflict resolution patterns.

### references/issue-execution.md
Issue type-specific execution patterns, requirement parsing, implementation strategies, and testing approaches.

### scripts/branch-helper.sh
Bash script providing common Git operations for branch management, validation, and safety checks.

## Best Practices

### Branch Management
1. **Always start from develop/master** - Ensure clean starting point
2. **Pull before branch creation** - Get latest changes
3. **Use consistent naming** - Follow `{type}/BLOG-{N}-{description}` pattern
4. **Commit frequently** - Small, atomic commits
5. **Descriptive commit messages** - Include issue reference
6. **Test before merging** - Verify functionality
7. **Keep branches short-lived** - Merge within days, not weeks
8. **Create PR for review** - Use gh pr create
9. **Merge PR to complete** - Use gh pr merge --squash --delete-branch
10. **Clean up local branch** - Delete after pulling merged changes
11. **Never use rebase** - Always use merge workflow
12. **No emojis in PRs** - Professional language only

### Issue Execution
1. **Read full issue first** - Understand complete requirements
2. **Check acceptance criteria** - Know what "done" means
3. **Ask clarifying questions** - When requirements unclear
4. **Follow issue type patterns** - Bug vs Feature vs Task approaches
5. **Update progress** - Keep issue comments current
6. **Document decisions** - Explain non-obvious choices
7. **Test thoroughly** - Cover edge cases
8. **Update docs** - Keep documentation in sync

### Merge Safety
1. **Always pull develop first** - Avoid conflicts
2. **Run tests before merge** - Catch issues early
3. **Review changes** - Self-review before merge
4. **Handle conflicts carefully** - Understand both sides
5. **Verify after merge** - Test merged result
6. **Push immediately** - Share changes with team
7. **Update Linear** - Keep issue tracking current

## Workflow Examples

### Example 1: Simple Bug Fix

```
User: "Start BLOG-16"

Agent:
1. Checks git status (clean)
2. Fetches issue BLOG-16 from Linear
3. Displays issue: "한국어 검색 필터링 미동작"
4. Creates branch: git switch -c fix/BLOG-16-korean-search
5. Analyzes requirements and implements fix
6. Commits: "fix: 한국어 검색 버그 수정 (BLOG-16)"
7. Tests functionality

User: "작업 완료했어"

Agent:
1. Runs tests (passing)
2. Generates completion summary
3. Publishes: git push -u origin fix/BLOG-16-korean-search
4. Merges to develop
5. Updates Linear with completion report
6. Asks about branch cleanup
```

### Example 2: Feature Implementation

```
User: "Begin issue BLOG-15"

Agent:
1. Saves current work (if any)
2. Fetches issue BLOG-15: "블로그 포스트 북마크 기능 추가"
3. Creates branch: git switch -c feature/BLOG-15-bookmark-feature
4. Breaks down feature requirements
5. Implements incrementally with commits:
   - "feat: useBookmarks hook 추가 (BLOG-15)"
   - "feat: BlogCard에 북마크 버튼 UI 추가 (BLOG-15)"
   - "feat: FilterPanel에 북마크 필터 옵션 추가 (BLOG-15)"
   - "test: useBookmarks hook 테스트 추가 (BLOG-15)"

User: "Complete this issue"

Agent:
1. Verifies all acceptance criteria met
2. Runs full test suite
3. Creates detailed completion summary
4. Publishes and merges
5. Updates Linear with implementation details
```

### Example 3: Chore Completion

```
User: "작업 시작: BLOG-18"

Agent:
1. Fetches chore: "TypeScript 5.3 업데이트"
2. Creates branch: git switch -c chore/BLOG-18-ts-update
3. Works through checklist:
   - Update TypeScript to 5.3
   - Update type definitions
   - Fix type errors
   - Test build
   - Update documentation
4. Commits for each checklist item

User: "Ready to merge"

Agent:
1. Verifies all checklist items complete
2. Runs build and type checks
3. Prepares upgrade summary
4. Publishes and merges
5. Documents upgrade steps in Linear
```

## Integration with Other Skills

### With linear-issue-composer
- Use linear-issue-composer to create issues
- Use issue-branch-manager to execute and complete them
- Seamless workflow from creation to completion

### With Git Workflows
- Follows Git Flow principles
- Compatible with team branching strategies
- Maintains clean commit history

### With CI/CD
- Ensures tests pass before merge
- Triggers deployment pipelines
- Maintains build status
