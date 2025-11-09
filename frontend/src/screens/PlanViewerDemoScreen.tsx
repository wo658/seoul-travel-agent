import React from 'react';
import { View, ScrollView, Pressable, Alert } from 'react-native';
import { Text, Button } from '@/components/ui';
import { PlanViewerScreen } from './PlanViewerScreen';
import { TravelPlan, PlannerResponse } from '@/types';
import { mapPlannerResponseToTravelPlan } from '@/lib/utils/plan-mapper';
import { ArrowLeft } from '@/lib/icons';

/**
 * PlanViewerScreen 테스트용 데모 화면
 * 실제 Planner Agent 응답 형식의 목 데이터를 사용합니다.
 */

// Mock Planner Agent Response (실제 백엔드 응답 형식)
const MOCK_PLANNER_RESPONSE: PlannerResponse = {
  type: 'complete',
  plan: {
    title: '역사와 맛집으로 채운 서울 3일 가이드 (2025-12-01 ~ 2025-12-03)',
    total_days: 3,
    total_cost: 292000,
    itinerary: [
      {
        day: 1,
        date: '2025-12-01',
        theme: '전통문화와 현대 맛집의 만남',
        activities: [
          {
            time: '10:00',
            venue_name: '경복궁',
            venue_type: 'attraction',
            duration_minutes: 120,
            estimated_cost: 3000,
            notes:
              '조선시대 법궁으로, 근정전과 경회루가 유명합니다. 수문장 교대식은 10시, 14시에 진행됩니다.',
          },
          {
            time: '12:15',
            venue_name: '광장시장',
            venue_type: 'restaurant',
            duration_minutes: 90,
            estimated_cost: 15000,
            notes:
              '전통 한식과 길거리 음식을 맛볼 수 있는 전통시장입니다. 빈대떡과 마약김밥이 유명해요.',
          },
          {
            time: '14:00',
            venue_name: '창덕궁 후원',
            venue_type: 'attraction',
            duration_minutes: 150,
            estimated_cost: 8000,
            notes:
              '유네스코 세계문화유산으로 지정된 아름다운 정원입니다. 후원은 예약 필수입니다.',
          },
          {
            time: '17:45',
            venue_name: '북촌한옥마을',
            venue_type: 'attraction',
            duration_minutes: 90,
            estimated_cost: 0,
            notes:
              '전통 한옥이 밀집된 지역으로 야경이 아름답습니다. 주민들이 거주하므로 조용히 관람해주세요.',
          },
          {
            time: '19:30',
            venue_name: '삼계탕 전문점',
            venue_type: 'restaurant',
            duration_minutes: 60,
            estimated_cost: 18000,
            notes: '신선한 재료로 만든 전통 삼계탕 전문점입니다.',
          },
        ],
        daily_cost: 44000,
      },
      {
        day: 2,
        date: '2025-12-02',
        theme: '현대 서울 체험',
        activities: [
          {
            time: '10:00',
            venue_name: '남산타워',
            venue_type: 'attraction',
            duration_minutes: 120,
            estimated_cost: 16000,
            notes:
              '서울의 랜드마크로 전망대에서 도시 전경을 볼 수 있습니다. 일몰 시간대가 가장 아름답습니다.',
          },
          {
            time: '13:00',
            venue_name: '명동 먹자골목',
            venue_type: 'restaurant',
            duration_minutes: 90,
            estimated_cost: 25000,
            notes:
              '다양한 한식과 세계 음식을 즐길 수 있는 번화가입니다. 주말은 매우 붐빕니다.',
          },
          {
            time: '15:30',
            venue_name: '동대문 디자인 플라자',
            venue_type: 'attraction',
            duration_minutes: 120,
            estimated_cost: 0,
            notes:
              '자하 하디드가 설계한 현대적인 건축물로 전시와 쇼핑을 즐길 수 있습니다. 야경이 아름답습니다.',
          },
          {
            time: '18:00',
            venue_name: '광장동 카페거리',
            venue_type: 'cafe',
            duration_minutes: 90,
            estimated_cost: 12000,
            notes:
              '트렌디한 카페들이 모여있는 핫플레이스입니다. 인스타그램 감성 카페들이 많아요.',
          },
          {
            time: '20:00',
            venue_name: '한강 야경 크루즈',
            venue_type: 'attraction',
            duration_minutes: 90,
            estimated_cost: 35000,
            notes:
              '한강의 야경을 유람선에서 감상할 수 있습니다. 예약 필수! 석식 포함 패키지도 있어요.',
          },
        ],
        daily_cost: 88000,
      },
      {
        day: 3,
        date: '2025-12-03',
        theme: '문화와 쇼핑',
        activities: [
          {
            time: '10:00',
            venue_name: '국립중앙박물관',
            venue_type: 'attraction',
            duration_minutes: 150,
            estimated_cost: 0,
            notes:
              '한국의 역사와 문화를 한눈에 볼 수 있는 국립박물관입니다. 입장료 무료!',
          },
          {
            time: '13:30',
            venue_name: '이태원 세계음식거리',
            venue_type: 'restaurant',
            duration_minutes: 90,
            estimated_cost: 30000,
            notes:
              '전세계 다양한 음식을 맛볼 수 있는 국제적인 거리입니다. 멕시칸, 터키, 인도 음식이 유명해요.',
          },
          {
            time: '16:00',
            venue_name: '코엑스몰',
            venue_type: 'shopping',
            duration_minutes: 180,
            estimated_cost: 50000,
            notes:
              '대형 쇼핑몰로 별마당 도서관이 유명합니다. 별마당 도서관은 인생샷 명소!',
          },
          {
            time: '19:30',
            venue_name: '강남 맛집 투어',
            venue_type: 'restaurant',
            duration_minutes: 90,
            estimated_cost: 40000,
            notes:
              '강남의 유명 맛집에서 저녁 식사를 즐깁니다. 예약 추천! 대기 시간이 길 수 있어요.',
          },
        ],
        daily_cost: 120000,
      },
    ],
    accommodation: {
      name: 'JW 메리어트 호텔 서울',
      cost_per_night: 110000,
      total_nights: 2,
    },
    summary:
      '3일간 서울의 역사적 분위기와 전통문화, 그리고 맛집을 조화롭게 체험하는 일정입니다. 첫날은 경복궁과 창덕궁을 중심으로 조선시대 궁궐 탐방을, 둘째날은 남산타워와 DDP를 통해 현대 서울을 체험하고, 셋째날은 국립중앙박물관과 코엑스몰로 문화와 쇼핑을 마무리합니다. 예산은 약 29만원으로 잡았고, 숙박은 2박 기준으로 구성했습니다.',
  },
};

