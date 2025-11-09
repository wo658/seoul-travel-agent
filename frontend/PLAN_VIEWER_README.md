# 여행 계획 뷰어/편집기 UI/UX 설계

SEO-41 구현: 타임라인 카드 뷰 + 채팅 하이브리드 인터페이스

## 개요

여행 계획을 효과적으로 표시하고, 사용자가 직관적으로 편집하며, AI와 대화를 통해 수정할 수 있는 하이브리드 인터페이스입니다.

## 주요 기능

### 1. 타임라인 카드 뷰 (메인)
- **일별 섹션**: 접기/펼치기 가능한 일별 카드
- **활동 카드**: 드래그 가능한 개별 활동 카드
- **제스처 지원**:
  - 롱프레스로 활동 선택
  - 카드 내 버튼으로 수정/삭제
  - 애니메이션 피드백

### 2. 채팅 인터페이스 (보조)
- **바텀시트**: 플로팅 버튼으로 열리는 채팅 UI
- **AI 대화**: Reviewer Agent와 대화형 계획 수정
- **빠른 제안**: 미리 정의된 수정 제안 버튼
- **실시간 반영**: 수정사항이 타임라인에 즉시 반영

### 3. 모바일 최적화
- **React Native + NativeWind**: 네이티브 성능 + Tailwind 스타일링
- **Reanimated 애니메이션**: 부드러운 인터랙션
- **반응형 디자인**: 다양한 화면 크기 지원

## 컴포넌트 구조

```
src/
├── types/
│   └── plan-viewer.ts              # 확장된 타입 정의
├── components/travel/
│   ├── DraggableActivityCard.tsx   # 드래그 가능한 활동 카드
│   ├── DraggableDayTimeline.tsx    # 일별 타임라인 (접기/펼치기)
│   └── PlanChatSheet.tsx           # 채팅 바텀시트
└── screens/
    └── PlanViewerScreen.tsx        # 메인 하이브리드 스크린
```

## 타입 정의

### EditableActivity
```typescript
interface EditableActivity extends Activity {
  id: string;              // 고유 ID (드래그앤드롭용)
  is_custom: boolean;      // 사용자 직접 추가 여부
  is_locked: boolean;      // 수정 잠금 여부
  alternatives?: VenueAlternative[]; // AI 추천 대안
}
```

### EditableDayItinerary
```typescript
interface EditableDayItinerary extends Omit<DayItinerary, 'activities'> {
  activities: EditableActivity[];
  is_expanded: boolean;    // 접기/펼치기 상태
}
```

### PlanChatMessage
```typescript
interface PlanChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  plan_snapshot?: TravelPlan; // 해당 시점의 계획 스냅샷
}
```

## 사용 방법

### 기본 사용
```typescript
import { PlanViewerScreen } from '@/screens';
import { TravelPlan } from '@/types';

function MyComponent() {
  const [plan, setPlan] = useState<TravelPlan>(...);

  return (
    <PlanViewerScreen
      plan={plan}
      onBack={() => navigation.goBack()}
      onSave={(updatedPlan) => {
        setPlan(updatedPlan);
        // 서버에 저장
      }}
    />
  );
}
```

### 활동 카드 커스터마이징
```typescript
<DraggableActivityCard
  activity={activity}
  onPress={() => console.log('Tapped')}
  onLongPress={() => console.log('Long pressed')}
  onSwipeDelete={() => handleDelete()}
  onEdit={() => handleEdit()}
  isDragging={false}
/>
```

### 채팅 인터페이스
```typescript
<PlanChatSheet
  visible={chatVisible}
  onClose={() => setChatVisible(false)}
  messages={chatMessages}
  isLoading={isModifying}
  onSendMessage={(message) => {
    // AI에게 메시지 전송
    handleModifyPlan(message);
  }}
  suggestions={[
    { id: '1', label: '예산 줄이기', prompt: '전체 예산을 20% 줄여주세요' }
  ]}
/>
```

## 주요 인터랙션

### 1. 활동 수정
- **버튼 탭**: 활동 카드의 "수정" 버튼 탭
- **동작**: 활동 편집 모달 표시 (추후 구현)

### 2. 활동 삭제
- **버튼 탭**: 활동 카드의 "삭제" 버튼 탭
- **동작**: 확인 Alert → 삭제 → 예산 재계산

### 3. 활동 추가
- **버튼 탭**: 일별 카드의 "활동 추가" 버튼
- **동작**: 활동 추가 모달 표시 (추후 구현)

