# 서울 여행 AI 에이전트 애플리케이션 기획서

---

## 1. AI 서비스 명칭

**Seoul Travel Agent (서울 여행 AI 도우미)**

- **영문명**: Seoul Travel Agent - AI-Powered Travel Planning Assistant
- **한글명**: 서울 여행 AI 도우미
- **부제**: 사전 계획부터 실시간 가이드까지, 당신의 완벽한 서울 여행 파트너

---

## 2. 활용 인공지능 학습용 데이터

### 2.1 공공 오픈 데이터

#### 서울시 관광 데이터
- **서울시 관광숙박업 인허가 정보**
  - 제공 기관: 서울시 열린데이터광장
  - 데이터 내용: 호텔, 게스트하우스, 한옥스테이 등 숙박업소 위치, 등급, 편의시설 정보
  - 활용 목적: 숙박 추천 및 예산 기반 숙소 필터링

- **전국 관광지 정보 표준 데이터**
  - 제공 기관: 한국관광공사 TourAPI 4.0
  - 데이터 내용: 관광 명소, 자연 경관, 문화재, 박물관 등의 위치, 운영시간, 설명, 이미지
  - 활용 목적: 여행지 추천 및 일정 생성

### 2.2 벡터 데이터베이스 (RAG)
- **관광지 정보 벡터 스토어**
  - 기술: Sentence Transformers 기반 임베딩
  - 저장소: ChromaDB (영구 저장)
  - 용도: 사용자 선호도 기반 유사 관광지 검색
  - 검색 방식: 코사인 유사도 기반 의미론적 검색

### 2.3 AI 모델
- **대규모 언어 모델 (LLM)**
  - 주 모델: OpenAI GPT-4o / Anthropic Claude 3.5 Sonnet
  - 용도: 자연어 대화, 여행 계획 생성, 맥락 이해 및 추천

- **임베딩 모델**
  - 모델: Sentence Transformers (all-MiniLM-L6-v2)
  - 용도: 관광지 설명 벡터화 및 유사도 검색

### 2.4 실시간 데이터 소스
- **Naver Places API**
  - 제공 정보: 실시간 영업시간, 리뷰, 평점, 전화번호
  - 활용 목적: 최신 장소 정보 제공 및 계획 검증

---

## 3. 핵심 내용

### 3.1 서비스 개요
Seoul Travel Agent는 **두 가지 전문 AI 에이전트**로 구성된 서울 여행 종합 플래너 애플리케이션입니다.

1. **Planner Agent (계획 수립 에이전트)**
   - 여행 전 사전 계획 수립 및 일정 생성
   - 사용자 선호도, 예산, 날짜 기반 맞춤형 추천
   - 실제 서울 관광 데이터를 활용한 현실적인 일정 제안

2. **Reviewer Agent (실시간 가이드 에이전트)**
   - 여행 중 계획 수정 및 실시간 피드백 반영
   - 상황 변화(날씨, 체력, 돌발 상황) 대응
   - 계획 승인/거절/수정 결정 및 재계획 지원

### 3.2 핵심 기술 스택

#### Frontend
- **Framework**: React Native 0.81 + Expo 54
- **Styling**: NativeWind (Tailwind CSS for React Native)
- **Language**: TypeScript
- **특징**: 크로스 플랫폼 지원 (iOS, Android, Web)

#### Backend
- **Framework**: FastAPI (Python 3.12+)
- **Database**: SQLite (개발) / PostgreSQL (프로덕션)
- **ORM**: SQLAlchemy 2.0
- **AI 워크플로우**: LangGraph (StateGraph 기반)

#### AI Infrastructure
- **LLM**: OpenAI GPT-4o / Anthropic Claude 3.5 Sonnet
- **Vector Store**: ChromaDB (관광지 정보 임베딩)
- **Workflow Engine**: LangGraph (Multi-Agent Orchestration)

### 3.3 주요 기능

