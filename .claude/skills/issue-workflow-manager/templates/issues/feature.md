# Feature Issue Template

새로운 기능 개발을 위한 Linear 이슈 생성.

## 체크리스트

- [ ] 요구사항 명확화
- [ ] Team 선택
- [ ] 제목 작성 (NO 이모지)
- [ ] Description 작성
- [ ] Priority 설정
- [ ] Label 추가

## 프로세스

### 1. Team 조회
```bash
linear_get_teams
```

**추출 정보**:
- Team ID (teamId)
- Feature label ID

### 2. Issue 내용 구조화

**Title 포맷**:
```
{동사} {대상} [{컨텍스트}]
```

**예시**:
- "Implement user authentication system"
- "Add workflow visualization component"
- "Build analytics dashboard"

**Description 구조**:
```markdown
# 개요
[1-2문장 요약]

## 요구사항
- 요구사항 1
- 요구사항 2

## Acceptance Criteria
- [ ] 기준 1
- [ ] 기준 2

## 기술 사항
[필요시 추가]
```

### 3. Issue 생성

```bash
linear_create_issue \
  --title "제목" \
  --description "$(cat <<'EOF'
# 개요
요약 내용

## 요구사항
- 요구사항 목록

## Acceptance Criteria
- [ ] 완료 기준
EOF
)" \
  --teamId "team-uuid" \
  --priority 2 \
  --labelIds ["feature-label-uuid"]
```

**Priority**:
- 0: None
- 1: Urgent
- 2: High
- 3: Normal
- 4: Low

### 4. 확인

생성 완료 후 반환:
- Issue identifier (ECM-XXX)
- Issue URL
- 현재 상태

## 예시

```
User: "워크플로우 시각화 컴포넌트 구현 이슈 만들어줘"

1. linear_get_teams
   → ECM-newtech (team-uuid)
   → Feature label (label-uuid)

2. 내용 구성:
   Title: "Implement workflow visualization component"
   Description:
   # 개요
   n8n 스타일 워크플로우 시각화 컴포넌트 구현

   ## 요구사항
   - JSON/Node View 토글
   - XYFlow 기반 노드 렌더링
   - 다크모드 통합

   ## Acceptance Criteria
   - [ ] View 토글 동작
   - [ ] 노드 렌더링 완료
   - [ ] 반응형 디자인 적용

3. linear_create_issue
   → ECM-109 생성 완료
   → https://linear.app/.../ECM-109
```

## 주의사항

**금지**:
- ❌ Title/Description에 이모지
- ❌ 애매한 제목 ("개선", "수정")
- ❌ 너무 긴 제목 (>60자)

**권장**:
- ✅ 명확한 동사로 시작
- ✅ Acceptance criteria 구체적으로
- ✅ 기술 용어는 영어 사용
