---
name: issue-workflow-manager
description: Linear 이슈 전체 생명주기 관리 스킬. 이슈 생성, 작업 시작(브랜치 생성), 작업 완료(PR/merge) 시 사용. 소규모 팀(1-4인)에 최적화됨.
---

# Issue Workflow Manager

Linear 이슈 기반 개발 워크플로우 관리.

## 필수 규칙 (MANDATORY)

### 언어 규칙
**모든 이슈 커뮤니케이션은 한글로 작성**
- ✅ Title: 한글 (예: "사용자 인증 시스템 구현")
- ✅ Description: 한글 (기술 용어는 영어 병기 가능)
- ✅ Comments: 한글
- ❌ 전체 영어 제목/설명 금지

**예외**:
- 기술명/라이브러리명: React, FastAPI, LangGraph, TourAPI 등 (원본 기술명은 반드시 영어)
- 브랜치명: feature/SEO-123-langgraph-integration (영어 필수)
- 코드 블록 내용
- 명령어 및 파일명
- 커밋 메시지: Conventional Commits 규칙 (영어)

### 템플릿 필수 사용
**이슈 생성 시 반드시 해당 타입의 템플릿을 먼저 로드하고 따라야 함**

1. 사용자 요청 분석 → 이슈 타입 결정 (feature/bug/task)
2. 해당 템플릿 파일 읽기 (Read tool 사용)
3. 템플릿 구조에 맞춰 내용 작성
4. Linear 이슈 생성

**템플릿 미사용 시 → 이슈 생성 거부**

## 워크플로우 선택

**이슈 생성?**
→ **필수**: `templates/issues/{type}.md` 먼저 로드
- `feature.md`: 새 기능 개발
- `bug.md`: 버그 수정
- `task.md`: 작업/개선/문서화

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
**Branch** (영어 필수): `{type}/{ISSUE-ID}-{description}`
```
feature/SEO-123-user-auth
feature/SEO-127-langgraph-workflow
bugfix/SEO-124-null-fix
task/SEO-125-refactor-api
```

**Commit** (영어 필수): Conventional Commits
```
feat(auth): add JWT validation
feat(agent): implement LangGraph state machine
fix(api): resolve null pointer
docs(readme): update installation guide
```

**기술명 사용 규칙**:
- ✅ 원본 기술명 그대로: React, FastAPI, LangGraph, PostgreSQL, TourAPI
- ✅ 브랜치 설명: langgraph-integration, react-components, tourapi-client
- ❌ 번역 금지: 랭그래프, 리액트, 투어API (X)

### Linear 포맷팅
- ❌ 이모지 사용 금지 (title, description, comment 모두)
- ✅ Plain text + markdown만 사용
- ✅ 한글로 명확하고 전문적인 톤
- ✅ 기술 용어는 영어 병기 가능

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

### Feature 개발 (올바른 예시)
```
1. "LangGraph 기반 여행 계획 Agent 구현 이슈 생성해줘"
   → Read templates/issues/feature.md (필수)
   → 템플릿 구조 확인
   → Linear 이슈 생성 (한글 제목/설명, 기술명은 영어)
   → Title: "LangGraph 기반 여행 계획 Agent 구현"
   → Description: 한글 작성 + 기술명(LangGraph, FastAPI, PostgreSQL)은 영어

2. "SEO-123 작업 시작할게"
   → templates/start-work.md 로드
   → feature/SEO-123-langgraph-agent branch 생성 (영어)
   → 첫 커밋: "feat(agent): initialize LangGraph workflow structure"

3. [개발 진행...]

4. "SEO-123 완료했어"
   → templates/complete-work.md 로드
   → PR 생성 (Title: "LangGraph 기반 Agent 구현 완료", 한글)
   → merge, cleanup
```

### Bug 수정 (올바른 예시)
```
1. "TourAPI 클라이언트 타임아웃 버그 이슈 만들어줘"
   → Read templates/issues/bug.md (필수)
   → 템플릿 구조 확인
   → Title: "TourAPI 클라이언트 타임아웃 에러 수정" (기술명 영어)
   → Description: 한글 (재현 단계, 로그 포함)

2. "SEO-124 시작"
   → bugfix/SEO-124-tourapi-timeout branch (영어)
   → 첫 커밋: "fix(api): add timeout handling for TourAPI client"

3. "SEO-124 완료"
   → PR merge, cleanup
```

### 잘못된 예시 (금지)
```
❌ "Implement LangGraph-based travel planning agent"
   → 제목 전체 영어 금지 (기술명만 영어)
   ✅ 올바른 예: "LangGraph 기반 여행 계획 Agent 구현"

❌ Title: "랭그래프 워크플로우 구현"
   → 기술명 번역 금지
   ✅ 올바른 예: "LangGraph 워크플로우 구현"

❌ Branch: feature/SEO-123-랭그래프-통합
   → 브랜치명 한글 금지
   ✅ 올바른 예: feature/SEO-123-langgraph-integration

❌ 템플릿 로드 없이 바로 이슈 생성
   → 반드시 템플릿 먼저 읽기

❌ "🎉 새 기능 추가"
   → 이모지 사용 금지
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