#### 1) 사전 여행 계획 (Planner Agent)
```
사용자 입력: "3일간 서울 여행, 예산 50만원, 역사 문화 관심"
       ↓
[정보 수집] → [관광지 검색] → [일정 생성] → [계획 제시]
       ↓
출력: 일자별 상세 일정 (시간대별 관광지, 이동 경로, 식당 추천)
```

**세부 프로세스**:
- **collect_info**: 여행 기간, 예산, 선호도, 동행인 정보 수집
- **fetch_venues**: 벡터 DB에서 유사 관광지 검색 + Naver API로 최신 정보 보강
- **generate_plan**: LLM 기반 일정 생성 (시간대별 최적 경로 고려)

#### 2) 실시간 여행 가이드 (Reviewer Agent)
```
여행 중 상황: "비가 와서 야외 활동이 어려워요"
       ↓
[피드백 분석] → [수정/거절/승인 판단] → [대안 일정 생성] → [검증] → [제시]
       ↓
출력: 실내 활동 중심 수정 일정 (박물관, 카페, 쇼핑몰)
```

**세부 프로세스**:
- **parse_feedback**: 사용자 피드백 의도 파악 (approve/reject/modify)
- **modify_plan**: 기존 계획 유지하며 특정 부분만 수정
- **validate_modification**: 수정된 계획의 타당성 검증

#### 3) 데이터 기반 추천 시스템
- **벡터 유사도 검색**: 사용자 선호 키워드와 관광지 설명 임베딩 비교
- **실시간 정보 통합**: Naver Places API로 영업시간, 휴무일 확인
- **예산 최적화**: 입장료, 식비, 교통비 고려한 일정 조정

---

## 4. 제안 배경 및 목적

### 4.1 배경

#### 문제 인식
1. **기존 여행 앱의 한계**
   - 정적인 추천: 사용자 맥락 무시한 일반적 추천
   - 실시간 대응 부족: 여행 중 변경사항 대응 어려움
   - 데이터 신뢰성: 오래된 정보로 인한 실망 경험

2. **서울 여행자의 실제 니즈**
   - 외국인 관광객: 언어 장벽, 복잡한 대중교통 시스템
   - 국내 관광객: 숨은 명소 발굴, 혼잡도 회피 욕구
   - 모든 여행자: 실시간 상황 변화 대응 필요

3. **AI 기술의 성숙**
   - LLM의 자연어 이해 능력 향상
   - Multi-Agent 시스템의 안정화 (LangGraph)
   - RAG 기술로 환각(Hallucination) 문제 해결

### 4.2 목적

#### 주요 목표
1. **개인화된 여행 경험 제공**
   - 사용자 선호도, 체력, 예산 맞춤형 일정
   - 과거 여행 이력 학습을 통한 추천 정확도 향상

2. **실시간 적응형 서비스**
   - 날씨, 교통, 혼잡도 등 실시간 변수 반영
   - 사용자 피드백 즉시 반영한 계획 재수립

3. **신뢰할 수 있는 정보 제공**
   - 공공 데이터 + 실시간 API 결합
   - AI 환각 방지를 위한 RAG 시스템 구축

4. **서울 관광 산업 활성화**
   - 비주류 관광지 홍보 지원
   - 계절별, 테마별 다양한 코스 제안

---

## 5. 세부 내용

### 5.1 시스템 아키텍처

