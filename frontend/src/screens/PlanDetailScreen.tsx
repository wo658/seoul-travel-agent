import React, { useState, useEffect } from 'react';
import { View, ScrollView, Pressable, Alert, ActivityIndicator, Modal, ImageBackground, StyleSheet } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RouteProp } from '@react-navigation/native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { PlanReviewChat, PlanSummary, PlanTimeline } from '@/components/travel';
import { Text, Card, CardContent, Input, LoadingState, ErrorState, Button, buttonTextVariants } from '@/components/ui';
import { Header } from '@/components/navigation';
import { ArrowLeft, Menu, Edit, Calendar, Tag, DollarSign, Map, Sparkles, Save } from '@/lib/icons';
import type { RootStackParamList } from '@/navigation';
import type { TravelPlanUpdate } from '@/types';
import { planToRecord } from '@/types';
import { useCurrentPlan, usePlanStore } from '@/stores/usePlanStore';
import { useError } from '@/stores/useAppStore';

/**
 * 여행 계획 상세 화면
 *
 * 기능:
 * - 플랜 조회
 * - 플랜 수정 (제목, 설명)
 * - 플랜 삭제
 * - AI 리뷰 채팅
 *
 * 성능 최적화:
 * - FlatList 사용으로 대용량 리스트 렌더링 최적화
 * - useCallback으로 renderItem, keyExtractor 메모이제이션
 * - removeClippedSubviews, windowSize 등 성능 prop 적용
 */

type PlanDetailScreenNavigationProp = NativeStackNavigationProp<
  RootStackParamList,
  'PlanDetail'
>;

type PlanDetailScreenRouteProp = RouteProp<RootStackParamList, 'PlanDetail'>;

