import React from 'react';
import { View } from 'react-native';
import DateTimePicker from 'react-native-ui-datepicker';
import dayjs from 'dayjs';
import { Text } from '@/components/ui';

interface DateRangePickerProps {
  startDate: string | null;
  endDate: string | null;
  onDateChange: (start: string | null, end: string | null) => void;
  error?: string;
}

export function DateRangePicker({
  startDate,
  endDate,
  onDateChange,
  error,
}: DateRangePickerProps) {
  const handleChange = ({ startDate: start, endDate: end }: { startDate?: dayjs.Dayjs; endDate?: dayjs.Dayjs }) => {
    const startStr = start ? start.format('YYYY-MM-DD') : null;
    const endStr = end ? end.format('YYYY-MM-DD') : null;
    onDateChange(startStr, endStr);
  };

  return (
    <View className="gap-3">
      <Text className="text-base font-semibold text-foreground">
        여행 날짜
      </Text>
      <View className="rounded-lg overflow-hidden border border-border bg-card p-4">
        <DateTimePicker
          mode="range"
          startDate={startDate ? dayjs(startDate) : undefined}
          endDate={endDate ? dayjs(endDate) : undefined}
          onChange={handleChange}
          minDate={dayjs()}
          selectedItemColor="bg-primary"
          selectedTextStyle="text-primary-foreground"
          calendarTextStyle="text-foreground"
          headerTextStyle="text-foreground"
          weekDaysTextStyle="text-muted-foreground"
          todayTextStyle="text-primary"
        />
      </View>
      {(startDate || endDate) && (
        <View className="flex flex-row items-center justify-between bg-primary/10 rounded-lg p-3">
          <View className="flex-1">
            <Text className="text-xs text-muted-foreground mb-1">시작 날짜</Text>
            <Text className="text-base font-semibold text-foreground">
              {startDate ? new Date(startDate).toLocaleDateString('ko-KR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              }) : '-'}
            </Text>
          </View>
          <View className="px-3">
            <Text className="text-muted-foreground">→</Text>
          </View>
          <View className="flex-1">
            <Text className="text-xs text-muted-foreground mb-1">종료 날짜</Text>
            <Text className="text-base font-semibold text-foreground">
              {endDate ? new Date(endDate).toLocaleDateString('ko-KR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              }) : '-'}
            </Text>
          </View>
        </View>
      )}
      {startDate && endDate && (
        <View className="bg-muted/50 rounded-md px-3 py-2">
          <Text className="text-sm text-center text-foreground">
            총 {Math.ceil((new Date(endDate).getTime() - new Date(startDate).getTime()) / (1000 * 60 * 60 * 24)) + 1}일 여행
          </Text>
        </View>
      )}
      {error && (
        <Text className="text-sm text-destructive">{error}</Text>
      )}
    </View>
  );
}