#### 전체 구조
```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React Native)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  홈 화면     │  │  채팅 화면   │  │  일정 뷰어   │      │
│  │  (계획 생성) │  │  (대화형 UI) │  │  (타임라인)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/SSE
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            AI Agent Orchestration Layer              │   │
│  │  ┌────────────────┐      ┌────────────────┐         │   │
│  │  │ Planner Agent  │      │ Reviewer Agent │         │   │
│  │  │  (LangGraph)   │◄────►│  (LangGraph)   │         │   │
│  │  └────────────────┘      └────────────────┘         │   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↕                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Vector Store │  │  PostgreSQL  │  │  Naver API   │      │
│  │  (ChromaDB)  │  │  (Plans/Users)│  │  (Real-time) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 데이터 모델

#### 핵심 엔티티

**1) User (사용자)**
```python
- id: int (PK)
- email: str (unique)
- full_name: str
- created_at: datetime
- preferences: dict (JSON) # 선호 카테고리, 예산 범위 등
```

**2) TravelPlan (여행 계획)**
```python
- id: int (PK)
- user_id: int (FK)
- title: str
- start_date: datetime
- end_date: datetime
- itinerary: dict (JSON) # 일정 상세
  ├─ day_1: [
  │    {time: "09:00", venue: "경복궁", duration: 120, ...},
  │    {time: "12:00", venue: "광장시장", duration: 90, ...}
  │  ]
  ├─ day_2: [...]
- recommendations: dict (JSON) # AI 추천 데이터
  ├─ attractions: [{name, address, category, ...}]
  ├─ restaurants: [{name, cuisine, price_range, ...}]
  ├─ nature_spots: [...]
- budget: float
- status: str (planning/active/completed)
```

**3) Conversation (대화 이력)**
```python
- id: int (PK)
- user_id: int (FK)
- travel_plan_id: int (FK, nullable)
- title: str
- status: str (active/completed/archived)
- messages: List[Message]
```

**4) Message (메시지)**
```python
- id: int (PK)
- conversation_id: int (FK)
- role: str (user/assistant/system)
- content: str
- model: str (gpt-4o/claude-3-5-sonnet)
- created_at: datetime
```

**5) Venue (관광지 - Vector DB)**
```python
- id: str
- name: str
- category: str (관광지/음식점/자연경관)
- address: str
- description: str
- embedding: List[float] # 768차원 벡터
- metadata: dict
  ├─ opening_hours: str
  ├─ price: str
  ├─ website: str
  └─ images: List[str]
```

### 5.3 AI 에이전트 상세 설계

#### Planner Agent (계획 수립)

**State 구조**:
```python
class PlanningState(TypedDict):
    messages: List[dict]           # 대화 이력
    user_preferences: dict         # 선호도
    travel_dates: dict             # 여행 기간
    budget: float                  # 예산
    venues: List[dict]             # 검색된 관광지
    draft_plan: dict               # 초안 일정
    final_plan: dict               # 최종 일정
    retry_count: int               # 재시도 횟수
```

**워크플로우**:
```
START
  ↓
[collect_info]
  - 사용자 입력 파싱 (LLM)
  - 여행 기간, 예산, 선호 카테고리 추출
  - State 업데이트
  ↓
[fetch_venues]
  - Vector DB 유사도 검색 (선호 키워드 임베딩)
  - Top 20 관광지 검색
  - Naver API로 실시간 정보 보강
  - State.venues 저장
  ↓
[generate_plan]
  - LLM에게 일정 생성 요청
  - 입력: user_preferences, venues, dates, budget
  - 출력: JSON 형식 일자별 일정
  - State.draft_plan 저장
  ↓
END (최종 계획 반환)
```

**주요 기능**:
- **스마트 시간 배분**: 관광지 간 이동시간 자동 계산
- **예산 관리**: 입장료, 식비, 교통비 누적 계산
- **피로도 고려**: 하루 최대 이동 거리 제한

#### Reviewer Agent (피드백 반영)

**State 구조**:
```python
class ReviewState(TypedDict):
    original_plan: dict           # 원본 일정
    user_feedback: str            # 사용자 피드백
    feedback_type: str            # approve/reject/modify
    modification_scope: List[str] # 수정 대상 (day_1, lunch 등)
    modified_plan: dict           # 수정된 일정
    validation_result: dict       # 검증 결과
```

**워크플로우**:
```
START
  ↓
[parse_feedback]
  - LLM으로 피드백 의도 분석
  - 분류: approve/reject/modify
  - 수정 범위 추출 (예: "2일차 저녁 일정만 변경")
  ↓
