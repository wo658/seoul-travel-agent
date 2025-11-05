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

**Title 포맷**:
```
Fix {문제} in {위치}
```

**예시**:
- "Fix null pointer exception in data processor"
- "Fix memory leak in analytics service"
- "Fix incorrect calculation in report generator"

**Description 구조**:
```markdown
# 문제

## 현재 동작
[실제 발생하는 문제]

## 기대 동작
[올바른 동작]

## 재현 단계
1. 단계 1
2. 단계 2
3. 결과 확인

## 환경
- OS:
- Browser/Runtime:
- Version:

## 오류 로그
```
[에러 메시지/스택 트레이스]
```

## 원인 분석
[파악된 경우 추가]

## 해결 방안
[제안사항]
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
  --title "Fix ..." \
  --description "$(cat <<'EOF'
# 문제
[문제 설명]

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
User: "데이터 프로세서에서 null pointer 에러 나는데 이슈 만들어줘"

1. linear_get_teams
   → Backend team
   → Bug label

2. 내용 구성:
   Title: "Fix null pointer exception in data processor"
   Description:
   # 문제
   대용량 데이터 처리 시 null pointer exception 발생

   ## 현재 동작
   데이터가 null일 때 프로세서가 크래시

   ## 재현 단계
   1. 빈 데이터셋 업로드
   2. 처리 실행
   3. Exception 발생 확인

   ## 오류 로그
   ```
   NullPointerException at DataProcessor.process():45
   ```

3. Priority 2 (High) - 주요 기능 영향
4. linear_create_issue
   → ECM-124 생성
```

## 주의사항

**금지**:
- ❌ 이모지 사용
- ❌ 재현 단계 생략
- ❌ 애매한 설명

**권장**:
- ✅ 재현 가능한 단계
- ✅ 오류 로그 첨부
- ✅ 환경 정보 포함
- ✅ Severity에 맞는 priority
