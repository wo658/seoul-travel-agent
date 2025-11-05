# Task Issue Template

작업, 개선, 리팩토링, 문서화 등을 위한 Linear 이슈 생성.

## 체크리스트

- [ ] 작업 목적 명확화
- [ ] Team 선택
- [ ] 제목 작성 (NO 이모지)
- [ ] 작업 내용 정리
- [ ] Priority 설정
- [ ] Label 추가

## 프로세스

### 1. Team 조회
```bash
linear_get_teams
```

### 2. Issue 내용 구조화

**Title 포맷**:
```
{동사} {대상}
```

**동사 선택**:
- Update: 기존 내용 수정
- Refactor: 코드 개선
- Improve: 성능/품질 향상
- Remove: 제거
- Upgrade: 버전 업그레이드
- Add: 추가 (작은 규모)

**예시**:
- "Update API documentation"
- "Refactor database connection pool"
- "Improve error handling"
- "Remove deprecated endpoints"
- "Upgrade React to v18"

**Description 구조**:
```markdown
# 목적
[작업의 목적과 배경]

## 작업 내용
- 작업 항목 1
- 작업 항목 2

## 예상 효과
- 효과 1
- 효과 2

## 체크리스트
- [ ] 항목 1
- [ ] 항목 2
```

### 3. Issue 생성

```bash
linear_create_issue \
  --title "제목" \
  --description "$(cat <<'EOF'
# 목적
[목적 설명]

## 작업 내용
- 항목들

## 체크리스트
- [ ] 완료 항목
EOF
)" \
  --teamId "team-uuid" \
  --priority 3 \
  --labelIds ["task-label-uuid"]
```

**Priority 가이드**:
- 2 (High): 긴급한 개선/리팩토링
- 3 (Normal): 일반 작업/문서화
- 4 (Low): 선택적 개선

## 예시

### 리팩토링
```
User: "API response handler 리팩토링 이슈 만들어"

Title: "Refactor API response handlers"
Description:
# 목적
중복 코드 제거 및 에러 처리 개선

## 작업 내용
- 공통 handler 함수 추출
- 에러 타입별 처리 로직 통합
- TypeScript 타입 정의 강화

## 예상 효과
- 코드 중복 50% 감소
- 유지보수성 향상
- 타입 안정성 확보
```

### 문서화
```
User: "API 문서 업데이트 이슈"

Title: "Update API documentation"
Description:
# 목적
v2 API endpoint 문서화

## 작업 내용
- 새로운 endpoint 추가
- 요청/응답 예시 업데이트
- 에러 코드 테이블 추가

## 체크리스트
- [ ] OpenAPI spec 업데이트
- [ ] README 수정
- [ ] 예시 코드 추가
```

### 기술 부채 해결
```
User: "레거시 코드 정리 이슈"

Title: "Remove deprecated authentication methods"
Description:
# 목적
v1 인증 방식 제거 및 v2 완전 전환

## 작업 내용
- v1 auth 관련 코드 제거
- v2 migration guide 작성
- 관련 테스트 정리

## 체크리스트
- [ ] 코드 제거
- [ ] 문서 업데이트
- [ ] 테스트 정리
```

## 주의사항

**금지**:
- ❌ 이모지 사용
- ❌ 애매한 제목
- ❌ 작업 목적 없이 나열만

**권장**:
- ✅ 작업 목적 명확히
- ✅ 구체적인 항목 리스트
- ✅ 예상 효과 포함
- ✅ 체크리스트 활용
