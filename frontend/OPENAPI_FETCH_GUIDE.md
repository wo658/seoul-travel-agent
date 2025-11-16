# OpenAPI-Fetch Integration Guide

이 프로젝트는 **openapi-fetch**를 사용하여 완전히 자동화된 타입 안전 API 클라이언트를 제공합니다.

## 개요

- ✅ **완전 자동 타입 추론**: OpenAPI 스키마에서 자동으로 타입 생성
- ✅ **제로 런타임 오버헤드**: 타입만 사용, 런타임 코드 최소화
- ✅ **단일 진실 원칙**: 백엔드 OpenAPI 스키마가 유일한 진실의 원천
- ✅ **IDE 자동완성**: 모든 엔드포인트와 파라미터에 대한 자동완성 지원

## 설치

```bash
npm install openapi-fetch
```

## 기본 사용법

### 1. API 클라이언트 (자동 생성)

`src/lib/api.ts`에 openapi-fetch 클라이언트가 설정되어 있습니다:

```typescript
import createClient from 'openapi-fetch';
import type { paths } from '@/types/api';

export const apiClient = createClient<paths>({
  baseUrl: 'http://localhost:8000',
});
```

### 2. 직접 사용 (고급)

필요한 경우 `apiClient`를 직접 사용할 수 있습니다:

```typescript
import { apiClient } from '@/lib/api';

// GET 요청 - 완전 자동 타입 추론
const { data, error } = await apiClient.GET('/api/plans/', {
  params: {
    query: { user_id: 1 },
  },
});

// data와 error가 자동으로 타입 추론됨!
if (error) {
  console.error('Error:', error);
} else {
  console.log('Plans:', data); // data는 TravelPlanResponse[] 타입
}
```

### 3. Wrapper 함수 사용 (권장)

대부분의 경우 미리 만들어진 wrapper 함수를 사용하세요:

```typescript
import { plansApi, aiPlansApi, authApi } from '@/lib/api';

// 플랜 목록 조회
const plans = await plansApi.list(userId);

// 플랜 생성
const newPlan = await aiPlansApi.generate({
  user_request: '3일 서울 여행',
  start_date: '2025-07-01',
  end_date: '2025-07-03',
  budget: 500000,
  interests: ['palace', 'food'],
});

// 플랜 수정
const updatedPlan = await plansApi.update(planId, {
  title: '수정된 제목',
  description: '수정된 설명',
});

// 플랜 삭제
await plansApi.delete(planId);
```

## API 모듈

### plansApi (플랜 CRUD)

```typescript
import { plansApi } from '@/lib/api';

// 목록 조회
const plans = await plansApi.list(userId);

// 단일 조회
const plan = await plansApi.get(planId, userId);

// 업데이트
const updated = await plansApi.update(planId, {
  title: '새 제목',
  description: '새 설명',
});

// 삭제
await plansApi.delete(planId);
```

### aiPlansApi (AI 기반 플랜 생성/리뷰)

```typescript
import { aiPlansApi } from '@/lib/api';

// 플랜 생성
const response = await aiPlansApi.generate(
  {
    user_request: '3일 서울 여행',
    start_date: '2025-07-01',
    end_date: '2025-07-03',
    budget: 500000,
    interests: ['palace', 'food'],
  },
  userId,      // 기본값: 1
  true         // save_to_db, 기본값: true
);

// 플랜 리뷰/수정
const reviewed = await aiPlansApi.review(
  '첫째 날에 카페 시간을 더 추가해주세요',
  originalPlan,
  0  // iteration, 기본값: 0
);
```

### authApi (인증)

```typescript
import { authApi } from '@/lib/api';

// 회원가입
const user = await authApi.register({
  email: 'user@example.com',
  password: 'password123',
  full_name: '홍길동',
});

// 로그인
const token = await authApi.login({
  email: 'user@example.com',
  password: 'password123',
});

// 현재 사용자 조회
const currentUser = await authApi.getCurrentUser();
```

## 타입 추론 예시

### 자동 타입 추론

```typescript
// ✅ 파라미터 타입 자동 추론
const { data, error } = await apiClient.POST('/api/ai/plans/generate', {
  params: {
    query: {
      user_id: 1,
      save_to_db: true,
    },
  },
  body: {
    user_request: '3일 서울 여행',
    start_date: '2025-07-01',
    end_date: '2025-07-03',
    budget: 500000,
    interests: ['palace', 'food'],
  },
});

// data는 자동으로 TravelPlanResponse 타입
// error는 자동으로 에러 타입
```

### 타입 에러 방지

