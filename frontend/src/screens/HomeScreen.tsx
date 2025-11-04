import React, { useState } from 'react';
import { View, ScrollView } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import {
  Button,
  buttonTextVariants,
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
  Input,
  Text,
  Separator,
} from '@/components/ui';
import { MapPin, Calendar, Sparkles, Clock, TrendingUp, Loader2 } from '@/lib/icons/';

export interface HomeScreenProps {
  onStartChat?: () => void;
  onViewConversations?: () => void;
}

export function HomeScreen({ onStartChat, onViewConversations }: HomeScreenProps) {
  const [destination, setDestination] = useState('');
  const [duration, setDuration] = useState('');

  return (
    <View className="flex-1 bg-background">
      <StatusBar style="auto" />

      <ScrollView className="flex-1">
        <View className="p-6 pt-12 gap-6">
          {/* Header */}
          <View className="gap-2">
            <Text className="text-4xl font-bold text-foreground">
              Seoul AI Travel Planner
            </Text>
            <Text className="text-base text-muted-foreground">
              여행 계획을 AI와 함께
            </Text>
          </View>

          <Separator />

          {/* Welcome Card */}
          <Card>
            <CardHeader>
              <CardTitle>환영합니다!</CardTitle>
              <CardDescription>
                AI 기반 서울 여행 플래너로 완벽한 여행을 계획하세요
              </CardDescription>
            </CardHeader>
            <CardContent className="gap-4">
              <Input
                placeholder="여행 목적지를 입력하세요..."
                value={destination}
                onChangeText={setDestination}
              />
              <Input
                placeholder="여행 기간을 입력하세요..."
                value={duration}
                onChangeText={setDuration}
              />
            </CardContent>
            <CardFooter className="gap-2">
              <Button className="flex-1" onPress={onStartChat}>
                <Text className={buttonTextVariants({ variant: 'default' })}>
                  새 대화 시작
                </Text>
              </Button>
              <Button variant="outline" className="flex-1" onPress={onViewConversations}>
                <Text className={buttonTextVariants({ variant: 'outline' })}>
                  대화 목록
                </Text>
              </Button>
            </CardFooter>
          </Card>

          {/* Features Section */}
          <View className="gap-4">
            <Text className="text-2xl font-semibold text-foreground">
              주요 기능
            </Text>

            <Card>
              <CardHeader>
                <View className="flex-row items-center gap-2">
                  <Sparkles className="text-primary" size={20} />
                  <CardTitle>AI 추천</CardTitle>
                </View>
                <CardDescription>
                  맞춤형 여행지와 일정 추천
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <View className="flex-row items-center gap-2">
                  <TrendingUp className="text-primary" size={20} />
                  <CardTitle>실시간 정보</CardTitle>
                </View>
                <CardDescription>
                  최신 관광 정보와 교통 정보 제공
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <View className="flex-row items-center gap-2">
                  <Clock className="text-primary" size={20} />
                  <CardTitle>일정 관리</CardTitle>
                </View>
                <CardDescription>
                  효율적인 여행 일정 자동 생성
                </CardDescription>
              </CardHeader>
            </Card>
          </View>

          <Separator />

          {/* Action Buttons Examples */}
          <View className="gap-3">
            <Text className="text-xl font-semibold text-foreground">
              버튼 스타일 가이드
            </Text>

            <Button variant="default" size="lg">
              <Text className={buttonTextVariants({ variant: 'default', size: 'lg' })}>
                Primary Button
              </Text>
            </Button>

            <Button variant="secondary" size="lg">
              <Text className={buttonTextVariants({ variant: 'secondary', size: 'lg' })}>
                Secondary Button
              </Text>
            </Button>

            <Button variant="destructive" size="lg">
              <Text className={buttonTextVariants({ variant: 'destructive', size: 'lg' })}>
                Destructive Button
              </Text>
            </Button>

            <Button variant="outline" size="lg">
              <Text className={buttonTextVariants({ variant: 'outline', size: 'lg' })}>
                Outline Button
              </Text>
            </Button>

            <Button variant="ghost" size="lg">
              <Text className={buttonTextVariants({ variant: 'ghost', size: 'lg' })}>
                Ghost Button
              </Text>
            </Button>

            <Button variant="link" size="lg">
              <Text className={buttonTextVariants({ variant: 'link', size: 'lg' })}>
                Link Button
              </Text>
            </Button>

            <Button size="lg" disabled>
              <View className="flex-row items-center gap-2">
                <Loader2 className="text-primary-foreground animate-spin" size={16} />
                <Text className={buttonTextVariants({ variant: 'default', size: 'lg' })}>
                  Loading...
                </Text>
              </View>
            </Button>
          </View>
        </View>
      </ScrollView>
    </View>
  );
}
