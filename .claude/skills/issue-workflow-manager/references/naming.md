# 명명 규칙 빠른 참조

## Branch 명명

### 포맷
```
{type}/{ISSUE-ID}-{description}
```

### Type
- `feature/`: 새 기능
- `bugfix/`: 버그 수정
- `hotfix/`: 긴급 수정
- `refactor/`: 리팩토링
- `docs/`: 문서
- `chore/`: 기타

### Description
- kebab-case (소문자-하이픈)
- 3-5 단어
- 핵심만 추출

### 예시
```
feature/ECM-123-user-auth
bugfix/ECM-124-null-fix
hotfix/ECM-125-security
docs/ECM-126-api-docs
```

## Commit 메시지

### Conventional Commits
```
{type}[({scope})]: {description}
```

### Type
- `feat`: 새 기능
- `fix`: 버그 수정
- `docs`: 문서
- `refactor`: 리팩토링
- `test`: 테스트
- `chore`: 기타

### 예시
```
feat(auth): add JWT validation
fix(api): resolve null pointer
docs(readme): update setup guide
refactor(utils): simplify helpers
```

### 규칙
- 소문자로 시작
- 명령형 ("add" not "added")
- 50자 이내
- 마침표 없음

## Issue Title

### 포맷
```
{동사} {대상} [{컨텍스트}]
```

### 예시
```
Implement user authentication system
Fix memory leak in data processor
Update API documentation for v2
Refactor database connection pool
```

### 규칙
- 명확한 동사로 시작
- NO 이모지
- 60자 이내
- 기술 용어는 영어

## PR Title

Issue title과 동일, NO 이모지

## Linear 포맷팅

**금지**:
- ❌ 이모지 (모든 곳)

**필수**:
- ✅ Plain text + markdown
- ✅ 기술적/전문적 톤
- ✅ 기술 용어는 영어
