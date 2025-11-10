import React from 'react';
import { View, Pressable } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { Text } from '@/components/ui';
import { ArrowLeft, LucideIcon } from '@/lib/icons';

export interface ScreenHeaderProps {
  title: string;
  showBackButton?: boolean;
  onBackPress?: () => void;
  rightIcon?: LucideIcon;
  onRightPress?: () => void;
  rightElement?: React.ReactNode;
}

export function ScreenHeader({
  title,
  showBackButton = true,
  onBackPress,
  rightIcon: RightIcon,
  onRightPress,
  rightElement,
}: ScreenHeaderProps) {
  const navigation = useNavigation();

  const handleBackPress = () => {
    if (onBackPress) {
      onBackPress();
    } else if (navigation.canGoBack()) {
      navigation.goBack();
    }
  };

  return (
    <View className="bg-card border-b border-border px-4 py-3 flex flex-row items-center justify-between">
      {/* Left: Back Button */}
      {showBackButton ? (
        <Pressable
          onPress={handleBackPress}
          className="p-2 -m-2 active:opacity-70"
          accessibilityRole="button"
          accessibilityLabel="뒤로 가기"
        >
          <ArrowLeft size={24} className="text-foreground" />
        </Pressable>
      ) : (
        <View className="w-10" />
      )}

      {/* Center: Title */}
      <Text className="text-lg font-semibold text-foreground">
        {title}
      </Text>

      {/* Right: Icon or Custom Element */}
      {rightElement ? (
        rightElement
      ) : RightIcon && onRightPress ? (
        <Pressable
          onPress={onRightPress}
          className="p-2 -m-2 active:opacity-70"
          accessibilityRole="button"
        >
          <RightIcon size={24} className="text-foreground" />
        </Pressable>
      ) : (
        <View className="w-10" />
      )}
    </View>
  );
}
