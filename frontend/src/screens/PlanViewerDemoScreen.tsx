import React from 'react';
import { View, ScrollView, Pressable } from 'react-native';
import { Text, Button } from '@/components/ui';
import { PlanViewerScreen } from './PlanViewerScreen';
import { TravelPlan } from '@/types';
import { ArrowLeft } from '@/lib/icons';

/**
 * PlanViewerScreen 테스트용 데모 화면
 * 목 데이터를 사용하여 PlanViewer를 테스트할 수 있습니다.
 */

// Mock data
const MOCK_TRAVEL_PLAN: TravelPlan = {
  id: 'demo-plan-001',
  title: '서울 3일 역사 탐방',
  total_days: 3,
  total_cost: 450000,
  days: [
    {
      day: 1,
      date: '2025-12-01',
      theme: '조선시대 궁궐 탐방',
      daily_cost: 150000,
      activities: [
        {
          time: '09:00',
          venue_name: '경복궁',
          venue_type: 'attraction',
          duration_minutes: 120,
          cost: 3000,
          description: '조선시대 법궁으로, 근정전과 경회루가 유명합니다.',
          tips: '오전에 방문하면 사람이 적어요. 수문장 교대식은 10시, 14시에 진행됩니다.',
          location: {
            lat: 37.5788,
            lng: 126.977,
            address: '서울특별시 종로구 사직로 161',
          },
        },
        {
          time: '12:00',
          venue_name: '광장시장',
          venue_type: 'restaurant',
          duration_minutes: 90,
          cost: 15000,
          description: '전통 한식과 길거리 음식을 맛볼 수 있는 전통시장입니다.',
          tips: '빈대떡과 마약김밥이 유명해요. 현금 준비 필수!',
          location: {
            lat: 37.5701,
            lng: 126.9997,
            address: '서울특별시 종로구 창경궁로 88',
          },
        },
        {
          time: '15:00',
          venue_name: '창덕궁 후원',
          venue_type: 'attraction',
          duration_minutes: 150,
          cost: 8000,
          description: '유네스코 세계문화유산으로 지정된 아름다운 정원입니다.',
          tips: '후원은 예약 필수입니다. 가이드 투어로만 입장 가능해요.',
          location: {
            lat: 37.5794,
            lng: 126.991,
            address: '서울특별시 종로구 율곡로 99',
          },
        },
        {
          time: '18:30',
          venue_name: '북촌한옥마을',
          venue_type: 'attraction',
          duration_minutes: 90,
          cost: 0,
          description: '전통 한옥이 밀집된 지역으로 야경이 아름답습니다.',
          tips: '주민들이 실제 거주하는 곳이므로 조용히 관람해주세요.',
          location: {
            lat: 37.5826,
            lng: 126.9832,
            address: '서울특별시 종로구 계동길 37',
          },
        },
        {
          time: '20:00',
          venue_name: '삼계탕 전문점',
          venue_type: 'restaurant',
          duration_minutes: 60,
          cost: 18000,
          description: '신선한 재료로 만든 전통 삼계탕 전문점입니다.',
          location: {
            lat: 37.5799,
            lng: 126.985,
            address: '서울특별시 종로구 북촌로 52',
          },
        },
      ],
    },
    {
      day: 2,
      date: '2025-12-02',
      theme: '현대 서울 체험',
      daily_cost: 180000,
      activities: [
        {
          time: '10:00',
          venue_name: '남산타워',
          venue_type: 'attraction',
          duration_minutes: 120,
          cost: 16000,
          description: '서울의 랜드마크로 전망대에서 도시 전경을 볼 수 있습니다.',
          tips: '케이블카 이용 추천. 일몰 시간대가 가장 아름답습니다.',
          location: {
            lat: 37.5512,
            lng: 126.9882,
            address: '서울특별시 용산구 남산공원길 105',
          },
        },
        {
          time: '13:00',
          venue_name: '명동 먹자골목',
          venue_type: 'restaurant',
          duration_minutes: 90,
          cost: 25000,
          description: '다양한 한식과 세계 음식을 즐길 수 있는 번화가입니다.',
          tips: '칼국수와 만두가 유명해요. 주말은 매우 붐빕니다.',
          location: {
            lat: 37.5636,
            lng: 126.9835,
            address: '서울특별시 중구 명동길 14',
          },
        },
        {
          time: '15:30',
          venue_name: '동대문 디자인 플라자',
          venue_type: 'attraction',
          duration_minutes: 120,
          cost: 0,
          description: '자하 하디드가 설계한 현대적인 건축물로 전시와 쇼핑을 즐길 수 있습니다.',
          tips: '야경이 특히 아름다우니 저녁까지 머물러보세요.',
          location: {
            lat: 37.5665,
            lng: 127.0092,
            address: '서울특별시 중구 을지로 281',
          },
        },
        {
          time: '18:00',
          venue_name: '광장동 카페거리',
          venue_type: 'cafe',
          duration_minutes: 90,
          cost: 12000,
          description: '트렌디한 카페들이 모여있는 핫플레이스입니다.',
          tips: '인스타그램 감성 카페들이 많아요. 디저트도 훌륭합니다.',
          location: {
            lat: 37.5447,
            lng: 127.0737,
            address: '서울특별시 광진구 광장동',
          },
        },
        {
          time: '20:00',
          venue_name: '한강 야경 크루즈',
          venue_type: 'attraction',
          duration_minutes: 90,
          cost: 35000,
          description: '한강의 야경을 유람선에서 감상할 수 있습니다.',
          tips: '예약 필수! 석식 포함 패키지도 있어요.',
          location: {
            lat: 37.5219,
            lng: 127.0411,
            address: '서울특별시 광진구 강변북로',
          },
        },
      ],
    },
    {
      day: 3,
      date: '2025-12-03',
      theme: '문화와 쇼핑',
      daily_cost: 120000,
      activities: [
        {
          time: '10:00',
          venue_name: '국립중앙박물관',
          venue_type: 'attraction',
          duration_minutes: 150,
          cost: 0,
          description: '한국의 역사와 문화를 한눈에 볼 수 있는 국립박물관입니다.',
          tips: '입장료 무료! 주요 전시관만 집중적으로 보세요.',
          location: {
            lat: 37.5238,
            lng: 126.9806,
            address: '서울특별시 용산구 서빙고로 137',
          },
        },
        {
          time: '13:30',
          venue_name: '이태원 세계음식거리',
          venue_type: 'restaurant',
          duration_minutes: 90,
          cost: 30000,
          description: '전세계 다양한 음식을 맛볼 수 있는 국제적인 거리입니다.',
          tips: '멕시칸, 터키, 인도 음식이 유명해요.',
          location: {
            lat: 37.5347,
            lng: 126.9935,
            address: '서울특별시 용산구 이태원동',
          },
        },
        {
          time: '16:00',
          venue_name: '코엑스몰',
          venue_type: 'shopping',
          duration_minutes: 180,
          cost: 50000,
          description: '대형 쇼핑몰로 별마당 도서관이 유명합니다.',
          tips: '별마당 도서관은 인생샷 명소! 주말은 매우 붐빕니다.',
          location: {
            lat: 37.5115,
            lng: 127.0595,
            address: '서울특별시 강남구 영동대로 513',
          },
        },
        {
          time: '19:30',
          venue_name: '강남 맛집 투어',
          venue_type: 'restaurant',
          duration_minutes: 90,
          cost: 40000,
          description: '강남의 유명 맛집에서 저녁 식사를 즐깁니다.',
          tips: '예약 추천! 대기 시간이 길 수 있어요.',
          location: {
            lat: 37.498,
            lng: 127.0276,
            address: '서울특별시 강남구 강남대로',
          },
        },
      ],
    },
  ],
  accommodation: {
    name: '명동 비즈니스 호텔',
    type: '호텔',
    location: '명동역 5번 출구 도보 3분',
    cost_per_night: 80000,
    total_nights: 3,
    total_cost: 240000,
    description: '깔끔하고 교통이 편리한 비즈니스 호텔입니다.',
  },
  tips: [
    '지하철 1일권(8,000원)을 구매하면 교통비를 절약할 수 있어요.',
    '주요 관광지는 미리 예약하는 것이 좋습니다.',
    '현금과 카드를 모두 준비하세요. 전통시장은 현금만 받는 곳이 많아요.',
    '날씨가 추울 수 있으니 따뜻한 옷을 챙기세요.',
  ],
  created_at: new Date().toISOString(),
};

