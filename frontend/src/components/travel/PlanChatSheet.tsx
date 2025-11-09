import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Modal,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Pressable,
  TextInput,
  ActivityIndicator,
} from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
} from 'react-native-reanimated';
import { Text, Button } from '@/components/ui';
import { PlanChatMessage, ChatSuggestion } from '@/types';
import { X, Send, Sparkles } from '@/lib/icons';

interface PlanChatSheetProps {
  visible: boolean;
  onClose: () => void;
  messages: PlanChatMessage[];
  suggestions?: ChatSuggestion[];
  isLoading?: boolean;
  onSendMessage: (message: string) => void;
  onSuggestionPress?: (suggestion: ChatSuggestion) => void;
}

export function PlanChatSheet({
  visible,
  onClose,
  messages,
  suggestions = [],
  isLoading = false,
  onSendMessage,
  onSuggestionPress,
}: PlanChatSheetProps) {
  const [inputText, setInputText] = useState('');
  const scrollViewRef = useRef<ScrollView>(null);
  const slideAnim = useSharedValue(0);

  // 기본 추천 메시지
  const defaultSuggestions: ChatSuggestion[] = [
    { id: '1', label: '예산 줄이기', prompt: '전체 예산을 20% 줄여주세요' },
    { id: '2', label: '일정 조정', prompt: '오후 일정을 더 여유롭게 조정해주세요' },
    { id: '3', label: '맛집 추가', prompt: '유명한 맛집을 추가해주세요' },
    { id: '4', label: '실내 활동', prompt: '비가 올 경우를 대비해 실내 활동을 추가해주세요' },
  ];

  const activeSuggestions = suggestions.length > 0 ? suggestions : defaultSuggestions;

  useEffect(() => {
    slideAnim.value = visible ? 1 : 0;
  }, [visible]);

  const animatedStyle = useAnimatedStyle(() => {
    return {
      transform: [
        {
          translateY: withSpring(slideAnim.value === 1 ? 0 : 600, {
            damping: 20,
            stiffness: 90,
          }),
        },
      ],
    };
  });

  const backdropStyle = useAnimatedStyle(() => {
    return {
      opacity: withTiming(slideAnim.value, { duration: 200 }),
    };
  });

  const handleSendMessage = () => {
    if (inputText.trim()) {
      onSendMessage(inputText.trim());
      setInputText('');

      // 메시지 전송 후 스크롤
      setTimeout(() => {
        scrollViewRef.current?.scrollToEnd({ animated: true });
      }, 100);
    }
  };

  const handleSuggestionPress = (suggestion: ChatSuggestion) => {
    if (onSuggestionPress) {
      onSuggestionPress(suggestion);
    } else {
      setInputText(suggestion.prompt);
    }
  };

  const formatTime = (date: Date) => {
    return new Intl.DateTimeFormat('ko-KR', {
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  };

  return (
    <Modal
      visible={visible}
      transparent
      animationType="none"
      onRequestClose={onClose}
      statusBarTranslucent
    >
      {/* Backdrop */}
      <Animated.View
        style={[backdropStyle]}
        className="absolute inset-0 bg-black/50"
      >
        <Pressable className="flex-1" onPress={onClose} />
      </Animated.View>

      {/* Bottom Sheet */}
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        className="flex-1 justify-end"
        pointerEvents="box-none"
      >
        <Animated.View style={[animatedStyle]} className="bg-card rounded-t-3xl overflow-hidden" pointerEvents="box-none">
          {/* Header */}
          <View className="flex flex-row items-center justify-between px-4 py-4 border-b border-border">
            <View className="flex flex-row items-center gap-2">
              <Sparkles size={20} className="text-primary" />
              <Text className="text-lg font-semibold text-foreground">
                AI와 계획 수정하기
              </Text>
            </View>
            <Pressable onPress={onClose} className="p-2 -m-2">
              <X size={24} className="text-foreground" />
            </Pressable>
          </View>

          {/* Messages */}
          <ScrollView
            ref={scrollViewRef}
            className="flex-1 px-4 py-4 max-h-96"
            showsVerticalScrollIndicator={false}
          >
            {messages.length === 0 ? (
              <View className="items-center justify-center py-8">
                <Sparkles size={48} className="text-muted-foreground mb-4" />
                <Text className="text-base text-center text-muted-foreground mb-2">
                  여행 계획을 수정하고 싶으신가요?
                </Text>
                <Text className="text-sm text-center text-muted-foreground">
                  아래 제안을 선택하거나 직접 입력해보세요
                </Text>
              </View>
            ) : (
              <View className="gap-3">
                {messages.map((message) => (
                  <View
                    key={message.id}
                    className={`flex ${
                      message.role === 'user' ? 'items-end' : 'items-start'
                    }`}
                  >
                    <View
                      className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                        message.role === 'user'
                          ? 'bg-primary'
                          : 'bg-muted'
                      }`}
                    >
                      <Text
                        className={`text-sm leading-5 ${
                          message.role === 'user'
                            ? 'text-primary-foreground'
                            : 'text-foreground'
                        }`}
                      >
                        {message.content}
                      </Text>
                      <Text
                        className={`text-xs mt-1 ${
                          message.role === 'user'
                            ? 'text-primary-foreground/70'
                            : 'text-muted-foreground'
                        }`}
                      >
                        {formatTime(message.timestamp)}
                      </Text>
                    </View>
                  </View>
                ))}

                {/* Loading indicator */}
                {isLoading && (
                  <View className="flex items-start">
                    <View className="bg-muted rounded-2xl px-4 py-3">
                      <ActivityIndicator size="small" color="hsl(var(--primary))" />
                    </View>
                  </View>
                )}
              </View>
            )}
          </ScrollView>

          {/* Suggestions */}
          {messages.length === 0 && (
            <View className="px-4 pb-4">
              <Text className="text-xs text-muted-foreground mb-2">빠른 수정</Text>
              <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                <View className="flex flex-row gap-2">
                  {activeSuggestions.map((suggestion) => (
                    <Pressable
                      key={suggestion.id}
                      onPress={() => handleSuggestionPress(suggestion)}
                      className="bg-secondary rounded-full px-4 py-2 active:bg-secondary/80"
                    >
                      <Text className="text-sm font-medium text-secondary-foreground">
                        {suggestion.label}
                      </Text>
                    </Pressable>
                  ))}
                </View>
              </ScrollView>
            </View>
          )}

          {/* Input */}
          <View className="flex flex-row items-center gap-2 px-4 py-3 border-t border-border bg-background">
            <View className="flex-1 bg-muted rounded-full px-4 py-2">
              <TextInput
                value={inputText}
                onChangeText={setInputText}
                placeholder="메시지를 입력하세요..."
                placeholderTextColor="hsl(var(--muted-foreground))"
                className="text-sm text-foreground"
                multiline
                maxLength={500}
                editable={!isLoading}
              />
            </View>
            <Pressable
              onPress={handleSendMessage}
              disabled={!inputText.trim() || isLoading}
              className={`w-10 h-10 rounded-full items-center justify-center ${
                inputText.trim() && !isLoading
                  ? 'bg-primary'
                  : 'bg-muted'
              }`}
            >
              <Send
                size={18}
                className={
                  inputText.trim() && !isLoading
                    ? 'text-primary-foreground'
                    : 'text-muted-foreground'
                }
              />
            </Pressable>
          </View>
        </Animated.View>
      </KeyboardAvoidingView>
    </Modal>
  );
}
