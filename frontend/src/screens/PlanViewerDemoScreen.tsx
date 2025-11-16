import React, { useState } from 'react';
import { View, ScrollView, Pressable, Alert, ActivityIndicator } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RouteProp } from '@react-navigation/native';
import { PlanSummary, PlanTimeline } from '@/components/travel';
import { Header } from '@/components/navigation';
import { Save, MoreVertical } from '@/lib/icons';
import { plansApi } from '@/lib/api';
import type { RootStackParamList } from '@/navigation';

/**
 * 여행 계획 뷰어 화면
 * 생성된 여행 계획을 확인하고 저장할 수 있습니다.
 */

type PlanViewerDemoScreenNavigationProp = NativeStackNavigationProp<
  RootStackParamList,
  'PlanViewer'
>;

type PlanViewerDemoScreenRouteProp = RouteProp<RootStackParamList, 'PlanViewer'>;

export function PlanViewerDemoScreen() {
  const navigation = useNavigation<PlanViewerDemoScreenNavigationProp>();
  const route = useRoute<PlanViewerDemoScreenRouteProp>();
  const { plan } = route.params;
  const [isSaving, setIsSaving] = useState(false);

  const handleSave = async () => {
    try {
      setIsSaving(true);

      // Convert TravelPlan to the format expected by the API
      const planData: Record<string, unknown> = {
        title: plan.title,
        total_days: plan.total_days,
        total_cost: plan.total_cost,
        itinerary: plan.days,
      };

      // Save the plan with all itinerary data
      const savedPlan = await plansApi.save(planData);

      Alert.alert('성공', '계획이 저장되었습니다!', [
        {
          text: '확인',
          onPress: () => navigation.navigate('Home'),
        },
      ]);
    } catch (error) {
      console.error('Failed to save plan:', error);
      Alert.alert(
        '오류',
        error instanceof Error
          ? error.message
          : '계획 저장에 실패했습니다. 다시 시도해주세요.'
      );
    } finally {
      setIsSaving(false);
    }
  };

  const handleMoreOptions = () => {
    // TODO: Implement more options menu
    Alert.alert('더보기', '추가 옵션이 곧 제공됩니다.');
  };

  return (
    <View className="flex-1 bg-background">
      <Header
        title="여행 계획"
        rightIcon={MoreVertical}
        onRightPress={handleMoreOptions}
        variant="minimal"
      />

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
      <View className="absolute bottom-6 right-4">
        <Pressable
          onPress={handleSave}
          disabled={isSaving}
          className="w-14 h-14 rounded-full bg-primary items-center justify-center shadow-lg active:scale-95"
          style={{ opacity: isSaving ? 0.6 : 1 }}
        >
          {isSaving ? (
            <ActivityIndicator size="small" color="white" />
          ) : (
            <Save size={24} className="text-primary-foreground" />
          )}
        </Pressable>
      </View>
    </View>
  );
}
