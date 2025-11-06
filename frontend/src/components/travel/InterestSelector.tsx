import React from 'react';
import { View } from 'react-native';
import { Chip, chipTextVariants, Text } from '@/components/ui';

const INTERESTS = [
  { id: 'culture', label: '문화/역사' },
  { id: 'food', label: '음식' },
  { id: 'nature', label: '자연' },
  { id: 'shopping', label: '쇼핑' },
  { id: 'art', label: '예술' },
  { id: 'nightlife', label: '야경' },
  { id: 'cafe', label: '카페' },
];

interface InterestSelectorProps {
  selectedInterests: string[];
  onInterestToggle: (interest: string) => void;
  error?: string;
}

export function InterestSelector({
  selectedInterests,
  onInterestToggle,
  error,
}: InterestSelectorProps) {
  return (
    <View className="gap-3">
      <Text className="text-base font-semibold text-foreground">
        관심사 선택 (여러 개 선택 가능)
      </Text>
      <View className="flex flex-row flex-wrap gap-2">
        {INTERESTS.map((interest) => {
          const isSelected = selectedInterests.includes(interest.id);
          return (
            <Chip
              key={interest.id}
              selected={isSelected}
              onPress={() => onInterestToggle(interest.id)}
            >
              <Text className={chipTextVariants({ variant: isSelected ? 'selected' : 'default' })}>
                {interest.label}
              </Text>
            </Chip>
          );
        })}
      </View>
      {error && (
        <Text className="text-sm text-destructive">{error}</Text>
      )}
    </View>
  );
}
