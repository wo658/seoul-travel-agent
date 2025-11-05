# Linear MCP 빠른 참조

소규모 팀을 위한 필수 Linear MCP 함수만 정리.

## 인증

```bash
echo $LINEAR_ACCESS_TOKEN  # 확인
```

## 주요 함수

### linear_get_teams

```bash
linear_get_teams
```

**필요한 정보**:
- `teams[].id`: Team UUID
- `teams[].states[]`: State 목록 ("Backlog", "In Progress", "Done")
- `teams[].labels[]`: Label 목록 ("Feature", "Bug", "Task")

### linear_create_issue

```bash
linear_create_issue \
  --title "제목" \
  --description "설명" \
  --teamId "team-uuid" \
  --priority 2 \
  --labelIds ["label-uuid"]
```

**필수**:
- `title`: NO 이모지
- `description`: Markdown, NO 이모지
- `teamId`: Team UUID

**선택**:
- `priority`: 0-4 (1=Urgent, 2=High, 3=Normal, 4=Low)
- `labelIds`: Label UUID 배열

**반환**:
- `issue.identifier`: ECM-XXX
- `issue.url`: Linear URL

### linear_get_issue

```bash
linear_get_issue --identifier "ECM-123"
```

**반환**:
- `issue.id`: Issue UUID (edit용)
- `issue.title`: 제목
- `issue.description`: 설명
- `issue.state`: 현재 상태

### linear_edit_issue

```bash
linear_edit_issue \
  --issueId "issue-uuid" \
  --stateId "state-uuid"
```

**주의**: Issue identifier (ECM-XXX) 아닌 UUID 필요

## 일반 패턴

### Issue 생성

```bash
# 1. Team/Label 조회
TEAMS=$(linear_get_teams)

# 2. ID 추출
TEAM_ID=$(echo $TEAMS | jq -r '.teams[] | select(.name=="ECM-newtech") | .id')
LABEL_ID=$(echo $TEAMS | jq -r '.teams[].labels[] | select(.name=="Feature") | .id')

# 3. 생성
linear_create_issue \
  --title "..." \
  --description "..." \
  --teamId "$TEAM_ID" \
  --labelIds ["$LABEL_ID"]
```

### 상태 업데이트

```bash
# 1. Issue 조회
ISSUE=$(linear_get_issue --identifier "ECM-123")
ISSUE_UUID=$(echo $ISSUE | jq -r '.issue.id')

# 2. State 조회
TEAMS=$(linear_get_teams)
STATE_ID=$(echo $TEAMS | jq -r '.teams[].states[] | select(.name=="Done") | .id')

# 3. 업데이트
linear_edit_issue --issueId "$ISSUE_UUID" --stateId "$STATE_ID"
```

## 포맷팅 규칙

**금지**:
- ❌ 이모지 (title, description, comment)

**필수**:
- ✅ Plain text + markdown
- ✅ 기술 용어는 영어
