import React, { useEffect } from 'react';
import { View, ScrollView, Pressable } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { useNavigation } from '@react-navigation/native';
import { useTranslation } from 'react-i18next';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  Text,
  IconContainer,
  LoadingState,
  ErrorState,
  EmptyState,
} from '@/components/ui';
import { Calendar, MapPin, Clock, Plus } from '@/lib/icons';
import { Header } from '@/components/navigation';
import type { RootStackScreenProps } from '@/navigation';
import { formatDate } from '@/lib/utils/formatters';
import { usePlans } from '@/stores/usePlanStore';
import { useError } from '@/stores/useAppStore';

export function MyPlansScreen() {
  const navigation = useNavigation<RootStackScreenProps<'MyPlans'>['navigation']>();
  const { t } = useTranslation();
  const { plans, isLoadingPlans, fetchPlans } = usePlans();
  const { error, setError } = useError();

  useEffect(() => {
    loadPlans();
  }, []);

  const loadPlans = async () => {
    try {
      setError(null);
      await fetchPlans();
    } catch (err) {
      console.error('Failed to load plans:', err);
      setError(err instanceof Error ? err.message : 'Failed to load plans');
    }
  };

  const handleCreatePlan = () => {
    navigation.navigate('PlanInput');
  };

  return (
    <View className="flex-1 bg-background">
      <StatusBar style="auto" />
      <Header title={t('myPlans.title')} />

      <ScrollView className="flex-1">
        <View className="p-6 gap-6">

          {/* Create New Plan Button */}
          <Pressable onPress={handleCreatePlan} className="active:opacity-70">
            <Card className="bg-primary/5 border-primary/20 border-dashed">
              <CardContent className="py-8">
                <View className="items-center gap-3">
                  <IconContainer size="xl" variant="primary-muted">
                    <Plus className="text-primary" size={32} />
                  </IconContainer>
                  <View className="gap-1 items-center">
                    <Text className="text-lg font-semibold text-foreground">
                      {t('myPlans.createNew')}
                    </Text>
                    <Text className="text-sm text-muted-foreground">
                      {t('myPlans.createNewDesc')}
                    </Text>
                  </View>
                </View>
              </CardContent>
            </Card>
          </Pressable>

          {/* Loading State */}
          {isLoadingPlans && (
            <LoadingState
              size="large"
              message={t('myPlans.loading', 'Loading plans...')}
            />
          )}

          {/* Error State */}
          {error && !isLoadingPlans && (
            <ErrorState
              title={t('myPlans.error', 'Failed to load plans')}
              message={error}
              onRetry={loadPlans}
              retryText={t('myPlans.retry', 'Retry')}
            />
          )}

          {/* Plans List */}
          {!isLoadingPlans && !error && plans.length > 0 && (
            <View className="gap-3">
              <Text className="text-xl font-semibold text-foreground">
                {t('myPlans.upcomingTrips')}
              </Text>
              {plans.map((plan) => (
                <Pressable
                  key={plan.id}
                  className="active:opacity-70"
                  onPress={() => navigation.navigate('PlanDetail', { planId: plan.id })}
                >
                  <Card>
                    <CardHeader>
                      <View className="flex-row items-center justify-between mb-2">
                        <CardTitle className="flex-1">{plan.title}</CardTitle>
                        <View className="h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                          <MapPin size={20} className="text-primary" />
                        </View>
                      </View>
                      <CardDescription>
                        <View className="gap-3 mt-2">
                          {plan.start_date && plan.end_date && (
                            <View className="flex-row items-center gap-2">
                              <Calendar size={18} className="text-muted-foreground" />
                              <Text className="text-sm text-foreground">
                                {formatDate(plan.start_date)} ~ {formatDate(plan.end_date)} ({plan.itinerary?.total_days || 0}일)
                              </Text>
                            </View>
                          )}
                          {plan.description && (
                            <View className="flex-row items-center gap-2">
                              <MapPin size={18} className="text-muted-foreground" />
                              <Text className="text-sm text-foreground" numberOfLines={1}>
                                {plan.description}
                              </Text>
                            </View>
                          )}
                          <View className="flex-row items-center gap-2">
                            <Clock size={18} className="text-muted-foreground" />
                            <Text className="text-sm text-foreground">
                              ₩₩ (보통)
                            </Text>
                          </View>
                        </View>
                      </CardDescription>
                    </CardHeader>
                  </Card>
                </Pressable>
              ))}
            </View>
          )}

          {/* Empty State */}
          {!isLoadingPlans && !error && plans.length === 0 && (
            <EmptyState
              icon={Clock}
              message={t('myPlans.noPlans')}
            />
          )}

          {/* Bottom spacing */}
          <View className="h-8" />
        </View>
      </ScrollView>
    </View>
  );
}
