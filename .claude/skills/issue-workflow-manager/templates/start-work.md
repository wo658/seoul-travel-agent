# Start Work Template

Linear 이슈 작업 시작 및 branch 생성.

## 체크리스트

- [ ] Issue identifier 확인 (ECM-XXX)
- [ ] Working tree clean 확인
- [ ] Branch 생성
- [ ] (선택) Linear 상태 업데이트

## 프로세스

### 1. Issue 조회

```bash
linear_get_issue --identifier "ECM-XXX"
```

**확인 사항**:
- Title (branch 이름용)
- Description (요구사항 확인)
- Acceptance criteria

### 2. Git 상태 확인

```bash
git status
```

**필수 조건**:
- Clean working tree
- `master`/`main` branch
- 최신 상태 (git pull)

**문제 있으면**:
```bash
# Uncommitted changes
git stash save "WIP"

# Wrong branch
git checkout master

# Not updated
git pull origin master
```

### 3. Branch 생성

**명명 규칙**: `{type}/{ISSUE-ID}-{description}`

**Type 선택**:
- `feature/`: 새 기능
- `bugfix/`: 버그 수정
- `hotfix/`: 긴급 수정
- `refactor/`: 리팩토링
- `docs/`: 문서
- `chore/`: 기타 작업

**Description 생성**:
1. Title에서 핵심 단어 3-5개 추출
2. kebab-case로 변환
3. 일반 단어 제거 (implement, add, fix 등)

**예시**:
```
ECM-123: "Implement user authentication system"
→ feature/ECM-123-user-authentication

ECM-124: "Fix null pointer in data processor"
→ bugfix/ECM-124-null-pointer

ECM-125: "Update API documentation"
→ docs/ECM-125-api-docs
```

**생성**:
```bash
git checkout -b feature/ECM-123-description
```

### 4. (선택) Linear 상태 업데이트

소규모 팀은 보통 생략 가능. 필요하면:

```bash
# Issue UUID 추출
ISSUE_UUID="<linear_get_issue에서 받은 id>"

# Team states 조회
linear_get_teams  # "In Progress" state 찾기

# 상태 업데이트
linear_edit_issue \
  --issueId "$ISSUE_UUID" \
  --stateId "in-progress-state-uuid"
```

### 5. 확인

```bash
git branch --show-current
# 출력: feature/ECM-123-description
```

**사용자에게 반환**:
```
Branch 생성 완료: feature/ECM-123-description
Issue: ECM-123 - [제목]
작업 시작 가능!
```

## 예시 플로우

```
User: "ECM-109 작업 시작"

1. linear_get_issue --identifier "ECM-109"
   ID: 1c7cbe11-...
   Title: "워크플로우 JSON 시각화 컴포넌트 구현"

2. git status
   → clean, on master

3. Branch 생성
   Type: feature
   ID: ECM-109
   Description: workflow-visualization
   → feature/ECM-109-workflow-visualization

4. git checkout -b feature/ECM-109-workflow-visualization
   Switched to a new branch

확인:
Branch: feature/ECM-109-workflow-visualization
Issue: ECM-109
Ready!
```

## Validation

**Branch 이름 검증** (선택):
```bash
./scripts/validate-branch.sh feature/ECM-109-workflow-visualization
```

## Common Issues

**Branch 이미 존재**:
```bash
git branch -D feature/ECM-109-workflow-visualization
git checkout -b feature/ECM-109-workflow-visualization
```

**Uncommitted changes**:
```bash
git add .
git commit -m "WIP: save current work"
# 또는
git stash
```

**Not on master**:
```bash
git checkout master
git pull origin master
```
