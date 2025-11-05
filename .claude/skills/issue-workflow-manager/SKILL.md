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

**이슈 수정?**
→ **이슈 수정만 진행** (다른 작업 금지)
- Linear MCP로 이슈 정보 조회
- 필요한 필드만 수정 (title, description, state 등)
- 코드 작업 없이 이슈 메타데이터만 변경

**작업 시작?**
→ `templates/start-work.md` 로드

**작업 완료?**
→ `templates/complete-work.md` 로드

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
# Issue 생성
linear_create_issue --title "..." --description "..." --teamId "..."

# Issue 조회/수정
linear_get_issue --identifier "SEO-123"
linear_edit_issue --issueId "uuid" --title "..." --description "..." --stateId "..."
```

### Git/PR
```bash
git checkout -b feature/SEO-123-description
git push -u origin feature/SEO-123-description
gh pr create --title "..." --body "..."
gh pr merge --merge --delete-branch
```

## Templates

- `templates/issues/{type}.md`: 이슈 타입별 생성 template
- `templates/start-work.md`: 작업 시작 절차
- `templates/complete-work.md`: PR 생성 및 완료
- `references/`: 상세 참고 문서 (필요시 로드)

## 예시

### Feature 개발
```
1. "LangGraph Agent 이슈 생성" → Read templates/issues/feature.md → 이슈 생성
2. "SEO-123 시작" → branch 생성 (feature/SEO-123-langgraph-agent)
3. "SEO-123 완료" → PR 생성/merge
```

### 이슈 수정 (다른 작업 금지)
```
1. "SEO-123 이슈 제목 수정해줘"
   → linear_get_issue로 조회
   → linear_edit_issue로 title만 수정
   → 코드 작업/브랜치 생성 등 다른 작업 진행 안 함

2. "SEO-124 상태를 In Progress로 변경"
   → 이슈 상태만 변경, 다른 작업 진행 안 함
```

### 잘못된 예시
```
❌ 전체 영어 제목: "Implement agent" → ✅ "Agent 구현"
❌ 기술명 번역: "랭그래프" → ✅ "LangGraph"
❌ 한글 브랜치: feature/SEO-123-에이전트 → ✅ feature/SEO-123-agent
❌ 템플릿 없이 이슈 생성 → ✅ 템플릿 먼저 로드
❌ 이모지 사용: "🎉 기능 추가" → ✅ "기능 추가"
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

- Linear 인증: `echo $LINEAR_ACCESS_TOKEN`
- Branch 충돌: `git branch -D old-branch`
- PR 실패: `gh auth status`
- Merge conflict: fetch → merge → resolve → commit → push
