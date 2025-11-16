import React from 'react';
import { View, Pressable } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Text } from '@/components/ui';
import { ArrowLeft, Settings, type LucideIcon } from '@/lib/icons';

export interface HeaderProps {
  /**
   * Header title text
   */
  title?: string;
  /**
   * Show back button
   * @default true
   */
  showBack?: boolean;
  /**
   * Custom back button press handler
   * If not provided, will use navigation.goBack()
   */
  onBackPress?: () => void;
  /**
   * Show settings button on the right
   * @default false
   */
  showSettings?: boolean;
  /**
   * Custom settings button press handler
   * If not provided and showSettings is true, will navigate to Settings screen
   */
  onSettingsPress?: () => void;
  /**
   * Custom icon component for right side
   */
  rightIcon?: LucideIcon;
  /**
   * Custom right icon press handler
   */
  onRightPress?: () => void;
  /**
   * Custom element to render on the right side
   * Takes precedence over rightIcon and showSettings
   */
  rightElement?: React.ReactNode;
  /**
   * Header variant
   * - 'full': Includes SafeAreaInsets padding at the top
   * - 'minimal': No SafeAreaInsets padding (for use with screens that handle it separately)
   * @default 'full'
   */
  variant?: 'full' | 'minimal';
}

/**
 * Unified Header component
 * Combines functionality of AppHeader and ScreenHeader
 *
 * @example
 * ```tsx
 * // Simple header with back button and title
 * <Header title="Settings" />
 *
 * // Header with settings button
 * <Header title="Home" showBack={false} showSettings />
 *
 * // Header with custom right icon
 * <Header title="Plan" rightIcon={MoreVertical} onRightPress={handleMore} />
 *
 * // Header with custom right element
 * <Header title="Profile" rightElement={<CustomButton />} />
 * ```
 */
export function Header({
  title,
  showBack = true,
  onBackPress,
  showSettings = false,
  onSettingsPress,
  rightIcon: RightIcon,
  onRightPress,
  rightElement,
  variant = 'full',
}: HeaderProps) {
  const navigation = useNavigation();
  const insets = useSafeAreaInsets();

  const handleBackPress = () => {
    if (onBackPress) {
      onBackPress();
    } else if (navigation.canGoBack()) {
      navigation.goBack();
    }
  };

  const handleSettingsPress = () => {
    if (onSettingsPress) {
      onSettingsPress();
    } else {
      navigation.navigate('Settings' as any);
    }
  };

  // Determine right side content
  let rightContent: React.ReactNode = null;
  if (rightElement) {
    rightContent = rightElement;
  } else if (RightIcon && onRightPress) {
    rightContent = (
      <Pressable
        onPress={onRightPress}
        className="w-10 h-10 items-center justify-center active:opacity-70"
        accessibilityRole="button"
      >
        <RightIcon size={24} className="text-foreground" />
      </Pressable>
    );
  } else if (showSettings) {
    rightContent = (
      <Pressable
        onPress={handleSettingsPress}
        className="w-10 h-10 items-center justify-center active:opacity-70"
        accessibilityRole="button"
        accessibilityLabel="설정"
      >
        <Settings size={24} className="text-foreground" />
      </Pressable>
    );
  }

  return (
    <View
      style={variant === 'full' ? { paddingTop: insets.top + 8 } : undefined}
      className="px-6 pb-4 bg-background border-b border-border"
    >
      <View className="flex-row items-center justify-between">
        {/* Left side - Back button or empty space */}
        <View className="w-10">
          {showBack && (
            <Pressable
              onPress={handleBackPress}
              className="w-10 h-10 items-center justify-center active:opacity-70"
              accessibilityRole="button"
              accessibilityLabel="뒤로 가기"
            >
              <ArrowLeft size={24} className="text-foreground" />
            </Pressable>
          )}
        </View>

        {/* Center - Title */}
        {title && (
          <Text className="text-lg font-semibold text-foreground">
            {title}
          </Text>
        )}

        {/* Right side - Settings, custom icon, or custom element */}
        <View className="w-10">
          {rightContent}
        </View>
      </View>
    </View>
  );
}
