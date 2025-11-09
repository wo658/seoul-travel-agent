import React, { useState } from 'react';
import { View, ActivityIndicator, Pressable } from 'react-native';
import { PlanForm } from '@/components/travel';
import { Text } from '@/components/ui';
import { PlanFormData, GeneratePlanApiResponse } from '@/types';
import { generatePlan } from '@/services/api/chat';
import { ArrowLeft } from '@/lib/icons';

interface TravelPlanInputScreenProps {
  onPlanGenerated: (plan: GeneratePlanApiResponse) => void;
  onBack: () => void;
}

export function TravelPlanInputScreen({
  onPlanGenerated,
  onBack,
}: TravelPlanInputScreenProps) {
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

      onPlanGenerated(response);
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
      {/* Header */}
      <View className="bg-card border-b border-border px-4 py-3 flex flex-row items-center justify-between">
        <Pressable onPress={onBack} className="p-2 -m-2">
          <ArrowLeft size={24} className="text-foreground" />
        </Pressable>
        <Text className="text-lg font-semibold text-foreground">
          여행 계획 만들기
        </Text>
        <View className="w-10" />
      </View>

      {/* Content */}
      {isGenerating ? (
        <View className="flex-1 justify-center items-center gap-4">
          <ActivityIndicator size="large" color="hsl(var(--primary))" />
          <Text className="text-base text-center text-muted-foreground px-6">
            AI가 맞춤형 여행 계획을 생성하고 있습니다...{'\n'}
            잠시만 기다려주세요.
          </Text>
        </View>
      ) : (
        <>
          {error && (
            <View className="bg-destructive/10 border-l-4 border-destructive p-4">
              <Text className="text-sm text-destructive">{error}</Text>
            </View>
          )}
          <PlanForm onSubmit={handleSubmit} isLoading={isGenerating} />
        </>
      )}
    </View>
  );
}
