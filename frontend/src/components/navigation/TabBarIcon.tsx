import React, { useEffect, useRef } from 'react';
import { View, Animated, Platform } from 'react-native';

interface TabBarIconProps {
  icon: React.ReactNode;
  focused: boolean;
}

/**
 * Minimalist icon-only tab bar
 * - Clean icon-focused design
 * - Smooth scale and opacity animations
 * - Subtle active indicator
 * - Cross-platform optimized (web + native)
 */
export function TabBarIcon({ icon, focused }: TabBarIconProps) {
  const scaleAnim = useRef(new Animated.Value(focused ? 1.15 : 1)).current;
  const opacityAnim = useRef(new Animated.Value(focused ? 1 : 0.5)).current;

  // Use native driver only on native platforms (not web)
  const useNativeDriver = Platform.OS !== 'web';

  useEffect(() => {
    Animated.parallel([
      Animated.spring(scaleAnim, {
        toValue: focused ? 1.15 : 1,
        friction: 7,
        tension: 120,
        useNativeDriver,
      }),
      Animated.timing(opacityAnim, {
        toValue: focused ? 1 : 0.5,
        duration: 200,
        useNativeDriver,
      }),
    ]).start();
  }, [focused, scaleAnim, opacityAnim, useNativeDriver]);

  return (
    <View
      style={{
        alignItems: 'center',
        justifyContent: 'center',
        width: 60,
        height: 48,
      }}
    >
      {/* Icon with smooth animation */}
      <Animated.View
        style={{
          transform: [{ scale: scaleAnim }],
          opacity: opacityAnim,
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {icon}
      </Animated.View>

      {/* Subtle active indicator bar */}
      {focused && (
        <View
          style={{
            position: 'absolute',
            bottom: 4,
            height: 2,
            width: 32,
            borderRadius: 2,
            backgroundColor: 'hsl(var(--primary))',
            shadowColor: 'hsl(var(--primary))',
            shadowOffset: { width: 0, height: 0 },
            shadowOpacity: 0.4,
            shadowRadius: 4,
            elevation: 2,
          }}
        />
      )}
    </View>
  );
}
