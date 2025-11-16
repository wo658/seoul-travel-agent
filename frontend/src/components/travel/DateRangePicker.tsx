import React, { useState } from 'react';
import { View, Pressable } from 'react-native';
import { Text } from '@/components/ui';
import { Calendar } from 'react-native-calendars';
import dayjs from 'dayjs';

interface DateRangePickerProps {
  startDate: string | null;
  endDate: string | null;
  onDateChange: (start: string | null, end: string | null) => void;
  error?: string;
}

/**
 * Theme colors for react-native-calendars
 * Note: react-native-calendars requires hex values, not CSS variables
 * These should match the theme defined in tailwind.config.js
 */
const THEME_COLORS = {
  // Primary: blue-600 (matches --primary in theme)
  primary: '#2563eb',
  // Primary Light: blue-300 (for range selection)
  primaryLight: '#93c5fd',
  // Slate-800: for range text
  rangeText: '#1e293b',
  // Slate-400: for section titles
  sectionTitle: '#64748b',
  // Slate-300: for disabled text
  disabled: '#cbd5e1',
  // White: background
  background: '#ffffff',
} as const;

export function DateRangePicker({
  startDate,
  endDate,
  onDateChange,
  error,
}: DateRangePickerProps) {
  const [markedDates, setMarkedDates] = useState<any>({});

  const handleDayPress = (day: any) => {
    const selectedDate = day.dateString;

    if (!startDate || (startDate && endDate)) {
      // Start new selection
      onDateChange(selectedDate, null);
      setMarkedDates({
        [selectedDate]: {
          startingDay: true,
          color: THEME_COLORS.primary,
          textColor: 'white',
        },
      });
    } else if (startDate && !endDate) {
      // Select end date
      if (dayjs(selectedDate).isBefore(dayjs(startDate))) {
        // If selected date is before start, swap them
        onDateChange(selectedDate, startDate);
        updateMarkedDates(selectedDate, startDate);
      } else {
        onDateChange(startDate, selectedDate);
        updateMarkedDates(startDate, selectedDate);
      }
    }
  };

  const updateMarkedDates = (start: string, end: string) => {
    const marked: any = {};
    let currentDate = dayjs(start);
    const endDate = dayjs(end);

    while (currentDate.isBefore(endDate) || currentDate.isSame(endDate, 'day')) {
      const dateString = currentDate.format('YYYY-MM-DD');

      if (dateString === start && dateString === end) {
        marked[dateString] = {
          startingDay: true,
          endingDay: true,
          color: THEME_COLORS.primary,
          textColor: 'white',
        };
      } else if (dateString === start) {
        marked[dateString] = {
          startingDay: true,
          color: THEME_COLORS.primary,
          textColor: 'white',
        };
      } else if (dateString === end) {
        marked[dateString] = {
          endingDay: true,
          color: THEME_COLORS.primary,
          textColor: 'white',
        };
      } else {
        marked[dateString] = {
          color: THEME_COLORS.primaryLight,
          textColor: THEME_COLORS.rangeText,
        };
      }

      currentDate = currentDate.add(1, 'day');
    }

    setMarkedDates(marked);
  };

  const handleClear = () => {
    onDateChange(null, null);
    setMarkedDates({});
  };

  return (
    <View className="gap-3">
      <View className="flex flex-row items-center justify-between">
        <Text className="text-base font-semibold text-foreground">
          여행 기간
        </Text>
        {(startDate || endDate) && (
          <Pressable onPress={handleClear}>
            <Text className="text-sm text-primary">초기화</Text>
          </Pressable>
        )}
      </View>

      {/* Selected dates display */}
      {startDate && (
        <View className="flex flex-row items-center gap-2 p-3 bg-muted rounded-md">
          <Text className="text-sm text-foreground">
            {dayjs(startDate).format('YYYY년 MM월 DD일')}
          </Text>
          {endDate && (
            <>
              <Text className="text-sm text-muted-foreground">~</Text>
              <Text className="text-sm text-foreground">
                {dayjs(endDate).format('YYYY년 MM월 DD일')}
              </Text>
              <Text className="text-xs text-muted-foreground ml-auto">
                {dayjs(endDate).diff(dayjs(startDate), 'day') + 1}일
              </Text>
            </>
          )}
        </View>
      )}

      {/* Calendar */}
      <View className="border border-border rounded-lg overflow-hidden">
        <Calendar
          onDayPress={handleDayPress}
          markingType="period"
          markedDates={markedDates}
          minDate={dayjs().format('YYYY-MM-DD')}
          theme={{
            backgroundColor: 'transparent',
            calendarBackground: THEME_COLORS.background,
            textSectionTitleColor: THEME_COLORS.sectionTitle,
            selectedDayBackgroundColor: THEME_COLORS.primary,
            selectedDayTextColor: 'white',
            todayTextColor: THEME_COLORS.primary,
            dayTextColor: THEME_COLORS.rangeText,
            textDisabledColor: THEME_COLORS.disabled,
            monthTextColor: THEME_COLORS.rangeText,
            textMonthFontWeight: 'bold',
            textDayFontSize: 14,
            textMonthFontSize: 16,
            arrowColor: THEME_COLORS.primary,
          }}
        />
      </View>

      {error && (
        <Text className="text-sm text-destructive">{error}</Text>
      )}

      <Text className="text-xs text-muted-foreground">
        시작 날짜와 종료 날짜를 선택하세요
      </Text>
    </View>
  );
}
