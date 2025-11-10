# Type Generation Guide

이 프로젝트는 백엔드의 OpenAPI 스키마를 사용하여 프론트엔드 TypeScript 타입을 자동 생성합니다.
이를 통해 **단일 진실 원칙(Single Source of Truth)**을 준수합니다.

## 개요

- 백엔드: FastAPI (Python)
  - OpenAPI 스키마 자동 생성: `/api/openapi.json`
- 프론트엔드: React Native + TypeScript
  - `openapi-typescript`를 사용하여 타입 자동 생성

## 타입 생성 방법

### 1. 백엔드 서버 실행

먼저 백엔드 서버가 실행 중이어야 합니다:

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### 2. 프론트엔드 타입 생성

프론트엔드 디렉토리에서 다음 명령어를 실행합니다:

```bash
cd frontend
npm run types:generate
```

이 명령어는:
- `http://localhost:8000/api/openapi.json`에서 OpenAPI 스키마를 가져옵니다
- `src/types/api.d.ts` 파일에 TypeScript 타입을 생성합니다

### 3. Watch 모드 (개발 중)

백엔드 API를 개발하면서 타입을 자동으로 업데이트하려면:

```bash
npm run types:watch
```

## 사용 방법

### 생성된 타입 import

```typescript
import type { components, operations } from '@/types/api';

// 컴포넌트 스키마 사용
type UserCreate = components['schemas']['UserCreate'];
type GeneratePlanRequest = components['schemas']['GenerateTravelPlanRequest'];

// Operation 타입 사용 (요청/응답)
type GeneratePlanOp = operations['generate_travel_plan_api_ai_plans_generate_post'];
```

### 타입 별칭 정의 (src/types/index.ts)

생성된 타입을 더 사용하기 쉽게 별칭을 정의합니다:

```typescript
// src/types/index.ts
import type { components } from './api';

export type GenerateTravelPlanRequest = components['schemas']['GenerateTravelPlanRequest'];
export type PlanFormData = GenerateTravelPlanRequest; // 별칭

// 컴포넌트에서 사용
import { PlanFormData } from '@/types';
```

## 타입 구조

### API Request/Response 타입

백엔드 OpenAPI 스키마에서 자동 생성되는 타입:

- **Travel Plan Generation**
  - `GenerateTravelPlanRequest`: 여행 계획 생성 요청
  - `TravelPlanApiResponse`: 여행 계획 응답
  - `ReviewTravelPlanRequest`: 여행 계획 리뷰/수정 요청

- **Authentication**
  - `UserCreate`: 사용자 생성
  - `UserLogin`: 로그인
  - `Token`: 인증 토큰
  - `UserResponse`: 사용자 정보

- **Plan CRUD**
  - `TravelPlanCreate`: 여행 계획 생성
  - `TravelPlanUpdate`: 여행 계획 업데이트
  - `PlanResponse`: 저장된 여행 계획 응답

### Frontend-specific 타입

프론트엔드에서만 사용하는 타입 (src/types/index.ts):

```typescript
export interface Activity {
  time: string;
  venue_name: string;
  venue_type: 'attraction' | 'restaurant' | 'accommodation' | 'cafe' | 'shopping';
  duration_minutes: number;
  cost: number;
  description: string;
  tips?: string;
  location?: {
    lat: number;
    lng: number;
    address: string;
  };
}

export interface DayItinerary {
  day: number;
  date: string;
  theme: string;
  activities: Activity[];
  daily_cost: number;
}

export interface TravelPlan {
  id?: string;
  title: string;
  total_days: number;
  total_cost: number;
  days: DayItinerary[];
  accommodation?: Accommodation;
  tips?: string[];
  created_at?: string;
}
```

## 백엔드 스키마 수정 시 워크플로우

1. **백엔드 스키마 수정**
   ```python
   # backend/app/ai/ai_schemas.py
   class GenerateTravelPlanRequest(BaseModel):
       user_request: str
       start_date: str
       end_date: str
       budget: Optional[int] = None  # 필드 추가/수정
       interests: list[str] = []
   ```

2. **타입 재생성**
   ```bash
   cd frontend
   npm run types:generate
   ```

3. **프론트엔드 코드 업데이트**
   - TypeScript 컴파일러가 타입 에러를 표시
   - 필요한 부분 수정

## 장점

### 1. 단일 진실 원칙 (Single Source of Truth)
- 백엔드 API 스키마가 유일한 진실의 원천
- 프론트엔드 타입은 자동으로 동기화

### 2. 타입 안정성
- API 변경 사항이 즉시 TypeScript 타입에 반영
- 컴파일 타임에 타입 불일치 감지

### 3. 개발 효율성
- API 문서와 타입이 항상 일치
- 수동 타입 관리 불필요
- IDE 자동완성 지원

### 4. 유지보수성
- API 변경 시 영향받는 코드를 쉽게 파악
- 리팩토링 시 안전성 보장

## 주의사항

### DO ✅

- 백엔드 API 스키마 수정 후 반드시 타입 재생성
- 생성된 `api.d.ts` 파일은 절대 직접 수정하지 않기
- `src/types/index.ts`에서 타입 별칭 정의하여 사용

### DON'T ❌

- `api.d.ts` 파일 직접 수정 (자동 생성됨)
- 백엔드와 다른 타입 수동으로 정의
- 생성된 타입 무시하고 `any` 사용

## 파일 구조

```
frontend/
├── package.json              # types:generate, types:watch 스크립트
├── src/
│   ├── types/
│   │   ├── api.d.ts         # 🤖 자동 생성 (수정 금지!)
│   │   ├── index.ts         # 타입 별칭 및 프론트엔드 전용 타입
│   │   ├── plan-viewer.ts   # 플랜 뷰어 관련 타입
│   │   └── planner-api.ts   # Planner Agent API 타입
│   └── ...
└── TYPE_GENERATION.md        # 이 문서
```

## 트러블슈팅

### 타입 생성 실패

**문제**: `npm run types:generate` 실행 시 에러

**해결**:
1. 백엔드 서버가 실행 중인지 확인: `curl http://localhost:8000/api/openapi.json`
2. 백엔드 스키마에 문법 오류가 없는지 확인
3. 백엔드 서버 재시작

### 타입 불일치

**문제**: 프론트엔드 코드에서 타입 에러 발생

**해결**:
1. 최신 스키마로 타입 재생성: `npm run types:generate`
2. 프론트엔드 코드를 새로운 타입에 맞게 수정
3. `null` vs `undefined` 확인 (OpenAPI는 주로 `null` 사용)

### 백엔드 서버 연결 실패

**문제**: ECONNREFUSED 에러

**해결**:
1. 백엔드 서버 실행 여부 확인
2. 포트 번호 확인 (8000)
3. package.json의 URL 확인

## 참고 자료

- [openapi-typescript 문서](https://openapi-ts.pages.dev/)
- [FastAPI OpenAPI 문서](https://fastapi.tiangolo.com/tutorial/metadata/)
- [TypeScript 타입 정의](https://www.typescriptlang.org/docs/handbook/2/types-from-types.html)