[route_feedback] (조건 분기)
  - approve → END (계획 확정)
  - reject → END (Planner Agent 재호출 필요)
  - modify → modify_plan 진행
  ↓
[modify_plan]
  - 기존 계획 유지
  - 지정 범위만 LLM으로 재생성
  - 예산, 시간 제약 유지
  ↓
[validate_modification]
  - 수정 일정 타당성 검증
  - 시간 중복 체크
  - 이동 거리 재계산
  ↓
END (수정 계획 반환)
```

**주요 기능**:
- **부분 수정**: 전체 일정 중 특정 부분만 변경
- **맥락 유지**: 기존 일정의 흐름 보존
- **다중 반복**: 만족할 때까지 수정 반복 가능

### 5.4 API 엔드포인트

#### 1) 대화 관리
```
POST   /api/ai/conversations              # 새 대화 시작
GET    /api/ai/conversations              # 대화 목록 조회
GET    /api/ai/conversations/{id}         # 대화 이력 조회
DELETE /api/ai/conversations/{id}         # 대화 삭제
```

#### 2) 메시지 전송
```
POST   /api/ai/conversations/{id}/messages        # 메시지 전송 (동기)
POST   /api/ai/conversations/{id}/messages/stream # SSE 스트리밍 (비동기)
```

**SSE 스트리밍 예시**:
```
data: {"type": "agent_start", "agent": "planner"}
data: {"type": "node_start", "node": "collect_info"}
data: {"type": "token", "content": "여행 "}
data: {"type": "token", "content": "기간을 "}
data: {"type": "node_end", "node": "collect_info"}
data: {"type": "agent_end", "result": {...}}
```

#### 3) 계획 생성 (Planner Agent)
```
POST   /api/plans/generate
Request Body:
{
  "conversation_id": "123",
  "user_input": "3일간 서울 여행, 역사 문화 관심, 예산 50만원"
}

Response:
{
  "plan_id": "456",
  "status": "success",
  "itinerary": {
    "day_1": [
      {
        "time": "09:00",
        "venue": "경복궁",
        "category": "관광지",
        "duration": 120,
        "cost": 3000,
        "description": "조선시대 정궁..."
      }
    ]
  },
  "total_cost": 480000,
  "summary": "역사 중심 3일 코스"
}
```

#### 4) 계획 수정 (Reviewer Agent)
```
POST   /api/plans/{id}/review
Request Body:
{
  "feedback": "2일차 점심을 한식으로 변경해주세요",
  "feedback_type": "modify"
}

Response:
{
  "status": "modified",
  "changes": {
    "day_2": {
      "lunch": {
        "old": "이탈리안 레스토랑",
        "new": "전주비빔밥",
        "reason": "사용자 요청 반영"
      }
    }
  },
  "updated_plan": {...}
}
```

#### 5) 관광지 검색
```
GET    /api/venues/search?q=궁궐&category=관광지&limit=10
Response:
{
  "results": [
    {
      "id": "venue_001",
      "name": "경복궁",
      "category": "관광지",
      "similarity_score": 0.92,
      "address": "서울시 종로구...",
      "opening_hours": "09:00-18:00",
      "price": "3000원",
      "naver_rating": 4.5
    }
  ]
}
```

### 5.5 프론트엔드 화면 구성

#### 1) 홈 화면
- **신규 계획 생성** 버튼
- **저장된 계획 목록** (카드 형식)
- **빠른 시작** 템플릿 (1일 코스, 3일 코스 등)

#### 2) 채팅 화면
- **대화형 UI**: 사용자 메시지 / AI 응답
- **타이핑 인디케이터**: 스트리밍 중 애니메이션
- **일정 미리보기 카드**: 생성된 일정 인라인 표시
- **피드백 버튼**: "좋아요", "수정 요청", "다시 생성"

#### 3) 일정 뷰어 화면
```
┌─────────────────────────────────────────┐
│  서울 3일 역사 문화 여행                │
│  2024.12.20 - 12.22                     │
├─────────────────────────────────────────┤
│  [Day 1] 2024.12.20 (금)                │
│  ┌──────────────────────────────────┐   │
│  │ 09:00 - 11:00  경복궁           │   │
│  │ 🏛️ 관광지 │ 3,000원           │   │
│  │ 📍 서울시 종로구...            │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │ 12:00 - 13:30  광장시장         │   │
│  │ 🍜 음식점 │ 15,000원           │   │
│  │ 📍 서울시 종로구...            │   │
│  └──────────────────────────────────┘   │
│  ...                                     │
│  [Day 2] 2024.12.21 (토)                │
│  ...                                     │
└─────────────────────────────────────────┘
```

**기능**:
- **타임라인 뷰**: 시간순 카드 스크롤
- **지도 연동**: 각 장소 위치 표시
- **실시간 수정**: 카드 길게 눌러 수정 요청
- **공유**: 일정 PDF/이미지 내보내기

### 5.6 기술 구현 세부사항

#### Vector Store 구축
```python
# 관광지 데이터 임베딩 및 저장
from sentence_transformers import SentenceTransformer
from chromadb import Client