export function PlanDetailScreen() {
  const navigation = useNavigation<PlanDetailScreenNavigationProp>();
  const route = useRoute<PlanDetailScreenRouteProp>();
  const { planId } = route.params;

  const { currentPlan, isLoadingPlan, fetchPlan } = useCurrentPlan();
  const { updatePlan, deletePlan } = usePlanStore();
  const { error, setError } = useError();
  const insets = useSafeAreaInsets();
  const [showReviewChat, setShowReviewChat] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [updating, setUpdating] = useState(false);
  const [modificationRequest, setModificationRequest] = useState('');

  useEffect(() => {
    loadPlan();
  }, [planId]);

  useEffect(() => {
    if (currentPlan) {
      setEditTitle(currentPlan.title || '');
      setEditDescription(currentPlan.description || '');
    }
  }, [currentPlan]);

  const loadPlan = async () => {
    try {
      setError(null);
      console.log('📥 Fetching plan', planId);
      await fetchPlan(planId);
      console.log('✅ Plan fetched successfully');
    } catch (err) {
      console.error('❌ Failed to load plan:', err);
      setError(err instanceof Error ? err.message : 'Failed to load plan');
    }
  };

  const handleDelete = () => {
    Alert.alert(
      '계획 삭제',
      '정말로 이 여행 계획을 삭제하시겠습니까?',
      [
        { text: '취소', style: 'cancel' },
        {
          text: '삭제',
          style: 'destructive',
          onPress: async () => {
            try {
              await deletePlan(planId);
              Alert.alert('성공', '계획이 삭제되었습니다.', [
                { text: '확인', onPress: () => navigation.goBack() },
              ]);
            } catch (err) {
              Alert.alert('오류', err instanceof Error ? err.message : '삭제에 실패했습니다.');
            }
          },
        },
      ]
    );
  };

  const handleUpdate = async () => {
    try {
      setUpdating(true);
      const updateData: TravelPlanUpdate = {
        title: editTitle || undefined,
        description: editDescription || undefined,
      };
      await updatePlan(planId, updateData);
      setShowEditModal(false);
      Alert.alert('성공', '계획이 수정되었습니다.');
    } catch (err) {
      Alert.alert('오류', err instanceof Error ? err.message : '수정에 실패했습니다.');
    } finally {
      setUpdating(false);
    }
  };

  const handlePlanUpdated = (updatedPlan: Record<string, unknown>) => {
    // When plan is updated via review chat, refresh the plan
    console.log('🔄 Plan updated via chat, reloading from server...');
    loadPlan();
  };

  // Transform DB response to TravelPlan format for components
  const transformedPlan = currentPlan ? {
    title: currentPlan.title,
    total_days: currentPlan.itinerary?.total_days || 0,
    total_cost: currentPlan.itinerary?.days?.reduce((sum: number, day) => sum + (day.daily_cost || 0), 0) || 0,
    days: currentPlan.itinerary?.days || [],
    accommodation: currentPlan.recommendations?.accommodation ?? undefined,
    tips: [],
  } : null;

  // Debug: Log when plan data changes
  React.useEffect(() => {
    if (currentPlan) {
      console.log('📊 Current plan updated:', {
        id: currentPlan.id,
        title: currentPlan.title,
        total_days: currentPlan.itinerary?.total_days,
        days_count: currentPlan.itinerary?.days?.length,
        updated_at: currentPlan.updated_at,
      });
    }
  }, [currentPlan]);

  if (isLoadingPlan) {
    return (
      <View className="flex-1 bg-background items-center justify-center">
        <LoadingState
          size="large"
          message="계획을 불러오는 중..."
        />
      </View>
    );
  }

  if (error || !currentPlan) {
    return (
      <View className="flex-1 bg-background">
        <Header title="여행 계획" />
        <ErrorState
          title="계획을 불러올 수 없습니다"
          message={error || '알 수 없는 오류가 발생했습니다'}
          onRetry={loadPlan}
          variant="full"
        />
      </View>
    );
  }

  return (
    <View className="flex-1 bg-background">
      {/* Header */}
      <View style={{ paddingTop: insets.top }} className="bg-card border-b border-border px-4 py-2">
        <View className="flex-row items-center justify-between">
          <Pressable onPress={() => navigation.goBack()} className="w-12 h-12 items-center justify-center active:opacity-70">
            <ArrowLeft size={24} className="text-foreground" />
          </Pressable>
          <Text className="flex-1 text-center text-lg font-bold text-foreground">
            AI 추천 여행 계획
          </Text>
          <Pressable onPress={handleDelete} className="w-12 h-12 items-center justify-center active:opacity-70">
            <Menu size={24} className="text-foreground" />
          </Pressable>
        </View>
      </View>

      {/* Content */}
      <ScrollView className="flex-1" contentContainerStyle={{ paddingBottom: 180 }}>
        {/* Plan Info Card */}
        <View className="bg-card px-4 py-4 border-b border-border">
          <View className="flex-row items-center justify-between mb-4">
            <Text className="text-xl font-bold text-foreground">
              {currentPlan.title || 'My Seoul Trip'}
            </Text>
            <Pressable
              onPress={() => setShowEditModal(true)}
              className="flex-row items-center gap-1.5 rounded-full bg-primary/10 px-3 py-1.5 active:opacity-70"
            >
              <Edit size={16} className="text-primary" />
              <Text className="text-sm font-medium text-primary">수정</Text>
            </Pressable>
          </View>

          {/* Info Grid */}
          <View className="gap-3">
            <View className="flex-row items-center gap-2">
              <Calendar size={18} className="text-muted-foreground" />
              <Text className="text-sm text-foreground">
                {currentPlan.start_date || '날짜 미정'} ~ {currentPlan.end_date || ''} ({transformedPlan?.total_days || 0}일)
              </Text>
            </View>
            <View className="flex-row items-center gap-2">
              <Tag size={18} className="text-muted-foreground" />
              <Text className="text-sm text-foreground">
                {currentPlan.description || '맛집, 쇼핑, 역사'}
              </Text>
            </View>
            <View className="flex-row items-center gap-2">
              <DollarSign size={18} className="text-muted-foreground" />
              <Text className="text-sm text-foreground">
                ₩₩ (보통)
              </Text>
            </View>
          </View>
        </View>

        {/* Map Image */}
        <View className="relative h-64 bg-muted">
          <ImageBackground
            source={{ uri: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAcM40FkldLshEzPfcWZ_0Udo_BIZg9euaWZF7FUT1YQtq5w6Agor8XAbXWULM5tiCWYzinkNmCJ4UY5OhWbkYdrq50D7ipAj5NV0WrBkT0KO6bsaho_E7o3JpgEK9Ap5dVwgnFAGGjhQ02ZJLrr1y9wjr1YOhT6MnP6CHS55e_TiY90niV6mJNDhaEmCwvox_1Xh8_nWXZ65qDyC7nVCa85KfAeFW88OLqgA5yVnBmV9G2a68W-G8kLYd3qrHSzcFKYpbn4E2hlIA' }}
            style={styles.mapImage}
            resizeMode="cover"
          >
            <View style={styles.mapOverlay} />
            <View className="absolute bottom-4 left-4 right-4 flex-row justify-between items-center">
              {/* Day Badges */}
              <View className="flex-row -space-x-2">
                {transformedPlan?.days?.slice(0, 3).map((_, index) => (
                  <View
                    key={index}
                    className="h-10 w-10 items-center justify-center rounded-full border-2 border-white bg-primary"
                  >
                    <Text className="text-sm font-bold text-white">{index + 1}</Text>
                  </View>
                ))}
              </View>

              {/* View Map Button */}
              <Pressable className="flex-row items-center justify-center rounded-full bg-card px-4 py-2 shadow-lg active:opacity-70">
                <Map size={20} className="text-foreground mr-2" />
                <Text className="text-foreground font-medium">지도 크게 보기</Text>
              </Pressable>
            </View>
          </ImageBackground>
        </View>

        {/* Detailed Plan Section */}
        <View className="px-4 py-6 bg-background">
          <View className="flex-row items-center justify-between mb-4">
            <Text className="text-xl font-bold text-foreground">상세 여행 계획</Text>
          </View>

          {/* Timeline */}
          {transformedPlan && <PlanTimeline days={transformedPlan.days} />}
        </View>
      </ScrollView>

      {/* Bottom Fixed Bar */}
      <View
        style={{ paddingBottom: insets.bottom + 16 }}
        className="absolute bottom-0 left-0 right-0 bg-card/80 backdrop-blur border-t border-border pt-3 px-4"
      >
        <View className="flex-row items-center gap-2 mb-3">
          <Input
            value={modificationRequest}
            onChangeText={setModificationRequest}
            placeholder="요청사항 입력 (예: 쇼핑 시간 추가)"
            className="flex-1 h-12"
          />
          <Pressable
            onPress={() => setShowReviewChat(true)}
            className="h-12 w-12 items-center justify-center rounded-lg bg-primary active:opacity-70"
          >
            <Sparkles size={20} className="text-white" />
          </Pressable>
        </View>

        <Button onPress={handleUpdate} className="w-full h-12">
          <View className="flex-row items-center justify-center gap-2">
            <Save size={20} className="text-white" />
            <Text className={buttonTextVariants()}>내 여행에 저장</Text>
          </View>
        </Button>
      </View>

      {/* Review Chat Modal */}
      <Modal
        visible={showReviewChat}
        transparent
        animationType="slide"
        onRequestClose={() => setShowReviewChat(false)}
      >
        <View className="flex-1 bg-black/50 justify-end">
          <View className="bg-card rounded-t-3xl" style={{ height: '80%' }}>
            <PlanReviewChat
              planId={planId}
              originalPlan={planToRecord(currentPlan?.itinerary || currentPlan)}
              onPlanUpdated={handlePlanUpdated}
            />
          </View>
        </View>
      </Modal>

      {/* Edit Modal */}
      <Modal
        visible={showEditModal}
        transparent
        animationType="slide"
        onRequestClose={() => setShowEditModal(false)}
      >
        <View className="flex-1 bg-black/50 justify-end">
          <View className="bg-background rounded-t-3xl p-6 gap-4">
            <Text className="text-xl font-bold text-foreground">계획 수정</Text>

            <View className="gap-2">
              <Text className="text-sm font-medium text-foreground">제목</Text>
              <Input
                value={editTitle}
                onChangeText={setEditTitle}
                placeholder="계획 제목"
              />
            </View>

            <View className="gap-2">
              <Text className="text-sm font-medium text-foreground">설명</Text>
              <Input
                value={editDescription}
                onChangeText={setEditDescription}
                placeholder="계획 설명"
                multiline
                numberOfLines={3}
              />
            </View>

            <View className="flex-row gap-2 mt-2">
              <Button variant="secondary" onPress={() => setShowEditModal(false)} className="flex-1">
                <Text className={buttonTextVariants({ variant: 'secondary' })}>취소</Text>
              </Button>
              <Button onPress={handleUpdate} disabled={updating} className="flex-1">
                {updating ? (
                  <ActivityIndicator size="small" color="white" />
                ) : (
                  <Text className={buttonTextVariants()}>저장</Text>
                )}
              </Button>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  mapImage: {
    width: '100%',
    height: '100%',
  },
  mapOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.2)',
  },
});
