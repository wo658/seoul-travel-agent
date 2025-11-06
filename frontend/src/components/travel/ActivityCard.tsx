import React from 'react';
import { View } from 'react-native';
import { Card, CardContent, Text, Badge, badgeTextVariants } from '@/components/ui';
import { Activity } from '@/types';
import { Clock, MapPin, DollarSign } from '@/lib/icons';

interface ActivityCardProps {
  activity: Activity;
}

const VENUE_TYPE_LABELS: Record<Activity['venue_type'], string> = {
  attraction: '관광지',
  restaurant: '식당',
  accommodation: '숙소',
  cafe: '카페',
  shopping: '쇼핑',
};

const VENUE_TYPE_COLORS: Record<Activity['venue_type'], 'default' | 'secondary' | 'success' | 'warning'> = {
  attraction: 'default',
  restaurant: 'success',
  accommodation: 'secondary',
  cafe: 'warning',
  shopping: 'secondary',
};

export function ActivityCard({ activity }: ActivityCardProps) {
  const formatCost = (cost: number) => {
    return new Intl.NumberFormat('ko-KR').format(cost);
  };

  return (
    <Card className="mb-3">
      <CardContent className="p-4 gap-3">
        {/* Header with time and type */}
        <View className="flex flex-row justify-between items-start">
          <View className="flex flex-row items-center gap-2">
            <Clock size={16} className="text-muted-foreground" />
            <Text className="text-base font-semibold text-foreground">
              {activity.time}
            </Text>
          </View>
          <Badge variant={VENUE_TYPE_COLORS[activity.venue_type]}>
            <Text className={badgeTextVariants({ variant: VENUE_TYPE_COLORS[activity.venue_type] })}>
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
            <View className="flex flex-row items-center gap-1">
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
              💡 팁
            </Text>
            <Text className="text-xs text-foreground leading-4">
              {activity.tips}
            </Text>
          </View>
        )}
      </CardContent>
    </Card>
  );
}
