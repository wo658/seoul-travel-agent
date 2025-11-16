import React from 'react';
import { View } from 'react-native';
import { Text, IconContainer } from '@/components/ui';
import { Activity } from '@/types';
import { Camera, Utensils, Home, Coffee, ShoppingCart } from '@/lib/icons';

interface ActivityCardProps {
  activity: Activity;
  isFirst?: boolean;
  isLast?: boolean;
}

// 장소 타입에 따른 아이콘 매핑
const VENUE_TYPE_ICONS = {
  attraction: Camera,
  restaurant: Utensils,
  accommodation: Home,
  cafe: Coffee,
  shopping: ShoppingCart,
};

export function ActivityCard({ activity, isFirst, isLast }: ActivityCardProps) {
  const VenueIcon = VENUE_TYPE_ICONS[activity.venue_type];

  return (
    <View className="flex-row gap-4">
      {/* Timeline Column */}
      <View className="items-center" style={{ width: 32 }}>
        {/* Top Line */}
        {!isFirst && (
          <View className="w-0.5 bg-border flex-1" style={{ minHeight: 8 }} />
        )}

        {/* Icon Container */}
        <IconContainer size="sm" variant="primary-muted" className="rounded-full bg-background ring-2 ring-card">
          <VenueIcon size={14} className="text-primary" />
        </IconContainer>

        {/* Bottom Line */}
        {!isLast && (
          <View className="w-0.5 bg-border flex-1" style={{ minHeight: 8 }} />
        )}
      </View>

      {/* Content Column */}
      <View className="flex-1 pb-6">
        <Text className="text-base font-medium text-foreground leading-normal">
          {activity.venue_name}
        </Text>
        <Text className="text-sm text-muted-foreground font-normal leading-normal mt-0.5">
          {activity.time}
        </Text>
      </View>
    </View>
  );
}
