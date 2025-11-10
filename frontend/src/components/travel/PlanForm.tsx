import React, { useState } from 'react';
import { View, ScrollView } from 'react-native';
import { Button, buttonTextVariants, Input, TextArea, Text } from '@/components/ui';
import { DateRangePicker } from './DateRangePicker';
import { InterestSelector } from './InterestSelector';
import { PlanFormData } from '@/types';

interface PlanFormProps {
  onSubmit: (data: PlanFormData) => void;
  isLoading?: boolean;
}

export function PlanForm({ onSubmit, isLoading }: PlanFormProps) {
  const [userRequest, setUserRequest] = useState('');
  const [startDate, setStartDate] = useState<string | null>(null);
  const [endDate, setEndDate] = useState<string | null>(null);
  const [budget, setBudget] = useState('');
  const [selectedInterests, setSelectedInterests] = useState<string[]>([]);
  const [errors, setErrors] = useState<Record<string, string>>({});

  console.log('[PlanForm] Rendering, isLoading:', isLoading);

  const handleInterestToggle = (interest: string) => {
    setSelectedInterests((prev) =>
      prev.includes(interest)
        ? prev.filter((i) => i !== interest)
        : [...prev, interest]
    );
  };

  const handleDateChange = (start: string | null, end: string | null) => {
    setStartDate(start);
    setEndDate(end);
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!userRequest.trim()) {
      newErrors.userRequest = '여행 계획을 간단히 설명해주세요';
    }

    if (!startDate) {
      newErrors.startDate = '시작 날짜를 선택해주세요';
    }

    if (!endDate) {
      newErrors.endDate = '종료 날짜를 선택해주세요';
    }

    if (selectedInterests.length === 0) {
      newErrors.interests = '최소 1개 이상의 관심사를 선택해주세요';
    }

    if (budget && (isNaN(Number(budget)) || Number(budget) <= 0)) {
      newErrors.budget = '올바른 예산을 입력해주세요';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (!validate() || !startDate || !endDate) {
      return;
    }

    const formData: PlanFormData = {
      user_request: userRequest.trim(),
      start_date: startDate,
      end_date: endDate,
      budget: budget ? Number(budget) : null,
      interests: selectedInterests,
    };

    onSubmit(formData);
  };

  return (
    <ScrollView className="flex-1 bg-background">
      <View className="p-6 gap-6">
        {/* User Request */}
        <View className="gap-3">
          <Text className="text-base font-semibold text-foreground">
            여행 계획 설명
          </Text>
          <TextArea
            placeholder="예: 서울 2박 3일 여행을 계획하고 있어요. 역사적인 장소와 맛집을 중심으로 둘러보고 싶어요."
            value={userRequest}
            onChangeText={setUserRequest}
            editable={!isLoading}
            className={errors.userRequest ? 'border-destructive' : ''}
          />
          {errors.userRequest && (
            <Text className="text-sm text-destructive">{errors.userRequest}</Text>
          )}
        </View>

        {/* Date Range Picker */}
        <DateRangePicker
          startDate={startDate}
          endDate={endDate}
          onDateChange={handleDateChange}
          error={errors.startDate || errors.endDate}
        />

        {/* Budget Input */}
        <View className="gap-3">
          <Text className="text-base font-semibold text-foreground">
            예산 (선택사항)
          </Text>
          <View className="flex flex-row items-center gap-2">
            <Input
              placeholder="300000"
              value={budget}
              onChangeText={setBudget}
              keyboardType="numeric"
              editable={!isLoading}
              className={`flex-1 ${errors.budget ? 'border-destructive' : ''}`}
            />
            <Text className="text-base text-foreground">원</Text>
          </View>
          {errors.budget && (
            <Text className="text-sm text-destructive">{errors.budget}</Text>
          )}
          <Text className="text-xs text-muted-foreground">
            예산을 입력하지 않으면 일반적인 중간 가격대로 계획됩니다.
          </Text>
        </View>

        {/* Interest Selector */}
        <InterestSelector
          selectedInterests={selectedInterests}
          onToggle={handleInterestToggle}
          error={errors.interests}
        />

        {/* Submit Button */}
        <Button
          onPress={handleSubmit}
          disabled={isLoading}
          className="mt-4"
        >
          <Text className={buttonTextVariants()}>
            {isLoading ? '계획 생성 중...' : '여행 계획 만들기'}
          </Text>
        </Button>
      </View>
    </ScrollView>
  );
}
