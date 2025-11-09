import React, { useState } from 'react';
import { View, Pressable, LayoutAnimation, Platform, UIManager } from 'react-native';
import { Card, CardHeader, CardTitle, CardContent, Text, Button } from '@/components/ui';
import { EditableDayItinerary, EditableActivity, ActivityAction } from '@/types';
import { DraggableActivityCard } from './DraggableActivityCard';
import { ChevronDown, ChevronUp, Plus } from '@/lib/icons';

// Enable LayoutAnimation for Android
if (Platform.OS === 'android' && UIManager.setLayoutAnimationEnabledExperimental) {
  UIManager.setLayoutAnimationEnabledExperimental(true);
}

interface DraggableDayTimelineProps {
  day: EditableDayItinerary;
  dayIndex: number;
  onActivityPress?: (activity: EditableActivity, activityIndex: number) => void;
  onActivityLongPress?: (activity: EditableActivity, activityIndex: number) => void;
  onActivityDelete?: (activityIndex: number) => void;
  onActivityEdit?: (activityIndex: number) => void;
  onActivityAction?: (activityIndex: number, action: ActivityAction) => void;
  onAddActivity?: () => void;
  onToggleExpand?: () => void;
}

export function DraggableDayTimeline({
  day,
  dayIndex,
  onActivityPress,
  onActivityLongPress,
  onActivityDelete,
  onActivityEdit,
  onActivityAction,
  onAddActivity,
  onToggleExpand,
}: DraggableDayTimelineProps) {
  const [isExpanded, setIsExpanded] = useState(day.is_expanded ?? true);

  const formatCost = (cost: number) => {
    return new Intl.NumberFormat('ko-KR').format(cost);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const days = ['일', '월', '화', '수', '목', '금', '토'];
    const month = date.getMonth() + 1;
    const dayNum = date.getDate();
    const dayOfWeek = days[date.getDay()];
    return `${month}월 ${dayNum}일 (${dayOfWeek})`;
  };

  const handleToggleExpand = () => {
    LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
    setIsExpanded(!isExpanded);
    if (onToggleExpand) {
      onToggleExpand();
    }
  };

  return (
    <Card className="mb-4">
      {/* Day Header */}
      <Pressable onPress={handleToggleExpand}>
        <CardHeader className="pb-3">
          <View className="flex flex-row justify-between items-center">
            <View className="gap-1 flex-1">
              <View className="flex flex-row items-center gap-2">
                <CardTitle>Day {day.day}</CardTitle>
                {isExpanded ? (
                  <ChevronUp size={20} className="text-muted-foreground" />
                ) : (
                  <ChevronDown size={20} className="text-muted-foreground" />
                )}
              </View>
              <Text className="text-sm text-muted-foreground">
                {formatDate(day.date)}
              </Text>
            </View>
            <View className="items-end gap-1">
              <Text className="text-xs text-muted-foreground">일일 예산</Text>
              <Text className="text-base font-bold text-primary">
                {formatCost(day.daily_cost)}원
              </Text>
            </View>
          </View>

          {/* Theme */}
          {day.theme && (
            <View className="mt-2 bg-primary/10 rounded-md px-3 py-2">
              <Text className="text-sm font-medium text-primary">{day.theme}</Text>
            </View>
          )}

          {/* Collapsed summary */}
          {!isExpanded && (
            <View className="mt-2">
              <Text className="text-xs text-muted-foreground">
                {day.activities.length}개 활동
              </Text>
            </View>
          )}
        </CardHeader>
      </Pressable>

      {/* Activities */}
      {isExpanded && (
        <CardContent className="pt-0">
          {/* Activity List */}
          {day.activities.map((activity, activityIndex) => (
            <DraggableActivityCard
              key={activity.id}
              activity={activity}
              onPress={() => onActivityPress?.(activity, activityIndex)}
              onLongPress={() => onActivityLongPress?.(activity, activityIndex)}
              onSwipeDelete={() => onActivityDelete?.(activityIndex)}
              onEdit={() => onActivityEdit?.(activityIndex)}
              onAction={(action) => onActivityAction?.(activityIndex, action)}
            />
          ))}

          {/* Add Activity Button */}
          <Button
            variant="outline"
            onPress={onAddActivity}
            className="mt-2 border-dashed"
          >
            <View className="flex flex-row items-center gap-2">
              <Plus size={16} className="text-muted-foreground" />
              <Text className="text-sm font-medium text-muted-foreground">
                활동 추가
              </Text>
            </View>
          </Button>
        </CardContent>
      )}
    </Card>
  );
}
