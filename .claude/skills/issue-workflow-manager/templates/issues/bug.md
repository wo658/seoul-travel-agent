# Bug Issue Template

버그 수정을 위한 Linear 이슈 생성.

## 체크리스트

- [ ] 버그 재현 확인
- [ ] Team 선택
- [ ] 제목 작성 (NO 이모지)
- [ ] 재현 단계 작성
- [ ] Priority 설정 (버그 심각도)
- [ ] Label 추가

## 프로세스

### 1. Team 조회
```bash
linear_get_teams
```

**추출 정보**:
- Team ID
- Bug label ID

### 2. Issue 내용 구조화

**Title 포맷** (한글 필수):
```
{위치} {문제} 수정
```

**예시** (기술명은 원본 영어 그대로):
- "데이터 프로세서 null pointer 에러 수정"
- "TourAPI 클라이언트 타임아웃 에러 수정"
- "LangGraph StateGraph 메모리 누수 수정"
- "PostgreSQL 연결 풀 고갈 오류 수정"
- "React Native 컴포넌트 렌더링 버그 수정"

**잘못된 예시**:
- ❌ "투어API 클라이언트 타임아웃 수정" → 원본 기술명(TourAPI) 필수
- ❌ "랭그래프 상태 관리 버그 수정" → 기술명 번역 금지

**Description 구조** (한글 필수):
```markdown
# 문제 설명
[버그에 대한 간단한 설명]

## 현재 동작
[실제로 발생하는 잘못된 동작]

## 기대 동작
[올바르게 동작해야 하는 방식]

## 재현 단계
1. 단계 1
2. 단계 2
3. 단계 3
4. 에러 발생 확인

## 환경 정보
- OS:
- 브라우저/런타임:
- 버전:

## 오류 로그
```
[에러 메시지 또는 스택 트레이스]
```

## 원인 분석
[원인이 파악된 경우 작성]

## 해결 방안
[제안하는 해결 방법]
```

### 3. Priority 결정

**Severity 기준**:
- 1 (Urgent): 서비스 중단, 데이터 손실
- 2 (High): 주요 기능 불가, 많은 사용자 영향
- 3 (Normal): 일부 기능 오류, 회피 방법 존재
- 4 (Low): UI 오류, 드문 케이스

### 4. Issue 생성

```bash
linear_create_issue \
  --title "한글 제목 (예: 데이터 프로세서 null 에러 수정)" \
  --description "$(cat <<'EOF'
# 문제 설명
[한글로 버그 설명]

## 현재 동작
[잘못된 동작]

## 기대 동작
[올바른 동작]

## 재현 단계
1. ...
2. ...

## 오류 로그
```
[로그]
```
EOF
)" \
  --teamId "team-uuid" \
  --priority 2 \
  --labelIds ["bug-label-uuid"]
```

## 예시

```
User: "TourAPI 클라이언트에서 타임아웃 에러 나는데 이슈 만들어줘"

1. Read templates/issues/bug.md (필수!)

2. linear_get_teams
   → Seoul-Agent (baf0b0fd-...)
   → Bug label (e58b5d28-...)

3. 내용 구성 (한글 + 기술명 영어):
   Title: "TourAPI 클라이언트 타임아웃 에러 수정"
   Description:
   # 문제 설명
   TourAPI 호출 시 간헐적으로 타임아웃 에러가 발생합니다.

   ## 현재 동작
   TourAPI 호출 시 5초 이상 걸릴 때 타임아웃으로 실패합니다.

   ## 기대 동작
   네트워크 지연 시에도 재시도 로직으로 안정적으로 데이터를 가져와야 합니다.

   ## 재현 단계
   1. TourAPI /areaBasedList1 엔드포인트 호출
   2. 네트워크 지연 상황 발생
   3. ReadTimeout 에러 확인

   ## 환경 정보
   - OS: Ubuntu 22.04
   - Runtime: Python 3.13
   - Version: backend v1.0.0
   - Library: httpx 0.28.1

   ## 오류 로그
   ```
   httpx.ReadTimeout: timed out
   File: backend/app/api/tourapi_client.py:45
   ```

   ## 원인 분석
   기본 타임아웃(5초)이 너무 짧고 재시도 로직 누락

   ## 해결 방안
   - 타임아웃 30초로 증가
   - exponential backoff 재시도 로직 추가 (최대 3회)

4. Priority 2 (High) - 주요 기능 영향
5. linear_create_issue
   → SEO-124 생성 완료
```

## 주의사항

**금지**:
- ❌ 이모지 사용
- ❌ 영어 제목 (한글 필수!)
- ❌ 재현 단계 생략
- ❌ 애매한 설명
- ❌ 템플릿 구조 무시

**권장**:
- ✅ 한글 제목 + 기술명은 원본 영어 (예: "TourAPI 클라이언트 에러 수정")
- ✅ 기술명 번역 금지 (TourAPI, LangGraph, PostgreSQL 등)
- ✅ 템플릿 구조 준수
- ✅ 재현 가능한 단계 작성
- ✅ 오류 로그 첨부
- ✅ 환경 정보 포함 (OS, 런타임, 라이브러리 버전)
- ✅ Severity에 맞는 priority 설정
