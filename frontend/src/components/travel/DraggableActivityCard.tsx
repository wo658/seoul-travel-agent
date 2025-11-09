import React from 'react';
import { View, Pressable } from 'react-native';
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withSpring,
  runOnJS,
} from 'react-native-reanimated';
import { Card, CardContent, Text, Badge, badgeTextVariants } from '@/components/ui';
import { EditableActivity, ActivityAction } from '@/types';
import { Clock, MapPin, DollarSign, GripVertical, Lock, Edit3, Trash2 } from '@/lib/icons';

interface DraggableActivityCardProps {
  activity: EditableActivity;
  onPress?: () => void;
  onLongPress?: () => void;
  onSwipeDelete?: () => void;
  onEdit?: () => void;
  onAction?: (action: ActivityAction) => void;
  isDragging?: boolean;
}

const VENUE_TYPE_LABELS: Record<EditableActivity['venue_type'], string> = {
  attraction: '관광지',
  restaurant: '식당',
  accommodation: '숙소',
  cafe: '카페',
  shopping: '쇼핑',
};

const VENUE_TYPE_COLORS: Record<
  EditableActivity['venue_type'],
  'default' | 'secondary' | 'success' | 'warning'
> = {
  attraction: 'default',
  restaurant: 'success',
  accommodation: 'secondary',
  cafe: 'warning',
  shopping: 'secondary',
};

export function DraggableActivityCard({
  activity,
  onPress,
  onLongPress,
  onSwipeDelete,
  onEdit,
  onAction,
  isDragging = false,
}: DraggableActivityCardProps) {
  const scale = useSharedValue(1);
  const translateX = useSharedValue(0);

  const formatCost = (cost: number) => {
    return new Intl.NumberFormat('ko-KR').format(cost);
  };

  // 드래깅 애니메이션 스타일
  const animatedStyle = useAnimatedStyle(() => {
    return {
      transform: [
        { scale: withSpring(isDragging ? 1.05 : scale.value) },
        { translateX: withSpring(translateX.value) },
      ],
      opacity: withSpring(isDragging ? 0.7 : 1),
    };
  });

  const handlePressIn = () => {
    scale.value = withSpring(0.98);
  };

  const handlePressOut = () => {
    scale.value = withSpring(1);
  };

  return (
    <Animated.View style={[animatedStyle]} className="mb-3">
      <Pressable
        onPress={onPress}
        onLongPress={onLongPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        delayLongPress={500}
      >
        <Card className="border-2 border-transparent active:border-primary">
          <CardContent className="p-4 gap-3">
            {/* Header with drag handle, time and type */}
            <View className="flex flex-row justify-between items-start">
              <View className="flex flex-row items-center gap-2 flex-1">
                {/* Drag Handle */}
                <View className="mr-1">
                  <GripVertical size={16} className="text-muted-foreground" />
                </View>

                <Clock size={16} className="text-muted-foreground" />
                <Text className="text-base font-semibold text-foreground">
                  {activity.time}
                </Text>

                {/* Lock indicator */}
                {activity.is_locked && (
                  <Lock size={14} className="text-muted-foreground ml-1" />
                )}
              </View>

              <Badge variant={VENUE_TYPE_COLORS[activity.venue_type]}>
                <Text
                  className={badgeTextVariants({
                    variant: VENUE_TYPE_COLORS[activity.venue_type],
                  })}
                >
                  {VENUE_TYPE_LABELS[activity.venue_type]}
                </Text>
              </Badge>
            </View>

            {/* Venue name */}
            <Text className="text-lg font-bold text-foreground">
              {activity.venue_name}
            </Text>

            {/* Description */}
            <Text className="text-sm text-foreground leading-5">
              {activity.description}
            </Text>

            {/* Details */}
            <View className="flex flex-row flex-wrap gap-4">
              <View className="flex flex-row items-center gap-1">
                <Clock size={14} className="text-muted-foreground" />
                <Text className="text-xs text-muted-foreground">
                  {activity.duration_minutes}분
                </Text>
              </View>
              <View className="flex flex-row items-center gap-1">
                <DollarSign size={14} className="text-muted-foreground" />
                <Text className="text-xs text-muted-foreground">
                  {formatCost(activity.cost)}원
                </Text>
              </View>
              {activity.location && (
                <View className="flex flex-row items-center gap-1 flex-1">
                  <MapPin size={14} className="text-muted-foreground" />
                  <Text className="text-xs text-muted-foreground" numberOfLines={1}>
                    {activity.location.address}
                  </Text>
                </View>
              )}
            </View>

            {/* Tips */}
            {activity.tips && (
              <View className="bg-muted/50 rounded-md p-3 mt-1">
                <Text className="text-xs text-muted-foreground font-medium mb-1">
                  팁
                </Text>
                <Text className="text-xs text-foreground leading-4">
                  {activity.tips}
                </Text>
              </View>
            )}

            {/* Quick actions (편집/삭제) */}
            {!activity.is_locked && (
              <View className="flex flex-row gap-2 pt-2 border-t border-border">
                <Pressable
                  onPress={onEdit}
                  className="flex-1 flex flex-row items-center justify-center gap-2 py-2 bg-muted/30 rounded-md active:bg-muted"
                >
                  <Edit3 size={14} className="text-foreground" />
                  <Text className="text-xs font-medium text-foreground">수정</Text>
                </Pressable>
                <Pressable
                  onPress={onSwipeDelete}
                  className="flex-1 flex flex-row items-center justify-center gap-2 py-2 bg-destructive/10 rounded-md active:bg-destructive/20"
                >
                  <Trash2 size={14} className="text-destructive" />
                  <Text className="text-xs font-medium text-destructive">삭제</Text>
                </Pressable>
              </View>
            )}

            {/* Custom indicator */}
            {activity.is_custom && (
              <View className="absolute top-2 right-2">
                <Badge variant="secondary">
                  <Text className={badgeTextVariants({ variant: 'secondary' })}>
                    직접 추가
                  </Text>
                </Badge>
              </View>
            )}
          </CardContent>
        </Card>
      </Pressable>
    </Animated.View>
  );
}
