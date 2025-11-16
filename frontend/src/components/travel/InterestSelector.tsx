import React from 'react';
import { View } from 'react-native';
import { Text, Chip, chipTextVariants } from '@/components/ui';

interface InterestSelectorProps {
  selectedInterests: string[];
  onToggle: (interest: string) => void;
  error?: string;
}

const INTEREST_CATEGORIES = [
  { id: '역사', label: '역사', icon: '🏛️' },
  { id: '문화', label: '문화', icon: '🎨' },
  { id: '맛집', label: '맛집', icon: '🍽️' },
  { id: '카페', label: '카페', icon: '☕' },
  { id: '쇼핑', label: '쇼핑', icon: '🛍️' },
  { id: '자연', label: '자연', icon: '🌳' },
  { id: '야경', label: '야경', icon: '🌃' },
  { id: '사진', label: '사진', icon: '📸' },
  { id: '공연', label: '공연', icon: '🎭' },
  { id: '체험', label: '체험', icon: '🎪' },
];

export function InterestSelector({
  selectedInterests,
  onToggle,
  error,
}: InterestSelectorProps) {
  return (
    <View className="gap-3">
      <Text className="text-base font-semibold text-foreground">
        관심사
      </Text>

      <View className="flex flex-row flex-wrap gap-2">
        {INTEREST_CATEGORIES.map((category) => {
          const isSelected = selectedInterests.includes(category.id);

          return (
            <Chip
              key={category.id}
              onPress={() => onToggle(category.id)}
              selected={isSelected}
              size="lg"
            >
              <View className="flex flex-row items-center gap-2">
                <Text className="text-base">
                  {category.icon}
                </Text>
                <Text className={chipTextVariants({ variant: isSelected ? 'selected' : 'default', size: 'lg' })}>
                  {category.label}
                </Text>
              </View>
            </Chip>
          );
        })}
      </View>

      {error && (
        <Text className="text-sm text-destructive">{error}</Text>
      )}

      <Text className="text-xs text-muted-foreground">
        원하는 관심사를 모두 선택하세요 (최소 1개)
      </Text>
    </View>
  );
}