```typescript
// ❌ 컴파일 에러: 필수 필드 누락
await apiClient.POST('/api/ai/plans/generate', {
  body: {
    user_request: '3일 서울 여행',
    // start_date 누락 → TypeScript 에러!
  },
});

// ❌ 컴파일 에러: 잘못된 타입
await apiClient.POST('/api/ai/plans/generate', {
  body: {
    user_request: '3일 서울 여행',
    start_date: '2025-07-01',
    end_date: '2025-07-03',
    budget: '500000', // ❌ string이 아닌 number여야 함
    interests: ['palace', 'food'],
  },
});
```

## 컴포넌트에서 사용하기

### 예시: 플랜 목록 화면

```typescript
import { useState, useEffect } from 'react';
import { plansApi } from '@/lib/api';

export function MyPlansScreen() {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadPlans = async () => {
      try {
        const data = await plansApi.list(1);
        setPlans(data); // 타입 안전!
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    loadPlans();
  }, []);

  // ...
}
```

### 예시: 플랜 생성

```typescript
import { aiPlansApi } from '@/lib/api';

export function PlanForm() {
  const handleSubmit = async (formData) => {
    try {
      const response = await aiPlansApi.generate({
        user_request: formData.request,
        start_date: formData.startDate,
        end_date: formData.endDate,
        budget: formData.budget,
        interests: formData.interests,
      });

      console.log('Generated plan:', response.plan);
      // response.plan은 자동으로 타입 추론됨
    } catch (error) {
      console.error('Failed to generate plan:', error);
    }
  };

  // ...
}
```

## 에러 처리

openapi-fetch는 에러를 throw하지 않고 `{ data, error }` 형태로 반환합니다:

```typescript
const { data, error } = await apiClient.GET('/api/plans/');

if (error) {
  // 에러 처리
  console.error('Error:', error);
  return;
}

// 성공 - data 사용
console.log('Plans:', data);
```

Wrapper 함수에서는 에러를 throw합니다:

```typescript
try {
  const plans = await plansApi.list(1);
  console.log('Plans:', plans);
} catch (error) {
  console.error('Failed to fetch plans:', error);
}
```

## 백엔드 API 변경 시 워크플로우

1. **백엔드 스키마 수정**
   ```python
   # backend/app/ai/ai_schemas.py
   class GenerateTravelPlanRequest(BaseModel):
       user_request: str
       new_field: str  # 새 필드 추가
   ```

2. **타입 재생성**
   ```bash
   cd frontend
   npm run types:generate
   ```

3. **TypeScript 컴파일러가 자동으로 에러 표시**
   - 누락된 필드가 있으면 컴파일 에러 발생
   - IDE에서 즉시 확인 가능

4. **코드 수정**
   ```typescript
   // TypeScript가 new_field가 필요하다고 알려줌
   await aiPlansApi.generate({
     user_request: '3일 서울 여행',
     new_field: '새 값', // IDE 자동완성으로 추가
     // ...
   });
   ```

## 장점

### 1. 완전 자동 타입 추론
- 모든 요청/응답 타입이 자동으로 추론됨
- 수동 타입 정의 불필요

### 2. 컴파일 타임 안전성
- API 변경사항이 즉시 TypeScript 에러로 표시
- 런타임 에러 방지

### 3. IDE 지원
- 자동완성으로 빠른 개발
- 파라미터 힌트 제공
- 타입 호버 정보

### 4. 유지보수성
- 백엔드 변경 시 영향받는 코드를 쉽게 파악
- 리팩토링 시 안전성 보장

## 고급 사용법

### 커스텀 Fetch 옵션

```typescript
const client = createClient<paths>({
  baseUrl: API_BASE_URL,
  headers: {
    'Custom-Header': 'value',
  },
});

// 또는 요청마다 설정
const { data } = await apiClient.GET('/api/plans/', {
  params: { query: { user_id: 1 } },
  headers: {
    'Authorization': `Bearer ${token}`,
  },
});
```

### Middleware 추가

```typescript
import createClient from 'openapi-fetch';
import type { paths } from '@/types/api';

const client = createClient<paths>({ baseUrl: API_BASE_URL });

// Request middleware
client.use({
  async onRequest({ request }) {
    const token = await getToken();
    if (token) {
      request.headers.set('Authorization', `Bearer ${token}`);
    }
    return request;
  },
  async onResponse({ response }) {
    // 응답 로깅
    console.log('Response:', response.status);
    return response;
  },
});
```

## 참고 자료

- [openapi-fetch 공식 문서](https://openapi-ts.pages.dev/openapi-fetch/)
- [OpenAPI TypeScript 문서](https://openapi-ts.pages.dev/)
- [프로젝트 타입 생성 가이드](./TYPE_GENERATION.md)