# 1. 임베딩 모델 로드
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. 관광지 설명 벡터화
for venue in tourist_data:
    description = f"{venue['name']} {venue['category']} {venue['description']}"
    embedding = model.encode(description)

    # 3. ChromaDB에 저장
    collection.add(
        ids=[venue['id']],
        embeddings=[embedding],
        metadatas=[venue],
        documents=[description]
    )

# 4. 검색 (사용자 입력과 유사도 계산)
query = "전통 한옥과 역사적인 궁궐"
results = collection.query(
    query_embeddings=model.encode(query),
    n_results=10
)
```

#### LangGraph 워크플로우 실행
```python
# Planner Agent 실행
from app.ai.agents.planner.graph import planner_graph

initial_state = {
    "messages": [{"role": "user", "content": user_input}],
    "user_preferences": {},
    "budget": 500000,
}

# 스트리밍 실행 (SSE 전송)
async for event in planner_graph.astream(initial_state):
    if event["type"] == "node_start":
        await sse_send({"node": event["node"], "status": "running"})
    elif event["type"] == "node_end":
        await sse_send({"node": event["node"], "result": event["result"]})

# 최종 결과
final_plan = event["final_plan"]
```

#### Naver Places API 통합
```python
import httpx

async def fetch_naver_place_info(venue_name: str) -> dict:
    """Naver API에서 최신 정보 가져오기"""
    url = "https://openapi.naver.com/v1/search/local.json"
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": venue_name, "display": 1}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        data = response.json()

    return {
        "address": data["items"][0]["roadAddress"],
        "phone": data["items"][0]["telephone"],
        "rating": data["items"][0].get("rating", "N/A"),
    }
