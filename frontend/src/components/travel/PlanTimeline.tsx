import React, { useCallback } from 'react';
import { FlatList } from 'react-native';
import { EmptyState } from '@/components/ui';
import { DayItinerary } from '@/types';
import { DayItineraryCard } from './DayItineraryCard';

interface PlanTimelineProps {
  days: DayItinerary[];
}

/**
 * 여행 일정 타임라인 컴포넌트
 *
 * React Native Best Practice 적용:
 * - FlatList 사용으로 성능 최적화
 * - useCallback으로 renderItem 메모이제이션
 * - 효율적인 keyExtractor 사용
 */
export function PlanTimeline({ days }: PlanTimelineProps) {
  // Render each day item with useCallback for performance
  const renderDayItem = useCallback(({ item: dayItinerary }: { item: DayItinerary }) => (
    <DayItineraryCard dayItinerary={dayItinerary} className="mb-4" />
  ), []);

  // Key extractor for FlatList
  const keyExtractor = useCallback((item: DayItinerary) => `day-${item.day}`, []);

  // Empty list component
  const ListEmptyComponent = useCallback(() => (
    <EmptyState
      message="일정 데이터가 없습니다."
      variant="card"
    />
  ), []);

  // Guard against invalid days data
  if (!days) {
    return <ListEmptyComponent />;
  }

  return (
    <FlatList
      data={days}
      renderItem={renderDayItem}
      keyExtractor={keyExtractor}
      ListEmptyComponent={ListEmptyComponent}
      scrollEnabled={false}
      // Performance optimizations
      removeClippedSubviews={true}
      maxToRenderPerBatch={5}
      initialNumToRender={3}
      windowSize={5}
    />
  );
}
