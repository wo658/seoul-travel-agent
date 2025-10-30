# Seoul Travel Agent - Frontend

AI 기반 서울 여행 플래너 React Native 앱

## 🚀 빠른 시작

```bash
# 의존성 설치
npm install

# 개발 서버 시작
npm run dev

# 플랫폼별 실행
npm run android
npm run ios
npm run web
```

## 📁 프로젝트 구조

자세한 구조는 [README_STRUCTURE.md](./README_STRUCTURE.md)를 참고하세요.

```
src/
├── components/ui/     # react-native-reusables 기반 UI 컴포넌트
├── screens/           # 화면 컴포넌트
├── lib/               # 유틸리티 및 헬퍼
├── hooks/             # 커스텀 React 훅
├── services/          # API 서비스
├── navigation/        # 네비게이션 설정
└── assets/            # 정적 리소스
```

## 🎨 기술 스택

- **React Native** 0.81.5 + **Expo** ~54.0.20
- **TypeScript** 5.9.3
- **NativeWind** 4.2.1 - Tailwind CSS for React Native
- **react-native-reusables** - shadcn/ui for React Native
- **Lucide React Native** - 아이콘 시스템

## 🧩 UI 컴포넌트

react-native-reusables를 기반으로 한 재사용 가능한 컴포넌트:

```tsx
import { Button, Card, CardTitle, Input, Text } from '@/ui';
import { Sparkles } from '@/lib/icons';

<Card>
  <CardTitle>제목</CardTitle>
  <Input placeholder="입력하세요" />
  <Button variant="default" size="lg">
    <Text>제출</Text>
  </Button>
</Card>
```

## 🎯 핵심 기능

### 1. Tailwind CSS 단일 테마 시스템
모든 스타일은 `global.css`의 CSS 변수로 관리:
```css
:root {
  --primary: oklch(0.5854 0.2041 277.1173);
  --foreground: oklch(0.2795 0.0368 260.0310);
  /* ... */
}
```

### 2. Path Aliases
절대 경로 import 지원:
```tsx
import { Button } from '@/ui';
import { formatDate } from '@/lib/utils';
import { HomeScreen } from '@/screens/HomeScreen';
```

### 3. Slot Pattern
유연한 컴포넌트 합성:
```tsx
<Button asChild>
  <CustomPressable>클릭</CustomPressable>
</Button>
```

## 📚 문서

- [프로젝트 구조 상세](./README_STRUCTURE.md)
- [react-native-reusables 공식 문서](https://rnr-docs.vercel.app/)
- [shadcn/ui](https://ui.shadcn.com/)
- [NativeWind](https://www.nativewind.dev/)

## 🛠️ 개발 가이드

### 컴포넌트 추가
1. [react-native-reusables 문서](https://rnr-docs.vercel.app/)에서 코드 복사
2. `src/components/ui/` 에 파일 생성
3. Tailwind 클래스로 커스터마이징
4. `src/components/ui/index.ts`에 export 추가

### 스타일 커스터마이징
1. `global.css`에서 CSS 변수 수정
2. `tailwind.config.js`에서 Tailwind 설정 조정

## 🤝 기여

이슈와 PR은 언제나 환영합니다!

## 📝 라이센스

MIT License