```

---

## 6. 기대 효과

### 6.1 사용자 측면

#### 1) 시간 절감
- **기존**: 여행 계획 수립에 평균 5-10시간 소요
- **개선**: AI 대화로 10-15분 내 초안 완성
- **효과**: 90% 이상 시간 단축

#### 2) 개인화 경험
- 획일적 패키지 투어 탈피
- 개인 선호도, 체력, 예산 맞춤형 일정
- 과거 이력 학습으로 정확도 지속 향상

#### 3) 실시간 대응력
- 날씨 변화, 돌발 상황 즉시 대응
- 피로도, 컨디션 고려한 일정 조정
- 현지에서 발견한 새로운 장소 추가 가능

#### 4) 정보 신뢰성
- 공공 데이터 기반 정확한 정보
- 실시간 영업시간, 휴무일 확인
- AI 환각 최소화 (RAG 시스템)

### 6.2 비즈니스 측면

#### 1) 서울 관광 산업 활성화
- **연간 서울 방문 외국인**: 약 1,300만 명 (2023년 기준)
- **잠재 사용자**: 국내외 관광객 연간 2,000만 명
- **비주류 관광지 홍보**: AI 추천으로 숨은 명소 활성화

#### 2) 데이터 자산 축적
- 사용자 행동 패턴 분석
- 인기 장소, 코스 트렌드 파악
- 계절별, 연령별 선호도 데이터

#### 3) 수익 모델
- **프리미엄 기능**: 무제한 일정 수정, 우선 응답
- **제휴 수수료**: 숙박, 식당, 투어 예약 연계
- **광고 수익**: 관광지, 지역 상권 프로모션

#### 4) 확장 가능성
- **다른 도시 확대**: 부산, 제주, 경주 등
- **B2B 서비스**: 여행사, 호텔 제휴
- **해외 진출**: K-문화 관심 증가에 따른 글로벌 확장

### 6.3 기술적 측면

#### 1) AI 연구 기여
- Multi-Agent 시스템 실제 적용 사례
- RAG 시스템 최적화 노하우
- LLM 프롬프트 엔지니어링 베스트 프랙티스

#### 2) 오픈소스 기여
- LangGraph 활용 레퍼런스
- React Native + FastAPI 통합 패턴
- Vector DB 검색 최적화 기법

#### 3) 플랫폼 확장
- 크로스 플랫폼 지원 (iOS, Android, Web)
- 다국어 지원 (한국어, 영어, 중국어, 일본어)
- 음성 인터페이스 추가 가능 (STT/TTS)

### 6.4 사회적 측면

#### 1) 접근성 향상
- 언어 장벽 해소 (다국어 지원)
- 장애인 관광 지원 (휠체어 접근 가능 코스)
- 고령층 친화적 UI (큰 글씨, 음성 안내)

#### 2) 지역 경제 활성화
- 골목 상권 활성화 (로컬 맛집 추천)
- 비수기 관광 수요 창출 (계절별 테마 코스)
- 신규 관광 콘텐츠 발굴

#### 3) 환경 기여
- 효율적 경로 계획으로 탄소 배출 감소
- 대중교통 우선 추천
- 지속 가능한 관광 촉진

---

## 7. 향후 개발 로드맵

### Phase 1 (MVP - 현재)
- ✅ Planner Agent 구현
- ✅ Reviewer Agent 구현
- ✅ Vector DB 관광지 검색
- ✅ Naver API 통합
- ✅ 채팅 UI 및 일정 뷰어

### Phase 2 (Q1 2025)
- 🔄 사용자 인증 및 계정 관리
- 🔄 계획 저장 및 편집 기능
- 🔄 지도 연동 (카카오맵/구글맵)
- 🔄 다국어 지원 (영어, 중국어)

### Phase 3 (Q2 2025)
- 📅 실시간 날씨 연동
- 📅 교통 혼잡도 반영
- 📅 숙박/식당 예약 연동
- 📅 SNS 공유 기능

### Phase 4 (Q3 2025)
- 📅 음성 인터페이스 (STT/TTS)
- 📅 AR 내비게이션
- 📅 커뮤니티 기능 (리뷰, 추천)
- 📅 프리미엄 구독 모델 출시

---

## 8. 결론

Seoul Travel Agent는 **최신 AI 기술(LLM, Multi-Agent, RAG)** 과 **신뢰할 수 있는 공공 데이터**를 결합하여, 서울을 방문하는 모든 여행자에게 **개인화된 맞춤형 여행 경험**을 제공하는 혁신적인 플랫폼입니다.

**두 가지 전문 AI 에이전트**(Planner, Reviewer)의 협업을 통해, 여행 전 계획부터 여행 중 실시간 가이드까지 **완벽한 여행 라이프사이클**을 지원합니다.

기술적 완성도와 사용자 경험을 모두 갖춘 본 서비스는, 서울 관광 산업의 디지털 전환을 선도하고, **AI 기반 여행 플래닝의 새로운 표준**이 될 것입니다.

---

**문서 버전**: 1.0
**작성일**: 2025년 1월
**기술 스택**: React Native + FastAPI + LangGraph + ChromaDB
**라이선스**: MIT
