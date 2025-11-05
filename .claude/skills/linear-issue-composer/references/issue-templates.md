# Linear Issue Templates

4가지 issue 유형에 대한 완전한 template: Bug, Feature, Task, Improvement

**작성 원칙:**
- 기술 용어는 영어 유지 (예: API, endpoint, component, middleware, frontend, backend 등)
- 설명과 문맥은 한글 사용
- 이모지 사용 금지 - Plain text만 사용
- Markdown 형식으로 구조화

## Bug Template

### Title Format
```
bug: [버그 증상 요약] (50자 이내)
```

### Description Template

```markdown
## 버그 설명

### 현재 동작
[발생하는 문제를 구체적으로 설명]

### 예상 동작
[정상 작동 시 어떻게 동작해야 하는지]

### 버그 발생 빈도
- [ ] 항상 (100%)
- [ ] 자주 (>50%)
- [ ] 가끔 (10-50%)
- [ ] 드물게 (<10%)

## 재현 단계

### 전제 조건
[버그를 재현하기 위한 초기 설정 또는 조건]

### 재현 단계
1. [첫 번째 단계]
2. [두 번째 단계]
3. [세 번째 단계]
4. [결과 확인]

## 로그 및 에러

### Browser Console Log
```
[브라우저 console에서 확인된 error log]
```

### Server Log
```
[서버 log 출력]
```

### Stack Trace
```
[Stack trace가 있는 경우]
```

## 영향도 분석

### 심각도
- [ ] Critical (앱 사용 불가)
- [ ] High (주요 기능 사용 불가)
- [ ] Medium (일부 기능 제한)
- [ ] Low (UI 문제, 사소한 불편)

### 영향 범위
[이 버그가 영향을 미치는 사용자 범위나 시나리오]

## 임시 해결책
[버그를 우회할 수 있는 방법이 있다면 설명]

## 추가 정보
- 관련 이슈: #[이슈 번호]
- 최근 변경사항: [관련 PR이나 최근 변경 내용]
```

### Examples

**Good Bug Title:**
- `bug: 로그인 후 채팅 목록 미표시`
- `bug: 파일 업로드 진행률 100%에서 멈춤`
- `bug: 모바일 메시지 입력창 키보드에 가려짐`

**Bad Bug Title:**
- `문제 있음` (너무 모호함)
- `채팅이 안돼요` (구체성 부족)
- `🐛 로그인 버그` (이모지 사용 금지)

---

## Feature Template

### Title Format
```
feat: [기능 요약] (50자 이내)
```

### Description Template

```markdown
## 문제 정의

### 현재 상황
[현재의 문제점이나 제약사항]

### 사용자 요구사항
[누가, 왜 이 기능이 필요한지 설명]

## 제안 솔루션

### 기능 개요
[구현하고자 하는 기능의 전체적인 개요]

### 주요 기능
- [ ] 핵심 기능 1
- [ ] 핵심 기능 2
- [ ] 핵심 기능 3

### UI/UX 상세
[사용자 플로우 및 화면 구성 설명]
[와이어프레임이나 목업이 있다면 링크 추가]

## 기술 사양

### 기술 스택
- Frontend: [사용할 프론트엔드 기술]
- Backend: [사용할 백엔드 기술]
- 라이브러리: [필요한 라이브러리 목록]

### 구현 방법
[기술적 접근 방식 설명]

### API 변경사항
[새로운 API 엔드포인트 또는 기존 API 변경 내용]

```http
POST /api/new-endpoint
GET /api/existing-endpoint?new-param=value
```

## 수용 기준

- [ ] 기준 1: [명확하고 측정 가능한 완료 조건]
- [ ] 기준 2: [명확하고 측정 가능한 완료 조건]
- [ ] 기준 3: [명확하고 측정 가능한 완료 조건]
- [ ] 테스트 작성 및 통과
- [ ] 문서 업데이트

## 예상 효과

### 비즈니스 임팩트
[이 기능이 가져올 비즈니스적 영향]

### 성능 지표
[측정 가능한 목표 지표]
- 사용자 만족도: [목표]
- 사용 빈도: [목표]
- 성능 개선: [목표]

## 추가 정보

### 참고 자료
- [관련 문서 링크]
- [참고 이미지 링크]
- [외부 레퍼런스]

### 추정 작업 크기
- [ ] Small (1-2일)
- [ ] Medium (3-5일)
- [ ] Large (1-2주)
```

