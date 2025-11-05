---
name: issue-workflow-manager
description: Linear 이슈 전체 생명주기 관리 스킬. 이슈 생성, 작업 시작(브랜치 생성), 작업 완료(PR/merge) 시 사용. 소규모 팀(1-4인)에 최적화됨.
---

# Issue Workflow Manager

Linear 이슈 기반 개발 워크플로우 관리.

## 워크플로우 선택

**이슈 생성?**
→ `templates/issues/{type}.md` 로드
- `feature.md`: 새 기능
- `bug.md`: 버그 수정
- `task.md`: 작업/개선

**작업 시작?**
→ `templates/start-work.md` 로드

**작업 완료?**
→ `templates/complete-work.md` 로드

**참고 필요?**
→ `references/` 디렉토리 확인

## 핵심 원칙

### 컨텍스트 효율성
- 필요한 template만 로드
- 단계별 점진적 로딩
- 간결한 체크리스트 중심

### 명명 규칙
**Branch**: `{type}/{ISSUE-ID}-{description}`
```
feature/ECM-123-user-auth
bugfix/ECM-124-null-fix
```

**Commit**: Conventional Commits
```
feat(auth): add JWT validation
fix(api): resolve null pointer
```

### Linear 포맷팅
- ❌ 이모지 사용 금지 (title, description, comment 모두)
- ✅ Plain text + markdown만 사용
- ✅ 기술적이고 전문적인 톤

### Git Workflow
- Base: `master`/`main`
- Merge: `--merge` (no-rebase)
- Cleanup: local/remote branch 삭제

## 빠른 참조

### Linear MCP
```bash
# Team 조회
linear_get_teams

# Issue 생성
linear_create_issue --title "..." --description "..." --teamId "..."

# Issue 조회
linear_get_issue --identifier "ECM-123"

# Issue 수정
linear_edit_issue --issueId "uuid" --stateId "state-uuid"
```

### Git
```bash
# Branch 생성
git checkout -b feature/ECM-123-description

# Push
git push -u origin feature/ECM-123-description

# PR 생성
gh pr create --title "..." --body "..."

# Merge
gh pr merge --merge --delete-branch
```

## Resources

### templates/issues/
이슈 타입별 생성 template (필요한 것만 로드):
- `feature.md`: 신규 기능 개발
- `bug.md`: 버그 수정
- `task.md`: 작업/개선/문서화

### templates/
워크플로우 template:
- `start-work.md`: 작업 시작 절차
- `complete-work.md`: PR 생성 및 완료

### references/
상세 참고 문서 (필요시 로드):
- `linear-quick.md`: Linear MCP 빠른 참조
- `git-quick.md`: Git 빠른 참조
- `naming.md`: 명명 규칙

## 예시 플로우

### Feature 개발
```
1. "ECM-123 feature 이슈 생성해줘"
   → templates/issues/feature.md 로드
   → Linear 이슈 생성

2. "ECM-123 작업 시작할게"
   → templates/start-work.md 로드
   → feature/ECM-123-description branch 생성

3. [개발 진행...]

4. "ECM-123 완료했어"
   → templates/complete-work.md 로드
   → PR 생성, merge, cleanup
```

### Bug 수정
```
1. "ECM-124 버그 이슈 생성"
   → templates/issues/bug.md 로드

2. "ECM-124 시작"
   → bugfix/ECM-124-fix branch

3. "ECM-124 완료"
   → PR merge, cleanup
```

## 소규모 팀 최적화

### 간소화된 프로세스
- Review 없이 self-merge 가능
- CI/CD 선택적
- 빠른 iteration

### 필수 단계만
- Clean working tree 확인
- Branch 명명 규칙 준수
- PR 생성 (기록용)
- Branch cleanup

### 생략 가능
- Formal review process
- Multiple approvers
- Complex CI/CD
- Milestone 관리

## Troubleshooting

**Linear 인증 오류**
```bash
echo $LINEAR_ACCESS_TOKEN  # 확인
```

**Branch 이미 존재**
```bash
git branch -D old-branch  # 삭제 후 재생성
```

**PR 생성 실패**
```bash
gh auth status  # GitHub CLI 인증 확인
```

**Merge conflict**
```bash
git fetch origin
git merge origin/master
# Conflict 해결 후
git add <resolved-files>
git commit -m "Merge master into feature branch"
git push
```
