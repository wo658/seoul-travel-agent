import React from 'react';
import { View } from 'react-native';
import { Card, CardHeader, CardTitle, CardContent, Text, IconContainer } from '@/components/ui';
import { DayItinerary } from '@/types';
import { ActivityCard } from './ActivityCard';
import { formatCost, formatDate } from '@/lib/utils/formatters';
import { Building, ShoppingCart, Utensils } from '@/lib/icons';

export interface DayItineraryCardProps {
  /**
   * 일일 여행 일정 데이터
   */
  dayItinerary: DayItinerary;

  /**
   * 추가 className
   */
  className?: string;
}

// 테마에 따른 아이콘 매핑
const getThemeIcon = (theme?: string) => {
  if (!theme) return Building;
  const lowerTheme = theme.toLowerCase();
  if (lowerTheme.includes('쇼핑')) return ShoppingCart;
  if (lowerTheme.includes('맛집') || lowerTheme.includes('식사')) return Utensils;
  if (lowerTheme.includes('역사') || lowerTheme.includes('문화')) return Building;
  return Building;
};

/**
 * 일일 여행 일정 카드 컴포넌트
 *
 * 하루 여행 일정을 카드 형태로 표시합니다.
 * - Day 번호 및 날짜
 * - 일일 예산
 * - 테마 (있을 경우)
 * - 활동 리스트
 *
 * @example
 * ```tsx
 * <DayItineraryCard
 *   dayItinerary={dayData}
 *   className="mb-4"
 * />
 * ```
 */
export function DayItineraryCard({ dayItinerary, className }: DayItineraryCardProps) {
  const ThemeIcon = getThemeIcon(dayItinerary.theme);

  return (
    <Card className={className}>
      <CardHeader className="pb-4">
        <View className="flex-row justify-between items-center">
          <View className="gap-1 flex-1">
            <CardTitle className="text-lg">
              Day {dayItinerary.day}{dayItinerary.theme ? `: ${dayItinerary.theme}` : ''}
            </CardTitle>
            <Text className="text-sm text-muted-foreground">
              {formatDate(dayItinerary.date, 'day-of-week')}
            </Text>
          </View>
          <IconContainer size="lg" variant="primary-muted" className="rounded-full">
            <ThemeIcon size={24} className="text-primary" />
          </IconContainer>
        </View>
      </CardHeader>
      <CardContent className="pt-0">
        {dayItinerary.activities?.map((activity, index) => (
          <ActivityCard
            key={index}
            activity={activity}
            isFirst={index === 0}
            isLast={index === dayItinerary.activities.length - 1}
          />
        )) || (
          <Text className="text-sm text-muted-foreground text-center py-4">
            활동이 없습니다.
          </Text>
        )}
      </CardContent>
    </Card>
  );
}