### Examples

**Good Feature Title:**
- `feat: 채팅 메시지 검색 기능 추가`
- `feat: RAG 문서 업로드 진행률 표시`
- `feat: 사용자 프로필 이미지 업로드`

**Bad Feature Title:**
- `새 기능` (무엇인지 불명확)
- `검색 만들기` (너무 짧고 맥락 부족)
- `✨ 메시지 검색 추가` (이모지 사용 금지)

---

## Task Template

### Title Format
```
task: [작업 내용 요약] (50자 이내)
또는
docs/chore/test/build: [작업 내용]
```

### Description Template

```markdown
## 작업 목표

### 작업 개요
[작업 내용 및 필요성을 간단히 설명]

### 배경/동기
[왜 이 작업을 수행해야 하는지]

## 작업 상세

### 주요 작업 내용
- [ ] 주요 작업 1
- [ ] 주요 작업 2
- [ ] 주요 작업 3

### 세부 체크리스트

#### 작업 항목 1
- [ ] 세부 작업 1-1
- [ ] 세부 작업 1-2
- [ ] 세부 작업 1-3

#### 작업 항목 2
- [ ] 세부 작업 2-1
- [ ] 세부 작업 2-2

## 작업 범위

### 포함 사항
[이 작업에 포함되는 내용]

### 제외 사항
[이 작업에서 제외하고 별도 이슈로 분리할 내용]

## 완료 조건

- [ ] 완료 조건 1
- [ ] 완료 조건 2
- [ ] 테스트 통과
- [ ] 문서 업데이트 (필요 시)
- [ ] 코드 리뷰 승인

## 기술 세부사항

### 변경 파일 목록
[수정이 필요한 파일 경로]
```
backend/apps/webui/models/users.py
frontend/src/lib/components/chat/Settings.svelte
```

### 의존성 변경
[추가하거나 제거할 패키지]
```
+ new-package==1.0.0
- old-package==0.9.0
```

## 예상 작업 시간

- [ ] Small (0.5일 이하)
- [ ] Medium (0.5-2일)
- [ ] Large (2-5일)

## 의존성

### 선행 작업
[이 작업을 시작하기 전에 완료되어야 할 작업]
- 관련 이슈: #[이슈 번호]

### 차단 요소
[작업을 방해하는 요소]

### 후속 작업
[이 작업 완료 후 진행할 작업]
- 관련 이슈: #[이슈 번호]

## 테스트 계획

### 테스트 항목
- [ ] 테스트 항목 1
- [ ] 테스트 항목 2
- [ ] 회귀 테스트

### 테스트 환경
[테스트를 수행할 환경]

## 문서화

### 업데이트 필요 문서
- [ ] README.md
- [ ] 사용자 가이드
- [ ] API 문서
- [ ] CHANGELOG.md
```

### Examples

**Good Task Title:**
- `task: Python 3.12 마이그레이션`
- `docs: API 엔드포인트 문서 업데이트`
- `chore: Docker 이미지 Ubuntu 22.04 변경`

**Bad Task Title:**
- `작업` (내용 불명확)
- `업데이트` (무엇을 업데이트하는지 모호)
- `📝 문서 작성` (이모지 사용 금지)

---

## Improvement Template

### Title Format
```
improve/refactor/perf: [개선 내용 요약] (50자 이내)
```

### Description Template