interface PlanViewerDemoScreenProps {
  onBack?: () => void;
}

export function PlanViewerDemoScreen({ onBack }: PlanViewerDemoScreenProps) {
  const [showDemo, setShowDemo] = React.useState(false);
  const [travelPlan, setTravelPlan] = React.useState<TravelPlan | null>(null);

  React.useEffect(() => {
    // Planner 응답을 TravelPlan으로 변환
    try {
      const plan = mapPlannerResponseToTravelPlan(MOCK_PLANNER_RESPONSE);
      setTravelPlan(plan);
    } catch (error) {
      console.error('Failed to map planner response:', error);
    }
  }, []);

  if (showDemo && travelPlan) {
    return (
      <PlanViewerScreen
        plan={travelPlan}
        onBack={() => setShowDemo(false)}
        onSave={(updatedPlan) => {
          console.log('Plan saved:', updatedPlan);
          Alert.alert('저장 완료', '계획이 저장되었습니다!');
        }}
      />
    );
  }

  if (!travelPlan) {
    return (
      <View className="flex-1 bg-background items-center justify-center">
        <Text className="text-base text-muted-foreground">
          목 데이터를 로딩하는 중...
        </Text>
      </View>
    );
  }

  return (
    <View className="flex-1 bg-background">
      {/* Header */}
      <View className="bg-card border-b border-border px-4 py-3 flex flex-row items-center justify-between">
        {onBack && (
          <Pressable onPress={onBack} className="p-2 -m-2">
            <ArrowLeft size={24} className="text-foreground" />
          </Pressable>
        )}
        <Text className="text-lg font-semibold text-foreground">
          Plan Viewer 데모
        </Text>
        <View className="w-10" />
      </View>

      {/* Content */}
      <ScrollView className="flex-1 p-4">
        <View className="gap-6">
          {/* Introduction */}
          <View className="gap-2">
            <Text className="text-2xl font-bold text-foreground">
              여행 계획 뷰어 테스트
            </Text>
            <Text className="text-base text-muted-foreground leading-6">
              타임라인 카드 뷰 + 채팅 하이브리드 인터페이스를 테스트해보세요.
            </Text>
          </View>

          {/* Mock Data Info */}
          <View className="bg-card rounded-lg p-4 gap-3">
            <Text className="text-lg font-semibold text-foreground">
              목 데이터 정보
            </Text>
            <View className="gap-2">
              <View className="flex flex-row gap-2">
                <Text className="text-sm text-muted-foreground">제목:</Text>
                <Text className="text-sm font-medium text-foreground flex-1">
                  {travelPlan.title}
                </Text>
              </View>
              <View className="flex flex-row gap-2">
                <Text className="text-sm text-muted-foreground">기간:</Text>
                <Text className="text-sm font-medium text-foreground flex-1">
                  {travelPlan.total_days}일
                </Text>
              </View>
              <View className="flex flex-row gap-2">
                <Text className="text-sm text-muted-foreground">예산:</Text>
                <Text className="text-sm font-medium text-foreground flex-1">
                  {travelPlan.total_cost.toLocaleString('ko-KR')}원
                </Text>
              </View>
              <View className="flex flex-row gap-2">
                <Text className="text-sm text-muted-foreground">활동 수:</Text>
                <Text className="text-sm font-medium text-foreground flex-1">
                  {travelPlan.days.reduce(
                    (sum, day) => sum + day.activities.length,
                    0
                  )}
                  개
                </Text>
              </View>
            </View>
          </View>

          {/* API Response Format */}
          <View className="bg-accent/10 rounded-lg p-4 border border-accent gap-3">
            <Text className="text-base font-semibold text-foreground">
              실제 Planner Agent 응답 형식
            </Text>
            <Text className="text-xs text-muted-foreground leading-5">
              이 데모는 실제 백엔드 Planner Agent의 응답 형식을 사용합니다:
            </Text>
            <View className="bg-muted/50 rounded p-2">
              <Text className="text-xs font-mono text-foreground">
                type: 'complete'{'\n'}plan.itinerary[].activities[]{'\n'}
                estimated_cost, notes
              </Text>
            </View>
            <Text className="text-xs text-muted-foreground">
              ✅ mapPlannerResponseToTravelPlan()으로 변환됨
            </Text>
          </View>

          {/* Features */}
          <View className="gap-3">
            <Text className="text-lg font-semibold text-foreground">
              테스트 가능한 기능
            </Text>
            <View className="gap-2">
              <FeatureItem
                icon="✅"
                title="타임라인 뷰"
                description="일별 섹션 접기/펼치기, 활동 카드 보기"
              />
              <FeatureItem
                icon="✅"
                title="활동 관리"
                description="활동 수정/삭제 버튼 (모달은 추후 구현)"
              />
              <FeatureItem
                icon="✅"
                title="채팅 인터페이스"
                description="플로팅 버튼으로 AI 채팅 열기, 빠른 제안"
              />
              <FeatureItem
                icon="✅"
                title="애니메이션"
                description="부드러운 스케일, 슬라이드, 레이아웃 애니메이션"
              />
              <FeatureItem
                icon="✅"
                title="API 응답 매핑"
                description="Backend 응답을 Frontend 타입으로 자동 변환"
              />
            </View>
          </View>

          {/* Instructions */}
          <View className="bg-muted/50 rounded-lg p-4 gap-3">
            <Text className="text-base font-semibold text-foreground">
              사용 방법
            </Text>
            <View className="gap-2">
              <InstructionItem number="1" text="아래 버튼을 눌러 데모 시작" />
              <InstructionItem
                number="2"
                text="일별 카드 헤더를 탭하여 접기/펼치기"
              />
              <InstructionItem number="3" text="활동 카드의 수정/삭제 버튼 테스트" />
              <InstructionItem
                number="4"
                text="우하단 메시지 아이콘으로 채팅 열기"
              />
              <InstructionItem number="5" text="빠른 제안 버튼 또는 직접 입력" />
            </View>
          </View>

          {/* Launch Button */}
          <Button onPress={() => setShowDemo(true)} className="py-4">
            <Text className="text-base font-semibold text-primary-foreground">
              데모 시작하기
            </Text>
          </Button>

          {/* Note */}
          <View className="bg-destructive/10 rounded-lg p-4 border border-destructive">
            <Text className="text-xs text-destructive-foreground leading-5">
              ⚠️ 참고: 채팅 기능은 실제 API가 연결되지 않았으므로 메시지 전송 시
              에러가 발생할 수 있습니다. UI/UX 테스트를 위한 목 데이터입니다.
            </Text>
          </View>
        </View>
      </ScrollView>
    </View>
  );
}

// Helper Components
function FeatureItem({
  icon,
  title,
  description,
}: {
  icon: string;
  title: string;
  description: string;
}) {
  return (
    <View className="flex flex-row gap-3 items-start">
      <Text className="text-base">{icon}</Text>
      <View className="flex-1">
        <Text className="text-sm font-medium text-foreground">{title}</Text>
        <Text className="text-xs text-muted-foreground">{description}</Text>
      </View>
    </View>
  );
}

function InstructionItem({ number, text }: { number: string; text: string }) {
  return (
    <View className="flex flex-row gap-2 items-start">
      <View className="w-6 h-6 rounded-full bg-primary items-center justify-center">
        <Text className="text-xs font-bold text-primary-foreground">
          {number}
        </Text>
      </View>
      <Text className="text-sm text-foreground flex-1">{text}</Text>
    </View>
  );
}