interface PlanViewerDemoScreenProps {
  onBack?: () => void;
}

export function PlanViewerDemoScreen({ onBack }: PlanViewerDemoScreenProps) {
  const [showDemo, setShowDemo] = React.useState(false);

  if (showDemo) {
    return (
      <PlanViewerScreen
        plan={MOCK_TRAVEL_PLAN}
        onBack={() => setShowDemo(false)}
        onSave={(updatedPlan) => {
          console.log('Plan saved:', updatedPlan);
          alert('계획이 저장되었습니다!');
        }}
      />
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
                  {MOCK_TRAVEL_PLAN.title}
                </Text>
              </View>
              <View className="flex flex-row gap-2">
                <Text className="text-sm text-muted-foreground">기간:</Text>
                <Text className="text-sm font-medium text-foreground flex-1">
                  {MOCK_TRAVEL_PLAN.total_days}일
                </Text>
              </View>
              <View className="flex flex-row gap-2">
                <Text className="text-sm text-muted-foreground">예산:</Text>
                <Text className="text-sm font-medium text-foreground flex-1">
                  {MOCK_TRAVEL_PLAN.total_cost.toLocaleString('ko-KR')}원
                </Text>
              </View>
              <View className="flex flex-row gap-2">
                <Text className="text-sm text-muted-foreground">활동 수:</Text>
                <Text className="text-sm font-medium text-foreground flex-1">
                  {MOCK_TRAVEL_PLAN.days.reduce(
                    (sum, day) => sum + day.activities.length,
                    0
                  )}
                  개
                </Text>
              </View>
            </View>
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
                icon="⏳"
                title="드래그앤드롭"
                description="활동 재정렬 (Phase 2에서 구현 예정)"
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
          <View className="bg-accent/10 rounded-lg p-4 border border-accent">
            <Text className="text-xs text-accent-foreground">
              💡 참고: 채팅 기능은 실제 API가 연결되지 않았으므로 메시지 전송 시
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
