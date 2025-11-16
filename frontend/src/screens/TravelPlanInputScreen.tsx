import React, { useState } from 'react';
import { View } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { PlanForm } from '@/components/travel';
import { Header } from '@/components/navigation';
import { LoadingState, ErrorState } from '@/components/ui';
import { PlanFormData, TravelPlan } from '@/types';
import { generatePlan } from '@/services/api/chat';
import type { RootStackParamList } from '@/navigation';

type TravelPlanInputScreenNavigationProp = NativeStackNavigationProp<
  RootStackParamList,
  'PlanInput'
>;

export function TravelPlanInputScreen() {
  const navigation = useNavigation<TravelPlanInputScreenNavigationProp>();
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (formData: PlanFormData) => {
    try {
      setIsGenerating(true);
      setError(null);

      const response = await generatePlan({
        user_request: formData.user_request,
        start_date: formData.start_date,
        end_date: formData.end_date,
        budget: formData.budget,
        interests: formData.interests,
      });

      // Navigate to plan viewer with the generated plan
      navigation.navigate('PlanViewer', {
        plan: response.plan as unknown as TravelPlan,
      });
    } catch (err) {
      console.error('Failed to generate plan:', err);
      setError(
        err instanceof Error
          ? err.message
          : '계획 생성 중 오류가 발생했습니다. 다시 시도해주세요.'
      );
    } finally {
      setIsGenerating(false);
    }
  };

  console.log('[TravelPlanInputScreen] Rendering, isGenerating:', isGenerating, 'error:', error);

  return (
    <View className="flex-1 bg-background">
      <Header title="여행 계획 만들기" variant="minimal" />

      {/* Content */}
      {isGenerating ? (
        <View className="flex-1 justify-center items-center">
          <LoadingState
            size="large"
            message={`AI가 맞춤형 여행 계획을 생성하고 있습니다...\n잠시만 기다려주세요.`}
            variant="primary"
          />
        </View>
      ) : (
        <>
          {error && (
            <ErrorState
              message={error}
              variant="inline"
            />
          )}
          <PlanForm onSubmit={handleSubmit} isLoading={isGenerating} />
        </>
      )}
    </View>
  );
}
