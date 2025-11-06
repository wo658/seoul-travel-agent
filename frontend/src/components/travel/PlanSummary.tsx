import React from 'react';
import { View } from 'react-native';
import { Card, CardHeader, CardTitle, CardContent, Text, Separator } from '@/components/ui';
import { TravelPlan } from '@/types';
import { Calendar, DollarSign, MapPin } from '@/lib/icons';

interface PlanSummaryProps {
  plan: TravelPlan;
}

export function PlanSummary({ plan }: PlanSummaryProps) {
  const formatCost = (cost: number) => {
    return new Intl.NumberFormat('ko-KR').format(cost);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-xl">{plan.title}</CardTitle>
      </CardHeader>
      <CardContent className="gap-4">
        {/* Quick Stats */}
        <View className="flex flex-row justify-around">
          <View className="items-center gap-2">
            <Calendar size={20} className="text-primary" />
            <Text className="text-sm text-muted-foreground">기간</Text>
            <Text className="text-base font-bold text-foreground">
              {plan.total_days}일
            </Text>
          </View>
          <View className="items-center gap-2">
            <DollarSign size={20} className="text-primary" />
            <Text className="text-sm text-muted-foreground">총 예산</Text>
            <Text className="text-base font-bold text-foreground">
              {formatCost(plan.total_cost)}원
            </Text>
          </View>
          <View className="items-center gap-2">
            <MapPin size={20} className="text-primary" />
            <Text className="text-sm text-muted-foreground">장소</Text>
            <Text className="text-base font-bold text-foreground">
              {plan.days.reduce((sum, day) => sum + day.activities.length, 0)}개
            </Text>
          </View>
        </View>

        {/* Accommodation */}
        {plan.accommodation && (
          <>
            <Separator />
            <View className="gap-2">
              <Text className="text-sm font-semibold text-foreground">🏨 숙소</Text>
              <View className="bg-muted/50 rounded-md p-3">
                <Text className="text-base font-medium text-foreground mb-1">
                  {plan.accommodation.name}
                </Text>
                <Text className="text-sm text-muted-foreground mb-2">
                  {plan.accommodation.location}
                </Text>
                <View className="flex flex-row justify-between">
                  <Text className="text-xs text-muted-foreground">
                    {plan.accommodation.type} · {plan.accommodation.total_nights}박
                  </Text>
                  <Text className="text-sm font-semibold text-foreground">
                    {formatCost(plan.accommodation.total_cost)}원
                  </Text>
                </View>
                {plan.accommodation.description && (
                  <Text className="text-xs text-muted-foreground mt-2 leading-4">
                    {plan.accommodation.description}
                  </Text>
                )}
              </View>
            </View>
          </>
        )}

        {/* Tips */}
        {plan.tips && plan.tips.length > 0 && (
          <>
            <Separator />
            <View className="gap-2">
              <Text className="text-sm font-semibold text-foreground">💡 여행 팁</Text>
              <View className="gap-2">
                {plan.tips.map((tip, index) => (
                  <View key={index} className="flex flex-row gap-2">
                    <Text className="text-primary">•</Text>
                    <Text className="text-sm text-foreground flex-1 leading-5">
                      {tip}
                    </Text>
                  </View>
                ))}
              </View>
            </View>
          </>
        )}
      </CardContent>
    </Card>
  );
}
