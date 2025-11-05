/**
 * ConversationListScreen - List of all conversations
 */

import React, { useEffect } from 'react';
import { View, ScrollView, Pressable, RefreshControl } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import {
  Text,
  Button,
  buttonTextVariants,
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
} from '@/components/ui';
import { useChat } from '@/hooks/useChat';
import { MessageCircle, Plus, Clock } from '@/lib/icons';

export interface ConversationListScreenProps {
  onConversationSelect: (conversationId: string) => void;
  onNewConversation: () => void;
}

export function ConversationListScreen({
  onConversationSelect,
  onNewConversation,
}: ConversationListScreenProps) {
  const { conversations, loadConversations, isLoading } = useChat();

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  const handleRefresh = async () => {
    await loadConversations();
  };

  return (
    <View className="flex-1 bg-background">
      <StatusBar style="auto" />

      {/* Header */}
      <View className="px-6 py-4 border-b border-border bg-card">
        <View className="flex-row items-center justify-between">
          <View>
            <Text className="text-2xl font-bold text-foreground">대화 목록</Text>
            <Text className="text-sm text-muted-foreground mt-1">
              {conversations.length}개의 대화
            </Text>
          </View>

          <Button variant="default" size="icon" onPress={onNewConversation}>
            <Plus size={24} className="text-primary-foreground" />
          </Button>
        </View>
      </View>

      {/* Conversations List */}
      <ScrollView
        className="flex-1"
        contentContainerClassName="p-6 gap-4"
        refreshControl={
          <RefreshControl refreshing={isLoading} onRefresh={handleRefresh} />
        }
      >
        {conversations.length === 0 && !isLoading && (
          <View className="flex-1 items-center justify-center py-20">
            <MessageCircle size={48} className="text-muted-foreground mb-4" />
            <Text className="text-xl font-semibold text-foreground mb-2">
              대화가 없습니다
            </Text>
            <Text className="text-base text-muted-foreground text-center px-8 mb-6">
              새 대화를 시작하여{'\n'}
              서울 여행 계획을 만들어보세요
            </Text>

            <Button variant="default" onPress={onNewConversation}>
              <View className="flex-row items-center gap-2">
                <Plus size={20} className="text-primary-foreground" />
                <Text className={buttonTextVariants({ variant: 'default' })}>
                  새 대화 시작
                </Text>
              </View>
            </Button>
          </View>
        )}

        {conversations.map((conversation) => (
          <Pressable
            key={conversation.id}
            onPress={() => onConversationSelect(conversation.id)}
            className="active:opacity-70"
          >
            <Card>
              <CardHeader>
                <View className="flex-row items-start justify-between">
                  <View className="flex-1 mr-2">
                    <CardTitle>{conversation.title}</CardTitle>
                    {conversation.last_message && (
                      <CardDescription className="mt-2">
                        {conversation.last_message.length > 100
                          ? `${conversation.last_message.slice(0, 100)}...`
                          : conversation.last_message}
                      </CardDescription>
                    )}
                  </View>

                  <View
                    className={`px-2 py-1 rounded ${
                      conversation.status === 'active'
                        ? 'bg-primary/10'
                        : conversation.status === 'completed'
                        ? 'bg-secondary'
                        : 'bg-muted'
                    }`}
                  >
                    <Text
                      className={`text-xs ${
                        conversation.status === 'active'
                          ? 'text-primary'
                          : 'text-muted-foreground'
                      }`}
                    >
                      {conversation.status === 'active'
                        ? '진행중'
                        : conversation.status === 'completed'
                        ? '완료'
                        : '보관'}
                    </Text>
                  </View>
                </View>

                <View className="flex-row items-center gap-1 mt-3">
                  <Clock size={12} className="text-muted-foreground" />
                  <Text className="text-xs text-muted-foreground">
                    {formatDate(new Date(conversation.updated_at))}
                  </Text>
                </View>
              </CardHeader>
            </Card>
          </Pressable>
        ))}
      </ScrollView>
    </View>
  );
}

function formatDate(date: Date): string {
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));

  if (days === 0) {
    const hours = Math.floor(diff / (1000 * 60 * 60));
    if (hours === 0) {
      const minutes = Math.floor(diff / (1000 * 60));
      return `${minutes}분 전`;
    }
    return `${hours}시간 전`;
  }

  if (days === 1) return '어제';
  if (days < 7) return `${days}일 전`;

  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}
