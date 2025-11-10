import React from 'react';
import { View, ScrollView, Pressable } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { useTranslation } from 'react-i18next';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  Text,
} from '@/components/ui';
import { Calendar, MapPin, Clock, Plus } from '@/lib/icons';
import type { RootStackParamList } from '@/navigation';

type MyPlansScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'MyPlans'>;

export function MyPlansScreen() {
  const navigation = useNavigation<MyPlansScreenNavigationProp>();
  const { t } = useTranslation();

  const handleCreatePlan = () => {
    navigation.navigate('PlanInput' as any);
  };

  // TODO: Fetch user's plans from backend
  const mockPlans = [
    {
      id: '1',
      title: '서울 3박 4일 여행',
      startDate: '2025-01-15',
      endDate: '2025-01-18',
      destination: '서울',
      status: 'upcoming',
    },
    {
      id: '2',
      title: '주말 서울 투어',
      startDate: '2025-01-20',
      endDate: '2025-01-21',
      destination: '서울',
      status: 'upcoming',
    },
  ];

  return (
    <View className="flex-1 bg-background">
      <StatusBar style="auto" />

      <ScrollView className="flex-1">
        <View className="p-6 pt-12 gap-6">
          {/* Header */}
          <View className="gap-2">
            <Text className="text-4xl font-bold text-foreground">
              {t('myPlans.title')}
            </Text>
            <Text className="text-base text-muted-foreground">
              {t('myPlans.description')}
            </Text>
          </View>

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

          {/* Plans List */}
          {mockPlans.length > 0 ? (
            <View className="gap-3">
              <Text className="text-xl font-semibold text-foreground">
                {t('myPlans.upcomingTrips')}
              </Text>
              {mockPlans.map((plan) => (
                <Pressable key={plan.id} className="active:opacity-70">
                  <Card>
                    <CardHeader>
                      <CardTitle>{plan.title}</CardTitle>
                      <CardDescription className="mt-2">
                        <View className="gap-2">
                          <View className="flex-row items-center gap-2">
                            <Calendar size={14} className="text-muted-foreground" />
                            <Text className="text-sm text-muted-foreground">
                              {plan.startDate} ~ {plan.endDate}
                            </Text>
                          </View>
                          <View className="flex-row items-center gap-2">
                            <MapPin size={14} className="text-muted-foreground" />
                            <Text className="text-sm text-muted-foreground">
                              {plan.destination}
                            </Text>
                          </View>
                        </View>
                      </CardDescription>
                    </CardHeader>
                  </Card>
                </Pressable>
              ))}
            </View>
          ) : (
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
