import React from 'react';
import { View, Pressable, Platform } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { ArrowLeft, Settings } from '@/lib/icons';
import { Text } from '@/components/ui';

interface AppHeaderProps {
  title?: string;
  showBack?: boolean;
  showSettings?: boolean;
}

export function AppHeader({ title, showBack = true, showSettings = true }: AppHeaderProps) {
  const navigation = useNavigation();
  const insets = useSafeAreaInsets();

  return (
    <View
      style={{ paddingTop: insets.top + 8 }}
      className="px-6 pb-4 bg-background border-b border-border"
    >
      <View className="flex-row items-center justify-between">
        {/* Left side - Back button or empty space */}
        <View className="w-10">
          {showBack && navigation.canGoBack() && (
            <Pressable
              onPress={() => navigation.goBack()}
              className="w-10 h-10 items-center justify-center active:opacity-70"
            >
              <ArrowLeft className="text-foreground" size={24} />
            </Pressable>
          )}
        </View>

        {/* Center - Title */}
        {title && (
          <Text className="text-lg font-semibold text-foreground">
            {title}
          </Text>
        )}

        {/* Right side - Settings button */}
        <View className="w-10">
          {showSettings && (
            <Pressable
              onPress={() => navigation.navigate('Settings' as any)}
              className="w-10 h-10 items-center justify-center active:opacity-70"
            >
              <Settings className="text-foreground" size={24} />
            </Pressable>
          )}
        </View>
      </View>
    </View>
  );
}
