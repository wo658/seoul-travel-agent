import React, { useState } from 'react';
import { View, ScrollView, ActivityIndicator } from 'react-native';
import { Button, buttonTextVariants, Text } from '@/components/ui';
import { PlanSummary, PlanTimeline, ModifyPlanModal } from '@/components/travel';
import { TravelPlan, ModifyPlanResponse } from '@/types';
import { modifyPlan } from '@/services/api/chat';
import { ArrowLeft, Edit, Save, RefreshCw } from '@/lib/icons';

interface PlanReviewScreenProps {
  plan: TravelPlan;
  onBack: () => void;
  onSave?: (plan: TravelPlan) => void;
  onRegenerate?: () => void;
}

export function PlanReviewScreen({
  plan,
  onBack,
  onSave,
  onRegenerate,
}: PlanReviewScreenProps) {
  const [currentPlan, setCurrentPlan] = useState<TravelPlan>(plan);
  const [isModifying, setIsModifying] = useState(false);
  const [showModifyModal, setShowModifyModal] = useState(false);
  const [iteration, setIteration] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const handleModifyRequest = async (feedback: string) => {
    try {
      setIsModifying(true);
      setError(null);

      const response = await modifyPlan({
        user_feedback: feedback,
        iteration: iteration + 1,
      });

      setCurrentPlan(response.plan);
      setIteration((prev) => prev + 1);
      setShowModifyModal(false);
    } catch (err) {
      console.error('Failed to modify plan:', err);
      setError(
        err instanceof Error
          ? err.message
          : '계획 수정 중 오류가 발생했습니다. 다시 시도해주세요.'
      );
    } finally {
      setIsModifying(false);
    }
  };

  const handleSave = () => {
    if (onSave) {
      onSave(currentPlan);
    }
  };

  const handleRegenerate = () => {
    if (onRegenerate) {
      onRegenerate();
    }
  };

  return (
    <View className="flex-1 bg-background">
      {/* Header */}
      <View className="bg-card border-b border-border px-4 py-3 flex flex-row items-center justify-between">
        <Button variant="ghost" size="icon" onPress={onBack}>
          <ArrowLeft size={24} className="text-foreground" />
        </Button>
        <Text className="text-lg font-semibold text-foreground">여행 계획</Text>
        <View className="w-10" />
      </View>

      {/* Error Message */}
      {error && (
        <View className="bg-destructive/10 border-l-4 border-destructive p-4">
          <Text className="text-sm text-destructive">{error}</Text>
        </View>
      )}

      {/* Loading Overlay */}
      {isModifying && (
        <View className="absolute inset-0 bg-background/80 z-50 justify-center items-center">
          <View className="bg-card rounded-lg p-6 items-center gap-4">
            <ActivityIndicator size="large" color="hsl(var(--primary))" />
            <Text className="text-base text-center text-foreground">
              피드백을 반영하여{'\n'}계획을 수정하고 있습니다...
            </Text>
          </View>
        </View>
      )}

      {/* Content */}
      <ScrollView className="flex-1">
        <View className="p-4 gap-4">
          {/* Summary */}
          <PlanSummary plan={currentPlan} />

          {/* Timeline */}
          <PlanTimeline days={currentPlan.days} />
        </View>
      </ScrollView>

      {/* Action Buttons */}
      <View className="bg-card border-t border-border p-4 gap-2">
        <View className="flex flex-row gap-2">
          <Button
            variant="outline"
            onPress={() => setShowModifyModal(true)}
            disabled={isModifying}
            className="flex-1"
          >
            <View className="flex flex-row items-center gap-2">
              <Edit size={16} className="text-foreground" />
              <Text className={buttonTextVariants({ variant: 'outline' })}>
                수정 요청
              </Text>
            </View>
          </Button>
          {onSave && (
            <Button
              onPress={handleSave}
              disabled={isModifying}
              className="flex-1"
            >
              <View className="flex flex-row items-center gap-2">
                <Save size={16} className="text-primary-foreground" />
                <Text className={buttonTextVariants()}>
                  계획 저장
                </Text>
              </View>
            </Button>
          )}
        </View>
        {onRegenerate && (
          <Button
            variant="secondary"
            onPress={handleRegenerate}
            disabled={isModifying}
          >
            <View className="flex flex-row items-center gap-2">
              <RefreshCw size={16} className="text-secondary-foreground" />
              <Text className={buttonTextVariants({ variant: 'secondary' })}>
                다시 생성
              </Text>
            </View>
          </Button>
        )}
      </View>

      {/* Modify Modal */}
      <ModifyPlanModal
        visible={showModifyModal}
        onClose={() => setShowModifyModal(false)}
        onSubmit={handleModifyRequest}
        isLoading={isModifying}
      />
    </View>
  );
}
