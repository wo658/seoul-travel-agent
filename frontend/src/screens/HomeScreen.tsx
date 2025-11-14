import React from 'react';
import { View, ImageBackground, StyleSheet, Pressable } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { useNavigation } from '@react-navigation/native';
import { useTranslation } from 'react-i18next';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import {
  Button,
  Text,
} from '@/components/ui';
import { Sparkles, Calendar, Settings } from '@/lib/icons/';
import type { RootStackScreenProps } from '@/navigation';

export function HomeScreen() {
  const navigation = useNavigation<RootStackScreenProps<'Home'>['navigation']>();
  const { t } = useTranslation();
  const insets = useSafeAreaInsets();

  const handleStartPlanning = () => {
    navigation.navigate('PlanInput');
  };

  return (
    <View className="flex-1">
      <StatusBar style="light" />

      <ImageBackground
        source={{ uri: 'https://images.unsplash.com/photo-1583417319070-4a69db38a482?q=80&w=2940&auto=format&fit=crop' }}
        style={styles.background}
        resizeMode="cover"
      >
        {/* Dark overlay gradient */}
        <LinearGradient
          colors={['rgba(0,0,0,0.6)', 'rgba(0,0,0,0.3)', 'rgba(0,0,0,0.7)']}
          style={styles.gradient}
        >
          <View className="flex-1 justify-center items-center px-6">
            {/* Hero Content */}
            <View className="items-center gap-6 max-w-2xl mb-32">
              {/* Icon */}
              <View className="w-20 h-20 rounded-full bg-white/10 backdrop-blur-xl items-center justify-center border border-white/20">
                <Sparkles className="text-white" size={40} />
              </View>

              {/* Title */}
              <View className="items-center gap-3">
                <Text className="text-5xl font-bold text-white text-center leading-tight">
                  {t('home.title')}
                </Text>
                <Text className="text-3xl font-semibold text-white/90 text-center">
                  {t('home.subtitle')}
                </Text>
              </View>

              {/* Description */}
              <Text className="text-lg text-white/80 text-center leading-relaxed max-w-md">
                {t('home.description')}
              </Text>

              {/* CTA Button */}
              <Button
                size="lg"
                onPress={handleStartPlanning}
                className="mt-4 bg-white shadow-2xl min-w-64"
              >
                <View className="flex-row items-center gap-3 px-4">
                  <Sparkles className="text-primary" size={24} />
                  <Text className="text-lg font-semibold text-primary">
                    {t('home.createPlan')}
                  </Text>
                </View>
              </Button>

              {/* Subtitle under button */}
              <Text className="text-sm text-white/60 text-center mt-2">
                {t('home.ctaDescription')}
              </Text>
            </View>
          </View>

          {/* Bottom Quick Actions */}
          <View
            style={{ paddingBottom: insets.bottom + 24 }}
            className="px-6"
          >
            <View className="flex-row justify-center gap-6">
              {/* My Plans */}
              <Pressable
                onPress={() => navigation.navigate('MyPlans')}
                className="active:opacity-70"
              >
                <View className="items-center gap-2">
                  <View className="w-14 h-14 rounded-full bg-white/10 backdrop-blur-xl items-center justify-center border border-white/20">
                    <Calendar className="text-white" size={24} />
                  </View>
                  <Text className="text-xs text-white/80 font-medium">
                    {t('navigation.myPlans')}
                  </Text>
                </View>
              </Pressable>

              {/* Settings */}
              <Pressable
                onPress={() => navigation.navigate('Settings')}
                className="active:opacity-70"
              >
                <View className="items-center gap-2">
                  <View className="w-14 h-14 rounded-full bg-white/10 backdrop-blur-xl items-center justify-center border border-white/20">
                    <Settings className="text-white" size={24} />
                  </View>
                  <Text className="text-xs text-white/80 font-medium">
                    {t('navigation.settings')}
                  </Text>
                </View>
              </Pressable>
            </View>
          </View>
        </LinearGradient>
      </ImageBackground>
    </View>
  );
}

const styles = StyleSheet.create({
  background: {
    flex: 1,
    width: '100%',
    height: '100%',
  },
  gradient: {
    flex: 1,
    width: '100%',
    height: '100%',
  },
});
