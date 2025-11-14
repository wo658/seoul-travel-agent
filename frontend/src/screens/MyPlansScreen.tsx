import React, { useState, useEffect } from 'react';
import { View, ScrollView, Pressable, ActivityIndicator } from 'react-native';
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
} from '@/components/ui';
import { Calendar, MapPin, Clock, Plus, AlertCircle } from '@/lib/icons';
import { AppHeader } from '@/components/navigation';
import type { RootStackScreenProps } from '@/navigation';
import { plansApi, type TravelPlanResponse } from '@/lib/api';

export function MyPlansScreen() {
  const navigation = useNavigation<RootStackScreenProps<'MyPlans'>['navigation']>();
  const { t } = useTranslation();

  const [plans, setPlans] = useState<TravelPlanResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadPlans();
  }, []);

  const loadPlans = async () => {
    try {
      setLoading(true);
      setError(null);
      const fetchedPlans = await plansApi.list();
      setPlans(fetchedPlans);
    } catch (err) {
      console.error('Failed to load plans:', err);
      setError(err instanceof Error ? err.message : 'Failed to load plans');
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePlan = () => {
    navigation.navigate('PlanInput');
  };

  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      });
    } catch {
      return dateString;
    }
  };

  return (
    <View className="flex-1 bg-background">
      <StatusBar style="auto" />
      <AppHeader title={t('myPlans.title')} />

      <ScrollView className="flex-1">
        <View className="p-6 gap-6">

          {/* Create New Plan Button */}
          <Pressable onPress={handleCreatePlan} className="active:opacity-70">
            <Card className="bg-primary/5 border-primary/20 border-dashed">
              <CardContent className="py-8">
                <View className="items-center gap-3">
                  <View className="w-16 h-16 rounded-full bg-primary/10 items-center justify-center">
                    <Plus className="text-primary" size={32} />
                  </View>
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
          {loading && (
            <View className="py-12 items-center gap-3">
              <ActivityIndicator size="large" />
              <Text className="text-base text-muted-foreground">
                {t('myPlans.loading', 'Loading plans...')}
              </Text>
            </View>
          )}

          {/* Error State */}
          {error && !loading && (
            <View className="py-8">
              <Card className="bg-destructive/5 border-destructive/20">
                <CardContent className="py-6">
                  <View className="items-center gap-3">
                    <AlertCircle className="text-destructive" size={32} />
                    <View className="gap-1 items-center">
                      <Text className="text-base font-semibold text-destructive">
                        {t('myPlans.error', 'Failed to load plans')}
                      </Text>
                      <Text className="text-sm text-muted-foreground text-center">
                        {error}
                      </Text>
                    </View>
                    <Pressable
                      onPress={loadPlans}
                      className="mt-2 px-4 py-2 bg-primary rounded-lg active:opacity-70"
                    >
                      <Text className="text-primary-foreground font-medium">
                        {t('myPlans.retry', 'Retry')}
                      </Text>
                    </Pressable>
                  </View>
                </CardContent>
              </Card>
            </View>
          )}

          {/* Plans List */}
          {!loading && !error && plans.length > 0 && (
            <View className="gap-3">
              <Text className="text-xl font-semibold text-foreground">
                {t('myPlans.upcomingTrips')}
              </Text>
              {plans.map((plan) => (
                <Pressable key={plan.id} className="active:opacity-70">
                  <Card>
                    <CardHeader>
                      <CardTitle>{plan.title}</CardTitle>
                      <CardDescription className="mt-2">
                        <View className="gap-2">
                          {plan.start_date && plan.end_date && (
                            <View className="flex-row items-center gap-2">
                              <Calendar size={14} className="text-muted-foreground" />
                              <Text className="text-sm text-muted-foreground">
                                {formatDate(plan.start_date)} ~ {formatDate(plan.end_date)}
                              </Text>
                            </View>
                          )}
                          {plan.description && (
                            <View className="flex-row items-center gap-2">
                              <MapPin size={14} className="text-muted-foreground" />
                              <Text className="text-sm text-muted-foreground" numberOfLines={1}>
                                {plan.description}
                              </Text>
                            </View>
                          )}
                          {plan.itinerary?.total_days && (
                            <View className="flex-row items-center gap-2">
                              <Clock size={14} className="text-muted-foreground" />
                              <Text className="text-sm text-muted-foreground">
                                {plan.itinerary.total_days}일 여행
                              </Text>
                            </View>
                          )}
                        </View>
                      </CardDescription>
                    </CardHeader>
                  </Card>
                </Pressable>
              ))}
            </View>
          )}

          {/* Empty State */}
          {!loading && !error && plans.length === 0 && (
            <View className="py-12 items-center gap-3">
              <Clock className="text-muted-foreground" size={48} />
              <Text className="text-base text-center text-muted-foreground">
                {t('myPlans.noPlans')}
              </Text>
            </View>
          )}

          {/* Bottom spacing */}
          <View className="h-8" />
        </View>
      </ScrollView>
    </View>
  );
}
