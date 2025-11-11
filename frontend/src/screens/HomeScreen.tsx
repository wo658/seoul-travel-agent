import React from 'react';
import { View, ScrollView, Pressable } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { useNavigation } from '@react-navigation/native';
import { useTranslation } from 'react-i18next';
import {
  Button,
  buttonTextVariants,
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  Text,
} from '@/components/ui';
import { MapPin, Calendar, Sparkles, Clock, TrendingUp, ArrowRight } from '@/lib/icons/';
import type { BottomTabScreenProps } from '@/navigation';

type HomeScreenNavigationProp = BottomTabScreenProps<'HomeTab'>['navigation'];

export function HomeScreen() {
  const navigation = useNavigation<HomeScreenNavigationProp>();
  const { t } = useTranslation();

  const handleStartPlanning = () => {
    navigation.navigate('PlanInput' as any);
  };

  return (
    <View className="flex-1 bg-background">
      <StatusBar style="auto" />

      <ScrollView className="flex-1">
        <View className="p-6 pt-16 gap-8">
          {/* Hero Section */}
          <View className="gap-3">
            <Text className="text-5xl font-bold text-foreground">
              {t('home.title')}
            </Text>
            <Text className="text-4xl font-bold text-primary">
              {t('home.subtitle')}
            </Text>
            <Text className="text-lg text-muted-foreground mt-2">
              {t('home.description')}
            </Text>
          </View>

          {/* CTA Card */}
          <Card className="bg-gradient-to-br from-primary/10 to-primary/5 border-primary/20">
            <CardContent className="gap-4 pt-6">
              <View className="gap-2">
                <Text className="text-2xl font-bold text-foreground">
                  {t('home.ctaTitle')}
                </Text>
                <Text className="text-base text-muted-foreground">
                  {t('home.ctaDescription')}
                </Text>
              </View>

              <Button size="lg" onPress={handleStartPlanning} className="mt-2">
                <View className="flex-row items-center gap-2">
                  <Calendar className="text-primary-foreground" size={22} />
                  <Text className={buttonTextVariants({ variant: 'default', size: 'lg' })}>
                    {t('home.createPlan')}
                  </Text>
                  <ArrowRight className="text-primary-foreground" size={20} />
                </View>
              </Button>
            </CardContent>
          </Card>

          {/* Features Grid */}
          <View className="gap-3">
            <Text className="text-2xl font-bold text-foreground mb-1">
              {t('home.featuresTitle')}
            </Text>

            <View className="gap-3">
              <Pressable
                onPress={handleStartPlanning}
                className="active:opacity-70"
              >
                <Card>
                  <CardHeader>
                    <View className="flex-row items-center justify-between">
                      <View className="flex-row items-center gap-3">
                        <View className="w-12 h-12 rounded-full bg-primary/10 items-center justify-center">
                          <Sparkles className="text-primary" size={24} />
                        </View>
                        <View className="flex-1">
                          <CardTitle>{t('home.aiRecommendation')}</CardTitle>
                          <CardDescription className="mt-1">
                            {t('home.aiRecommendationDesc')}
                          </CardDescription>
                        </View>
                      </View>
                      <ArrowRight className="text-muted-foreground" size={20} />
                    </View>
                  </CardHeader>
                </Card>
              </Pressable>

              <Pressable
                onPress={handleStartPlanning}
                className="active:opacity-70"
              >
                <Card>
                  <CardHeader>
                    <View className="flex-row items-center justify-between">
                      <View className="flex-row items-center gap-3">
                        <View className="w-12 h-12 rounded-full bg-primary/10 items-center justify-center">
                          <Clock className="text-primary" size={24} />
                        </View>
                        <View className="flex-1">
                          <CardTitle>{t('home.smartSchedule')}</CardTitle>
                          <CardDescription className="mt-1">
                            {t('home.smartScheduleDesc')}
                          </CardDescription>
                        </View>
                      </View>
                      <ArrowRight className="text-muted-foreground" size={20} />
                    </View>
                  </CardHeader>
                </Card>
              </Pressable>

              <Pressable
                onPress={handleStartPlanning}
                className="active:opacity-70"
              >
                <Card>
                  <CardHeader>
                    <View className="flex-row items-center justify-between">
                      <View className="flex-row items-center gap-3">
                        <View className="w-12 h-12 rounded-full bg-primary/10 items-center justify-center">
                          <TrendingUp className="text-primary" size={24} />
                        </View>
                        <View className="flex-1">
                          <CardTitle>{t('home.realTimeInfo')}</CardTitle>
                          <CardDescription className="mt-1">
                            {t('home.realTimeInfoDesc')}
                          </CardDescription>
                        </View>
                      </View>
                      <ArrowRight className="text-muted-foreground" size={20} />
                    </View>
                  </CardHeader>
                </Card>
              </Pressable>

              <Pressable
                onPress={handleStartPlanning}
                className="active:opacity-70"
              >
                <Card>
                  <CardHeader>
                    <View className="flex-row items-center justify-between">
                      <View className="flex-row items-center gap-3">
                        <View className="w-12 h-12 rounded-full bg-primary/10 items-center justify-center">
                          <MapPin className="text-primary" size={24} />
                        </View>
                        <View className="flex-1">
                          <CardTitle>{t('home.spotGuide')}</CardTitle>
                          <CardDescription className="mt-1">
                            {t('home.spotGuideDesc')}
                          </CardDescription>
                        </View>
                      </View>
                      <ArrowRight className="text-muted-foreground" size={20} />
                    </View>
                  </CardHeader>
                </Card>
              </Pressable>
            </View>
          </View>

          {/* Bottom spacing */}
          <View className="h-8" />
        </View>
      </ScrollView>
    </View>
  );
}
