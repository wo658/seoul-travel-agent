import React from 'react';
import { View, ScrollView, Pressable } from 'react-native';
import { Text } from '@/components/ui';
import { PlanSummary, PlanTimeline } from '@/components/travel';
import { TravelPlan } from '@/types';
import { ArrowLeft, Save, MoreVertical } from '@/lib/icons';

/**
 * 여행 계획 뷰어 화면
 * 생성된 여행 계획을 확인하고 저장할 수 있습니다.
 */

interface PlanViewerDemoScreenProps {
  plan: TravelPlan;
  onBack: () => void;
  onSave?: (plan: TravelPlan) => void;
}

export function PlanViewerDemoScreen({
  plan,
  onBack,
  onSave,
}: PlanViewerDemoScreenProps) {
  const handleSave = () => {
    if (onSave) {
      onSave(plan);
    }
  };

  return (
    <View className="flex-1 bg-background">
      {/* Header */}
      <View className="bg-card border-b border-border px-4 py-3 flex flex-row items-center justify-between">
        <Pressable onPress={onBack} className="p-2 -m-2">
          <ArrowLeft size={24} className="text-foreground" />
        </Pressable>
        <Text className="text-lg font-semibold text-foreground">여행 계획</Text>
        <Pressable className="p-2 -m-2">
          <MoreVertical size={24} className="text-foreground" />
        </Pressable>
      </View>

      {/* Content */}
      <ScrollView className="flex-1">
        <View className="p-4 gap-4">
          {/* Summary */}
          <PlanSummary plan={plan} />

          {/* Timeline */}
          <PlanTimeline days={plan.days} />
        </View>

        {/* Bottom padding */}
        <View className="h-24" />
      </ScrollView>

      {/* Save Button */}
      {onSave && (
        <View className="absolute bottom-6 right-4">
          <Pressable
            onPress={handleSave}
            className="w-14 h-14 rounded-full bg-primary items-center justify-center shadow-lg active:scale-95"
          >
            <Save size={24} className="text-primary-foreground" />
          </Pressable>
        </View>
      )}
    </View>
  );
}