```markdown
## 현재 상황 분석

### 문제점
[개선이 필요한 사항을 구체적으로 설명]

### 영향 범위
[문제가 미치는 영향]

### 현재 코드
```language
[문제가 있는 현재 코드 스니펫]
```

## 개선 목표

### 기대 효과
[개선 후 얻을 수 있는 결과]

### 측정 지표
- [ ] 측정 목표 1
- [ ] 측정 목표 2
- [ ] 측정 목표 3

## 개선 방법

### 제안 솔루션
[구체적인 해결 방법 설명]

### 개선 후 코드
```language
[개선된 코드 예시]
```

### 구현 단계
1. [구현 1단계]
2. [구현 2단계]
3. [구현 3단계]

## 개선 유형

- [ ] 성능 최적화
- [ ] 코드 품질 개선
- [ ] 리팩토링
- [ ] 기술 부채 해소
- [ ] 보안 강화
- [ ] 아키텍처 개선

## 기술 세부사항

### 영향 컴포넌트
[수정될 영역이나 컴포넌트]

### 변경 사항
[구체적인 변경 내용]

### 호환성
[하위 호환성 유지 여부 및 Breaking Changes]

## 성능 지표 (성능 개선 시)

### 현재 성능
- 응답 시간: [현재 값]
- 쿼리 수: [현재 값]
- CPU/메모리: [현재 값]

### 목표 성능
- 응답 시간: [목표 값]
- 쿼리 수: [목표 값]
- CPU/메모리: [목표 값]

### 측정 방법
[벤치마크 도구 및 측정 방법]

## 리팩토링 범위 (리팩토링 시)

### 대상 코드
[리팩토링할 영역]

### 적용 원칙
[적용할 설계 원칙이나 패턴]
- SOLID 원칙
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)

### Before/After 구조
[구조 변경 내용을 다이어그램이나 텍스트로 설명]

## 완료 조건

- [ ] 목표 지표 달성
- [ ] 기존 테스트 모두 통과
- [ ] 새로운 테스트 추가
- [ ] 코드 리뷰 승인
- [ ] 문서 업데이트

## 리스크

### 잠재적 위험
[예상되는 위험 요소]

### 완화 방안
[위험을 줄이기 위한 대응책]

## 테스트

### 테스트 범위
- [ ] 단위 테스트
- [ ] 통합 테스트
- [ ] 성능 테스트
- [ ] 회귀 테스트

## 예상 작업 시간

- [ ] Small (1-2일)
- [ ] Medium (3-5일)
- [ ] Large (1-2주)
```

### Examples

**Good Improvement Title:**
- `improve: 채팅 메시지 로딩 성능 30% 개선`
- `refactor: 인증 로직 별도 서비스 분리`
- `perf: 데이터베이스 쿼리 N+1 문제 해결`

**Bad Improvement Title:**
- `개선` (무엇을 개선하는지 불명확)
- `코드 수정` (목적과 범위 모호)
- `⚡ 성능 개선` (이모지 사용 금지)

---

## Template Usage Guidelines

### Choosing the Right Template

**Use Bug Template when:**
- Something is broken or not working as expected
- There's an error message or unexpected behavior
- A feature that used to work is now failing

**Use Feature Template when:**
- Adding completely new functionality
- Extending existing features with new capabilities
- Implementing user-requested enhancements

**Use Task Template when:**
- Performing maintenance work
- Updating documentation
- Migrating to new versions or platforms
- Setting up infrastructure or configuration

**Use Improvement Template when:**
- Optimizing performance
- Refactoring code for better quality
- Addressing technical debt
- Enhancing security
- Improving architecture

### Customization Guidelines

Templates are starting points - customize them based on:
- Available information (skip sections if data unavailable)
- Issue complexity (simple bugs may not need all sections)
- Project conventions (adapt to team standards)
- Specific context (add sections if needed)

### Quality Checklist

Before submitting any issue, verify:
- [ ] Title follows format: `type: description (under 50 chars)`
- [ ] No emojis used anywhere
- [ ] All required sections filled
- [ ] Code blocks have syntax highlighting
- [ ] Links are valid
- [ ] Priority matches severity
- [ ] Appropriate labels selected
- [ ] Related issues linked