### 4. AI 대화 수정
- **플로팅 버튼**: 화면 우하단 메시지 아이콘
- **동작**: 채팅 바텀시트 표시 → 메시지 입력/제안 선택 → API 호출 → 계획 업데이트

### 5. 일별 접기/펼치기
- **헤더 탭**: Day 카드 헤더 영역 탭
- **동작**: 애니메이션과 함께 활동 리스트 표시/숨김

## 애니메이션

### 활동 카드
- **탭 피드백**: 0.98 스케일 축소
- **드래깅**: 1.05 스케일 확대 + 0.7 투명도

### 채팅 바텀시트
- **슬라이드 업**: Spring 애니메이션 (damping: 20, stiffness: 90)
- **백드롭**: Fade 애니메이션 (duration: 200ms)

### 일별 접기/펼치기
- **레이아웃**: easeInEaseOut 프리셋

## 필수 패키지

현재 설치된 패키지:
- ✅ `react-native-reanimated`: ^4.1.3
- ✅ `nativewind`: ^4.2.1
- ✅ `lucide-react-native`: ^0.548.0

추가 필요한 패키지 (선택):
- `react-native-gesture-handler` (고급 드래그앤드롭용)
- `react-native-draggable-flatlist` (리스트 재정렬용)

## 스타일링

### Tailwind 클래스 사용
```tsx
<View className="flex-1 bg-background p-4 gap-4">
  <Card className="border-2 border-transparent active:border-primary">
    <Text className="text-lg font-bold text-foreground">
      제목
    </Text>
  </Card>
</View>
```

### 커스텀 색상
프로젝트의 Tailwind 설정에 정의된 색상 사용:
- `primary`: 메인 액션 색상
- `secondary`: 보조 색상
- `muted`: 비활성/배경 색상
- `destructive`: 삭제/경고 색상
- `foreground`: 텍스트 색상
- `background`: 배경 색상

## 향후 개선사항

### Phase 1 (현재)
- ✅ 타임라인 카드 뷰
- ✅ 기본 활동 카드 (수정/삭제 버튼)
- ✅ 채팅 바텀시트
- ✅ 일별 접기/펼치기
- ✅ AI 대화형 수정

### Phase 2 (추후)
- [ ] 실제 드래그앤드롭 재정렬
- [ ] 활동 편집 모달
- [ ] 활동 추가 모달
- [ ] 대안 장소 제안 UI
- [ ] 오프라인 지원

### Phase 3 (고급)
- [ ] 지도 통합 (위치 시각화)
- [ ] 루트 최적화 시각화
- [ ] 협업 편집 (실시간 공유)
- [ ] 히스토리 및 되돌리기

## API 연동

### 계획 수정 API
```typescript
// src/services/api/chat.ts
export async function modifyPlan(request: ModifyPlanRequest): Promise<ModifyPlanResponse> {
  const response = await fetch('/api/ai/plans/review', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  return response.json();
}
```

### 필요한 엔드포인트
- `POST /api/ai/plans/review`: Reviewer Agent를 통한 계획 수정
- `PATCH /api/plans/:id/activities/:aid`: 개별 활동 수정
- `DELETE /api/plans/:id/activities/:aid`: 활동 삭제
- `POST /api/plans/:id/activities`: 활동 추가

## 접근성

- **시맨틱 마크업**: 올바른 컴포넌트 사용
- **포커스 관리**: 키보드 네비게이션 지원
- **색상 대비**: WCAG AA 준수
- **터치 타겟**: 최소 44x44 크기

## 성능 최적화

- **useCallback**: 이벤트 핸들러 메모이제이션
- **React.memo**: 불필요한 리렌더링 방지 (필요시 적용)
- **LayoutAnimation**: 네이티브 레이아웃 애니메이션 사용
- **Reanimated**: UI 스레드에서 실행되는 애니메이션

## 문제 해결

### 애니메이션이 작동하지 않음
- Android: `UIManager.setLayoutAnimationEnabledExperimental(true)` 확인
- iOS: 일반적으로 문제 없음

### 채팅 바텀시트가 키보드에 가려짐
- `KeyboardAvoidingView` 사용 확인
- `behavior="padding"` (iOS) / `undefined` (Android)

### 타입 에러
- `types/plan-viewer.ts` import 확인
- `types/index.ts`에서 re-export 확인

## 참고 자료

- [React Native Reanimated](https://docs.swmansion.com/react-native-reanimated/)
- [NativeWind](https://www.nativewind.dev/)
- [Lucide React Native](https://lucide.dev/guide/packages/lucide-react-native)
- [UI/UX 설계 문서](SEO-41 Linear 이슈 참고)
