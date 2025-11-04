import React, { useEffect, useRef } from 'react';
import { View, Animated, Easing } from 'react-native';
import { Text } from '@/components/ui';
import { cn } from '@/lib/utils';
import { Sparkles } from '@/lib/icons';

export interface StreamingIndicatorProps {
  className?: string;
  streamingText?: string;
}

/**
 * StreamingIndicator - AI response streaming indicator
 * Shows typing animation while AI is generating response
 *
 * @example
 * ```tsx
 * <StreamingIndicator streamingText="AI is thinking..." />
 * ```
 */
export function StreamingIndicator({
  className,
  streamingText
}: StreamingIndicatorProps) {
  const opacity1 = useRef(new Animated.Value(0.3)).current;
  const opacity2 = useRef(new Animated.Value(0.3)).current;
  const opacity3 = useRef(new Animated.Value(0.3)).current;

  useEffect(() => {
    const animation = Animated.loop(
      Animated.sequence([
        Animated.timing(opacity1, {
          toValue: 1,
          duration: 500,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
        Animated.timing(opacity2, {
          toValue: 1,
          duration: 500,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
        Animated.timing(opacity3, {
          toValue: 1,
          duration: 500,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
        Animated.parallel([
          Animated.timing(opacity1, {
            toValue: 0.3,
            duration: 500,
            easing: Easing.inOut(Easing.ease),
            useNativeDriver: true,
          }),
          Animated.timing(opacity2, {
            toValue: 0.3,
            duration: 500,
            easing: Easing.inOut(Easing.ease),
            useNativeDriver: true,
          }),
          Animated.timing(opacity3, {
            toValue: 0.3,
            duration: 500,
            easing: Easing.inOut(Easing.ease),
            useNativeDriver: true,
          }),
        ]),
      ])
    );

    animation.start();

    return () => {
      animation.stop();
    };
  }, [opacity1, opacity2, opacity3]);

  return (
    <View className={cn('mb-4 flex-row justify-start', className)}>
      <View className="w-8 h-8 rounded-full bg-primary items-center justify-center mr-2">
        <Sparkles size={16} className="text-primary-foreground" />
      </View>

      <View className="max-w-[80%]">
        <View className="rounded-2xl px-4 py-3 bg-muted">
          {streamingText ? (
            <Text className="text-base text-foreground leading-5">
              {streamingText}
            </Text>
          ) : (
            <View className="flex-row items-center gap-1">
              <Animated.View
                style={{ opacity: opacity1 }}
                className="w-2 h-2 rounded-full bg-foreground"
              />
              <Animated.View
                style={{ opacity: opacity2 }}
                className="w-2 h-2 rounded-full bg-foreground"
              />
              <Animated.View
                style={{ opacity: opacity3 }}
                className="w-2 h-2 rounded-full bg-foreground"
              />
            </View>
          )}
        </View>
      </View>
    </View>
  );
}
