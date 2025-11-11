import React from 'react';
import { View } from 'react-native';
import { Text } from '@/components/ui';

interface TabBarIconProps {
  icon: React.ReactNode;
  label: string;
  focused: boolean;
}

/**
 * YouTube-style tab bar icon with label
 * Uses Tailwind CSS for consistent theming
 */
export function TabBarIcon({ icon, label, focused }: TabBarIconProps) {
  return (
    <View className="items-center justify-center gap-1 py-1">
      {/* Icon container */}
      <View
        className={`
          items-center justify-center
          ${focused ? 'scale-110' : 'scale-100'}
        `}
        style={{ transform: [{ scale: focused ? 1.1 : 1 }] }}
      >
        {icon}
      </View>

      {/* Label with focused state */}
      <Text
        className={`
          text-xs
          ${focused ? 'font-semibold' : 'font-normal'}
        `}
        style={{
          color: focused ? 'hsl(var(--primary))' : 'hsl(var(--muted-foreground))',
        }}
      >
        {label}
      </Text>
    </View>
  );
}
