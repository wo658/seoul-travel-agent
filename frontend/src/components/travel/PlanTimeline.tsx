import React from 'react';
import { View } from 'react-native';
import { Card, CardHeader, CardTitle, CardContent, Text } from '@/components/ui';
import { DayItinerary } from '@/types';
import { ActivityCard } from './ActivityCard';

interface PlanTimelineProps {
  days: DayItinerary[];
}

export function PlanTimeline({ days }: PlanTimelineProps) {
  const formatCost = (cost: number) => {
    return new Intl.NumberFormat('ko-KR').format(cost);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const days = ['일', '월', '화', '수', '목', '금', '토'];
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const dayOfWeek = days[date.getDay()];
    return `${month}월 ${day}일 (${dayOfWeek})`;
  };

  return (
    <View className="gap-4">
      {days.map((dayItinerary) => (
        <Card key={dayItinerary.day}>
          <CardHeader className="pb-3">
            <View className="flex flex-row justify-between items-center">
              <View className="gap-1">
                <CardTitle>Day {dayItinerary.day}</CardTitle>
                <Text className="text-sm text-muted-foreground">
                  {formatDate(dayItinerary.date)}
                </Text>
              </View>
              <View className="items-end gap-1">
                <Text className="text-xs text-muted-foreground">일일 예산</Text>
                <Text className="text-base font-bold text-primary">
                  {formatCost(dayItinerary.daily_cost)}원
                </Text>
              </View>
            </View>
            {dayItinerary.theme && (
              <View className="mt-2 bg-primary/10 rounded-md px-3 py-2">
                <Text className="text-sm font-medium text-primary">
                  🎯 {dayItinerary.theme}
                </Text>
              </View>
            )}
          </CardHeader>
          <CardContent className="pt-0">
            {dayItinerary.activities.map((activity, index) => (
              <ActivityCard key={index} activity={activity} />
            ))}
          </CardContent>
        </Card>
      ))}
    </View>
  );
}
