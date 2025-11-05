# Git 빠른 참조

소규모 팀 Git 워크플로우 필수 명령어.

## 기본 워크플로우

### Branch 생성

```bash
# 최신 상태 확인
git checkout master
git pull origin master

# 새 branch
git checkout -b feature/ECM-123-description
```

### Commit

```bash
git add .
git commit -m "feat(scope): description"
```

**Conventional Commits**:
- `feat`: 새 기능
- `fix`: 버그 수정
- `docs`: 문서
- `refactor`: 리팩토링
- `chore`: 기타

### Push

```bash
# 첫 push
git push -u origin feature/ECM-123-description

# 이후
git push
```

### PR & Merge

```bash
# PR 생성
gh pr create --title "..." --body "..."

# Merge (no-rebase)
gh pr merge --merge --delete-branch
```

### Cleanup

```bash
git checkout master
git pull origin master
git branch -d feature/ECM-123-description
git fetch --prune origin
```

## 자주 쓰는 명령어

### 상태 확인

```bash
git status              # 현재 상태
git log --oneline       # Commit 히스토리
git diff                # 변경 사항
git branch              # Branch 목록
```

### Sync

```bash
git fetch origin        # 최신 정보 가져오기
git pull origin master  # Pull & merge
git merge origin/master # Master 변경사항 merge (이력 보존)
```

### Stash

```bash
git stash save "WIP"    # 임시 저장
git stash pop           # 복원
git stash list          # 목록
```

### Undo

```bash
git reset --soft HEAD~1 # Commit 취소 (변경 유지)
git reset --hard HEAD~1 # Commit 취소 (변경 삭제)
git checkout -- file    # 파일 변경 취소
```

## Conflict 해결

```bash
# Merge conflict
git status              # 충돌 파일 확인
# ... 파일 수정 ...
git add <resolved-files>
git commit -m "Merge master into feature branch"

# Merge 중단 (취소)
git merge --abort
```

## Branch 전략

**소규모 팀 - GitHub Flow**:
```
master (production)
  ├── feature/ECM-123-feature
  ├── bugfix/ECM-124-fix
  └── hotfix/ECM-125-hotfix
```

**규칙**:
- `master`에서 branch
- `master`로 merge
- Merge 후 즉시 deploy 가능

## Merge 전략

**기본 - Merge Commit** (`--merge`):
```bash
gh pr merge --merge
```
- History 보존
- Revert 용이

**대안 - Squash** (`--squash`):
```bash
gh pr merge --squash
```
- Clean history
- 작은 기능용

## Git 설정

```bash
# User 설정
git config --global user.name "Name"
git config --global user.email "email@example.com"

# Default branch
git config --global init.defaultBranch master

# Editor
git config --global core.editor "code --wait"
```

## Troubleshooting

**Push rejected**:
```bash
git fetch origin
git merge origin/master
git push
```

**Branch 삭제 안됨**:
```bash
git branch -D branch-name  # Force delete
```

**Commit 수정**:
```bash
git commit --amend --no-edit  # 마지막 commit 수정
```
