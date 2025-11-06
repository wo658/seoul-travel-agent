import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Calendar, DateData } from 'react-native-calendars';
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
  const handleDayPress = (day: DateData) => {
    const selectedDate = day.dateString;

    // If no dates selected, set as start date
    if (!startDate && !endDate) {
      onDateChange(selectedDate, null);
      return;
    }

    // If only start date selected, set as end date (or swap if before start)
    if (startDate && !endDate) {
      if (dayjs(selectedDate).isBefore(dayjs(startDate))) {
        onDateChange(selectedDate, startDate);
      } else {
        onDateChange(startDate, selectedDate);
      }
      return;
    }

    // If both dates selected, reset and start new selection
    onDateChange(selectedDate, null);
  };

  // Generate marked dates for the range
  const getMarkedDates = () => {
    const marked: any = {};

    if (!startDate) return marked;

    const start = dayjs(startDate);
    const end = endDate ? dayjs(endDate) : null;

    // Mark start date
    marked[startDate] = {
      startingDay: true,
      color: 'hsl(215, 100%, 50%)', // primary color
      textColor: 'white',
      selected: true,
    };

    // Mark end date if exists
    if (end && endDate) {
      // Mark all dates in between
      let currentDate = start.add(1, 'day');
      while (currentDate.isBefore(end)) {
        marked[currentDate.format('YYYY-MM-DD')] = {
          color: 'hsl(215, 100%, 85%)', // lighter primary
          textColor: 'hsl(215, 100%, 20%)',
        };
        currentDate = currentDate.add(1, 'day');
      }

      marked[endDate] = {
        endingDay: true,
        color: 'hsl(215, 100%, 50%)',
        textColor: 'white',
        selected: true,
      };
    }

    return marked;
  };

  return (
    <View className="gap-3">
      <Text className="text-base font-semibold text-foreground">
        여행 날짜
      </Text>
      <View className="rounded-lg overflow-hidden border border-border bg-card">
        <Calendar
          onDayPress={handleDayPress}
          markingType="period"
          markedDates={getMarkedDates()}
          minDate={dayjs().format('YYYY-MM-DD')}
          theme={{
            calendarBackground: 'transparent',
            textSectionTitleColor: 'hsl(215, 20%, 45%)',
            selectedDayBackgroundColor: 'hsl(215, 100%, 50%)',
            selectedDayTextColor: 'white',
            todayTextColor: 'hsl(215, 100%, 50%)',
            dayTextColor: 'hsl(215, 20%, 10%)',
            textDisabledColor: 'hsl(215, 20%, 80%)',
            monthTextColor: 'hsl(215, 20%, 10%)',
            textMonthFontWeight: '600',
            textDayFontSize: 16,
            textMonthFontSize: 18,
            textDayHeaderFontSize: 14,
            arrowColor: 'hsl(215, 100%, 50%)',
          }}
          style={styles.calendar}
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

const styles = StyleSheet.create({
  calendar: {
    paddingHorizontal: 10,
    paddingVertical: 10,
  },
});
