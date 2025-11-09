import React, { useState, useCallback } from 'react';
import { View, ScrollView, Pressable, Alert } from 'react-native';
import { Button, buttonTextVariants, Text } from '@/components/ui';
import { PlanSummary } from '@/components/travel';
import { DraggableDayTimeline } from '@/components/travel/DraggableDayTimeline';
import { PlanChatSheet } from '@/components/travel/PlanChatSheet';
import {
  TravelPlan,
  EditableDayItinerary,
  EditableActivity,
  PlanChatMessage,
  ActivityAction,
  ChatSuggestion,
  PlanViewerMode,
} from '@/types';
import { modifyPlan } from '@/services/api/chat';
import {
  ArrowLeft,
  Save,
  MessageCircle,
  MoreVertical,
} from '@/lib/icons';

interface PlanViewerScreenProps {
  plan: TravelPlan;
  onBack: () => void;
  onSave?: (plan: TravelPlan) => void;
}

export function PlanViewerScreen({
  plan,
  onBack,
  onSave,
}: PlanViewerScreenProps) {
  // State management
  const [currentPlan, setCurrentPlan] = useState<TravelPlan>(plan);
  const [editableDays, setEditableDays] = useState<EditableDayItinerary[]>(
    convertToEditableDays(plan.days)
  );
  const [chatVisible, setChatVisible] = useState(false);
  const [chatMessages, setChatMessages] = useState<PlanChatMessage[]>([]);
  const [isModifying, setIsModifying] = useState(false);
  const [iteration, setIteration] = useState(0);
  const [mode, setMode] = useState<PlanViewerMode>('view');

  // Convert DayItinerary to EditableDayItinerary
  function convertToEditableDays(days: TravelPlan['days']): EditableDayItinerary[] {
    return days.map((day) => ({
      ...day,
      is_expanded: true,
      activities: day.activities.map((activity, index) => ({
        ...activity,
        id: `${day.day}-${index}-${Date.now()}`,
        is_custom: false,
        is_locked: false,
        alternatives: [],
      })),
    }));
  }

  // Convert EditableDayItinerary back to DayItinerary
  function convertToRegularDays(days: EditableDayItinerary[]): TravelPlan['days'] {
    return days.map((day) => ({
      day: day.day,
      date: day.date,
      theme: day.theme,
      daily_cost: day.daily_cost,
      activities: day.activities.map((activity) => {
        const { id, is_custom, is_locked, alternatives, ...rest } = activity;
        return rest;
      }),
    }));
  }

  // Handle chat message send
  const handleSendMessage = useCallback(
    async (message: string) => {
      try {
        setIsModifying(true);

        // Add user message
        const userMessage: PlanChatMessage = {
          id: `user-${Date.now()}`,
          role: 'user',
          content: message,
          timestamp: new Date(),
        };
        setChatMessages((prev) => [...prev, userMessage]);

        // Call API to modify plan
        const response = await modifyPlan({
          user_feedback: message,
          iteration: iteration + 1,
        });

        // Add assistant message
        const assistantMessage: PlanChatMessage = {
          id: `assistant-${Date.now()}`,
          role: 'assistant',
          content: '계획을 수정했습니다. 확인해주세요!',
          timestamp: new Date(),
          plan_snapshot: response.plan,
        };
        setChatMessages((prev) => [...prev, assistantMessage]);

        // Update plan
        setCurrentPlan(response.plan);
        setEditableDays(convertToEditableDays(response.plan.days));
        setIteration((prev) => prev + 1);
      } catch (err) {
        console.error('Failed to modify plan:', err);
        Alert.alert(
          '오류',
          '계획 수정 중 오류가 발생했습니다. 다시 시도해주세요.',
          [{ text: '확인' }]
        );
      } finally {
        setIsModifying(false);
      }
    },
    [iteration]
  );

  // Handle activity actions
  const handleActivityDelete = useCallback(
    (dayIndex: number, activityIndex: number) => {
      Alert.alert(
        '활동 삭제',
        '이 활동을 삭제하시겠습니까?',
        [
          { text: '취소', style: 'cancel' },
          {
            text: '삭제',
            style: 'destructive',
            onPress: () => {
              setEditableDays((prevDays) => {
                const newDays = [...prevDays];
                newDays[dayIndex].activities.splice(activityIndex, 1);
                // Recalculate daily cost
                newDays[dayIndex].daily_cost = newDays[dayIndex].activities.reduce(
                  (sum, act) => sum + act.cost,
                  0
                );
                return newDays;
              });
            },
          },
        ]
      );
    },
    []
  );

  const handleActivityEdit = useCallback(
    (dayIndex: number, activityIndex: number) => {
      // TODO: Implement activity edit modal
      Alert.alert('활동 수정', '활동 수정 기능은 곧 추가될 예정입니다.');
    },
    []
  );

  const handleAddActivity = useCallback((dayIndex: number) => {
    // TODO: Implement add activity modal
    Alert.alert('활동 추가', '활동 추가 기능은 곧 추가될 예정입니다.');
  }, []);

  const handleSave = () => {
    if (onSave) {
      const updatedPlan = {
        ...currentPlan,
        days: convertToRegularDays(editableDays),
        total_cost: editableDays.reduce((sum, day) => sum + day.daily_cost, 0),
      };
      onSave(updatedPlan);
    }
  };

  const handleToggleChat = () => {
    setChatVisible(!chatVisible);
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
          <PlanSummary plan={currentPlan} />

          {/* Timeline */}
          {editableDays.map((day, dayIndex) => (
            <DraggableDayTimeline
              key={`day-${day.day}`}
              day={day}
              dayIndex={dayIndex}
              onActivityDelete={(activityIndex) =>
                handleActivityDelete(dayIndex, activityIndex)
              }
              onActivityEdit={(activityIndex) =>
                handleActivityEdit(dayIndex, activityIndex)
              }
              onAddActivity={() => handleAddActivity(dayIndex)}
            />
          ))}
        </View>

        {/* Bottom padding for FAB */}
        <View className="h-24" />
      </ScrollView>

      {/* Floating Action Buttons */}
      <View className="absolute bottom-6 right-4 gap-3">
        {/* Chat Button */}
        <Pressable
          onPress={handleToggleChat}
          className="w-14 h-14 rounded-full bg-primary items-center justify-center shadow-lg active:scale-95"
        >
          <MessageCircle size={24} className="text-primary-foreground" />
        </Pressable>

        {/* Save Button */}
        {onSave && (
          <Pressable
            onPress={handleSave}
            className="w-14 h-14 rounded-full bg-secondary items-center justify-center shadow-lg active:scale-95"
          >
            <Save size={24} className="text-secondary-foreground" />
          </Pressable>
        )}
      </View>

      {/* Chat Sheet */}
      <PlanChatSheet
        visible={chatVisible}
        onClose={() => setChatVisible(false)}
        messages={chatMessages}
        isLoading={isModifying}
        onSendMessage={handleSendMessage}
      />
    </View>
  );
}
