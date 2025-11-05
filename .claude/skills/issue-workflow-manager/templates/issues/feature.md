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

**Title 포맷** (한글 필수):
```
{대상} {동사} [{컨텍스트}]
```

**예시** (기술명은 원본 영어 그대로):
- "사용자 인증 시스템 구현"
- "LangGraph 기반 여행 계획 Agent 구현"
- "TourAPI 통합 및 클라이언트 구현"
- "React Native 워크플로우 시각화 컴포넌트 추가"
- "PostgreSQL 데이터베이스 스키마 설계"

**잘못된 예시**:
- ❌ "랭그래프 기반 여행 계획 에이전트 구현" → 기술명 번역 금지
- ❌ "투어API 통합" → 원본 기술명(TourAPI) 사용 필수

**Description 구조** (한글 필수):
```markdown
# 개요
[기능에 대한 1-2문장 요약]

## 배경
[왜 이 기능이 필요한지]

## 요구사항
- 요구사항 1
- 요구사항 2
- 요구사항 3

## 완료 조건 (Acceptance Criteria)
- [ ] 조건 1
- [ ] 조건 2
- [ ] 조건 3

## 기술 세부사항
[구현 방식, 사용할 기술, 파일 구조 등]

## 예상 기간
[선택사항: X주 또는 X일]
```

### 3. Issue 생성

```bash
linear_create_issue \
  --title "한글 제목 (예: TourAPI 클라이언트 모듈 구현)" \
  --description "$(cat <<'EOF'
# 개요
[한글로 기능 요약]

## 배경
[필요성 설명]

## 요구사항
- 요구사항 1
- 요구사항 2

## 완료 조건
- [ ] 조건 1
- [ ] 조건 2

## 기술 세부사항
[구현 방식]
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
User: "LangGraph 기반 여행 계획 Agent 이슈 만들어줘"

1. Read templates/issues/feature.md (필수!)

2. linear_get_teams
   → Seoul-Agent (baf0b0fd-...)
   → Feature label (e7a0acc4-...)

3. 내용 구성 (한글 + 기술명 영어):
   Title: "LangGraph 기반 여행 계획 Agent 구현"
   Description:
   # 개요
   LangGraph를 활용하여 다단계 여행 계획을 생성하는 Agent 시스템을 구현합니다.

   ## 배경
   사용자 입력(날짜, 예산, 선호도)을 기반으로 TourAPI 데이터와 결합하여
   실시간으로 최적화된 여행 계획을 생성해야 합니다.

   ## 요구사항
   - LangGraph StateGraph 기반 워크플로우
   - TourAPI 데이터 통합
   - PostgreSQL 상태 체크포인팅
   - FastAPI SSE 스트리밍

   ## 완료 조건
   - [ ] LangGraph StateGraph 구현 완료
   - [ ] 3개 Agent 노드 구현 (Collector, Fetcher, Generator)
   - [ ] PostgreSQL 체크포인팅 연동
   - [ ] SSE 스트리밍 테스트 통과

   ## 기술 세부사항
   - 프레임워크: LangGraph, FastAPI
   - 파일: backend/app/agents/workflow.py
   - 데이터베이스: PostgreSQL (체크포인팅)
   - API: TourAPI 4.0

4. linear_create_issue
   → SEO-33 생성 완료
   → https://linear.app/.../SEO-33
```

## 주의사항

**금지**:
- ❌ Title/Description에 이모지
- ❌ 영어 제목 (한글 필수!)
- ❌ 애매한 제목 ("개선", "수정")
- ❌ 너무 긴 제목 (>60자)
- ❌ 템플릿 구조 무시

**권장**:
- ✅ 한글 제목 + 기술명은 원본 영어 (예: "LangGraph 기반 Agent 구현")
- ✅ 기술명 번역 금지 (LangGraph, React, TourAPI, PostgreSQL 등)
- ✅ 템플릿 구조 준수
- ✅ 명확한 동사 사용 (구현, 추가, 구축)
- ✅ 완료 조건 구체적으로 작성
- ✅ 배경/필요성 명시
