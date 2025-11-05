# Complete Work Template

PR 생성, merge, cleanup 완료.

## 체크리스트

- [ ] Commit 확인
- [ ] Tests/Lint 통과
- [ ] Branch push
- [ ] PR 생성
- [ ] Merge
- [ ] Cleanup
- [ ] (선택) Linear 상태 업데이트

## 프로세스

### 1. 완료 검증

```bash
# Commit 확인
git log --oneline master..HEAD

# 변경 파일 확인
git diff --name-status master...HEAD

# Lint/Test (프로젝트에 따라)
npm run lint && npm run check
```

### 2. Base Branch 동기화

```bash
# 최신 master 가져오기
git fetch origin

# Merge (이력 보존)
git merge origin/master

# Conflict 해결 필요시
git status  # 충돌 파일 확인
# ... 파일 수정 ...
git add <resolved-files>
git commit -m "Merge master into feature branch"
```

### 3. Push

```bash
# Push (첫 push 또는 merge 후)
git push -u origin feature/ECM-123-description

# 이미 tracking 설정된 경우
git push
```

### 4. PR 생성

```bash
gh pr create \
  --title "PR 제목" \
  --body "$(cat <<'EOF'
# 개요
변경 사항 요약

## Related Issue
Closes ECM-XXX

## 주요 변경
- 변경 1
- 변경 2

## 테스트
- [ ] 로컬 테스트 완료
- [ ] Lint 통과
EOF
)"
```

**PR Title**: Issue title과 동일하게 (NO 이모지)

**PR Body 최소 구조**:
```markdown
# 개요
[요약]

## Related Issue
Closes ECM-XXX

## 주요 변경
- 변경 내용
```

### 5. Merge

**소규모 팀 - Self Merge**:
```bash
# CI 체크 확인 (있는 경우)
gh pr checks

# Merge (no-rebase)
gh pr merge --merge --delete-branch
```

**Review 필요한 경우**:
```bash
# Review 대기
gh pr view

# Approve 후 merge
gh pr merge --merge --delete-branch
```

### 6. Local Cleanup

```bash
# Master로 전환
git checkout master

# 최신 상태 동기화
git pull origin master

# Local branch 삭제
git branch -d feature/ECM-123-description

# Remote tracking 정리
git fetch --prune origin
```

### 7. (선택) Linear 상태 업데이트

```bash
# Issue UUID 가져오기
ISSUE=$(linear_get_issue --identifier "ECM-XXX")
ISSUE_UUID=$(echo $ISSUE | jq -r '.issue.id')

# Done state 찾기
TEAMS=$(linear_get_teams)
DONE_STATE=$(echo $TEAMS | jq -r '.teams[].states[] | select(.name=="Done") | .id')

# 상태 업데이트
linear_edit_issue \
  --issueId "$ISSUE_UUID" \
  --stateId "$DONE_STATE"

# (선택) Comment 추가
linear_create_comment \
  --issueId "$ISSUE_UUID" \
  --body "Completed in PR #XX"
```

### 8. 최종 확인

```bash
git status
# 출력: On branch master, clean working tree

git branch
# feature branch 없어야 함
```

## 예시 플로우

```
User: "ECM-109 완료"

1. 검증
   git log --oneline master..HEAD
   → 5 commits

   npm run lint && npm run check
   → Pass

2. 동기화
   git fetch origin
   git merge origin/master
   → Success (no conflict)

3. Push
   git push -u origin feature/ECM-109-workflow-visualization

4. PR 생성
   gh pr create \
     --title "Implement workflow visualization component" \
     --body "..."
   → PR #42 created

5. Merge
   gh pr merge 42 --merge --delete-branch
   → Merged, remote branch deleted

6. Cleanup
   git checkout master
   git pull origin master
   git branch -d feature/ECM-109-workflow-visualization

7. Linear 업데이트 (선택)
   linear_edit_issue → Done 상태로

완료!
```

## 소규모 팀 단순화

**생략 가능**:
- Review process (self-merge)
- CI/CD checks (선택적)
- Milestone 관리
- 복잡한 테스트

**필수만**:
- Clean commits
- PR 생성 (기록용)
- Merge
- Branch cleanup

## Common Issues

**Push rejected**:
```bash
git fetch origin
git merge origin/master  # 최신 master merge
git push
```

**PR 생성 실패**:
```bash
gh auth status  # 인증 확인
gh auth login   # 재인증
```

**Merge conflict**:
```bash
git fetch origin
git merge origin/master
# 충돌 해결
git add <resolved-files>
git commit -m "Merge master into feature branch"
git push
```

**Branch 삭제 실패**:
```bash
# Force delete
git branch -D feature/ECM-123-description
```

## Merge 전략

**기본**: `--merge` (no-rebase)
- History 보존
- Feature tracking 명확
- Revert 용이

**대안**: `--squash` (선택적)
```bash
gh pr merge --squash --delete-branch
```
- 단일 commit으로 통합
- Clean history
- 작은 기능에 적합
