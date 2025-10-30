# Seoul Travel Agent - Frontend Structure

## 프로젝트 구조

```
frontend/
├── src/
│   ├── components/
│   │   └── ui/                    # react-native-reusables 기반 컴포넌트
│   │       ├── button.tsx         # Button (with Slot pattern)
│   │       ├── card.tsx           # Card components
│   │       ├── input.tsx          # Input component
│   │       ├── text.tsx           # Text wrapper
│   │       ├── separator.tsx      # Separator
│   │       └── index.ts           # UI 컴포넌트 export
│   ├── screens/
│   │   └── HomeScreen.tsx         # 메인 화면
│   ├── hooks/                     # 커스텀 React 훅
│   ├── lib/
│   │   ├── utils.ts               # 유틸리티 함수 (cn, formatDate 등)
│   │   └── icons/
│   │       └── index.ts           # Lucide icons export
│   ├── services/                  # API 서비스
│   ├── utils/                     # 헬퍼 함수
│   ├── constants/                 # 상수
│   ├── types/                     # TypeScript 타입 정의
│   ├── navigation/                # 네비게이션 설정
│   └── assets/
│       ├── fonts/
│       ├── images/
│       └── icons/
├── App.tsx                        # 앱 진입점
├── index.tsx                      # Root 파일
├── global.css                     # Tailwind CSS + CSS 변수 (단일 진실 원천)
├── tailwind.config.ts             # Tailwind 설정
├── babel.config.ts                # Babel + path aliases 설정
└── tsconfig.json                  # TypeScript 설정
```

## UI 컴포넌트 시스템

### react-native-reusables 기반
**shadcn/ui의 React Native 구현체**

react-native-reusables는 shadcn/ui의 철학을 React Native에 그대로 적용한 라이브러리입니다:

- ✅ **컴포넌트 복사**: npm으로 설치하는 것이 아니라 코드를 복사
- ✅ **@rn-primitives 활용**: Radix UI의 React Native 버전
- ✅ **Slot 패턴**: 유연한 컴포넌트 합성
- ✅ **Tailwind CSS 단일 테마**: global.css의 CSS 변수만 사용
- ✅ **타입 안전성**: TypeScript + CVA (class-variance-authority)
- ✅ **제로 런타임 오버헤드**: CSS-in-JS 없음

### 핵심 개념

#### 1. Slot Pattern (@rn-primitives/slot)
```tsx
<Button asChild>
  <CustomPressable>Click me</CustomPressable>
</Button>
```
`asChild` prop으로 Button의 스타일을 다른 컴포넌트에 적용 가능

#### 2. CVA (Class Variance Authority)
```tsx
const buttonVariants = cva(
  'group flex items-center justify-center rounded-md',
  {
    variants: {
      variant: {
        default: 'bg-primary',
        outline: 'border border-input',
      },
      size: {
        default: 'h-10 px-4',
        lg: 'h-11 px-8',
      },
    },
  }
);
```

#### 3. Web/Native 조건부 스타일
```tsx
'web:hover:opacity-90 native:h-12'
```
웹과 네이티브에서 다른 스타일 적용 가능

### 사용 예제

```tsx
import { Button, buttonTextVariants, Card, Text } from '@/ui';
import { Sparkles } from '@/lib/icons';

function MyScreen() {
  return (
    <Card>
      <Button variant="default" size="lg">
        <View className="flex-row items-center gap-2">
          <Sparkles size={16} />
          <Text className={buttonTextVariants({ variant: 'default', size: 'lg' })}>
            시작하기
          </Text>
        </View>
      </Button>
    </Card>
  );
}
```

## Path Aliases

TypeScript와 Babel 모두 설정 완료:

- `@/*` → `src/*`
- `@/ui/*` → `src/components/ui/*`
- `@/screens/*` → `src/screens/*`
- `@/lib/icons` → `src/lib/icons/index.ts`
- 기타 등등...

## 테마 관리

### 단일 진실 원천: global.css

모든 디자인 토큰은 `global.css`에서 관리:

```css
:root {
  --primary: oklch(0.5854 0.2041 277.1173);
  --foreground: oklch(0.2795 0.0368 260.0310);
  --background: oklch(0.9232 0.0026 48.7171);
  /* ... */
}

.dark {
  --primary: oklch(0.6801 0.1583 276.9349);
  /* ... */
}
```

Tailwind에서 CSS 변수 참조:

```ts
// tailwind.config.ts
colors: {
  primary: 'var(--color-primary)',
  foreground: 'var(--color-foreground)',
  background: 'var(--color-background)',
}
```

## 기술 스택

- **React Native** 0.81.5
- **Expo** ~54.0.20
- **TypeScript** 5.9.3
- **NativeWind** 4.2.1 - Tailwind CSS for React Native
- **Tailwind CSS** 3.4.18 - 단일 스타일 시스템
- **@rn-primitives** - Radix UI for React Native
- **CVA** - Variant 관리
- **CLSX** - 클래스명 조합
- **Lucide React Native** - 아이콘 시스템

## 컴포넌트 추가 방법

react-native-reusables에서 제공하는 컴포넌트를 추가하려면:

1. 공식 문서에서 컴포넌트 코드 복사: https://rnr-docs.vercel.app/
2. `src/components/ui/` 에 파일 생성
3. 필요한 @rn-primitives 패키지 설치
4. Tailwind CSS 클래스로 커스터마이징
5. `src/components/ui/index.ts` 에 export 추가

예: Badge 컴포넌트 추가
```tsx
// src/components/ui/badge.tsx
import { View, Text } from 'react-native';
import { cva } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const badgeVariants = cva(
  'flex-row items-center rounded-full px-2.5 py-0.5',
  {
    variants: {
      variant: {
        default: 'bg-primary',
        secondary: 'bg-secondary',
      },
    },
  }
);

export function Badge({ children, variant, className }) {
  return (
    <View className={cn(badgeVariants({ variant }), className)}>
      <Text className="text-xs font-semibold">{children}</Text>
    </View>
  );
}
```

## 아이콘 사용법

Lucide React Native 아이콘:

```tsx
import { Sparkles, Calendar, MapPin } from '@/lib/icons';

<Sparkles className="text-primary" size={20} />
<Calendar size={24} color="#000" />
```

## 개발 시작

```bash
npm run dev
```

## 왜 react-native-reusables인가?

1. **shadcn/ui 철학**: 컴포넌트를 복사해서 사용, 완전한 제어
2. **단일 진실 원천**: CSS 변수 한 곳에서만 테마 관리
3. **Radix UI 기반**: 접근성과 키보드 네비게이션 내장
4. **확장 용이**: 필요한 컴포넌트만 추가
5. **성능**: CSS-in-JS 없이 순수 Tailwind
6. **커뮤니티**: shadcn/ui와 동일한 API, 문서 풍부

## 참고 자료

- [react-native-reusables 공식 문서](https://rnr-docs.vercel.app/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Radix UI](https://www.radix-ui.com/)
- [NativeWind](https://www.nativewind.dev/)
- [Lucide Icons](https://lucide.dev/)
