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
import type { RootStackScreenProps } from '@/navigation';

export function HomeScreen() {
  const navigation = useNavigation<RootStackScreenProps<'Home'>['navigation']>();
  const { t } = useTranslation();
  const insets = useSafeAreaInsets();

  const handleStartPlanning = () => {
    navigation.navigate('PlanInput');
  };

  const handleMyPlans = () => {
    navigation.navigate('MyPlans');
  };

  const handleLogin = () => {
    // TODO: Navigate to login screen
    console.log('Login pressed');
  };

  return (
    <View className="flex-1">
      <StatusBar style="light" />

      <ImageBackground
        source={{ uri: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBnGBlbY0jLP9IMEnNeZEoJQBCnTQUP9OHLFoDXNqyVB7QSKEm2Jq6ZfAtUYC9W5TWSW67SWkox5jpx4QeW5XxR4pnMCWQerwFP1dVInOch8MVRpuU4Mx9QVBFfHegomV67AgHfCDGiUgYxfHwFjoKIZS3nFm9tuuy1xI37P22rakroBocxG0NbYrxLY0WnnSMRTU0SZzDFa5LzKFA6owxat8wuMkP_fUj-HKk23_v1jXLwKCxBj1nzmbA9BScmnAQfuLEuIpZcA_k' }}
        style={styles.background}
        resizeMode="cover"
      >
        {/* Gradient overlay matching the HTML design */}
        <LinearGradient
          colors={['rgba(0,0,0,0.6)', 'rgba(0,0,0,0.1)', 'rgba(0,0,0,0.6)']}
          style={styles.gradient}
        >
          <View className="flex-1 flex-col p-4">
            {/* Header */}
            <View style={{ paddingTop: insets.top + 16 }} className="flex-shrink-0">
              <Text className="text-white text-[28px] font-bold leading-tight">
                {t('home.title')}
              </Text>
            </View>

            {/* Main Content - Centered */}
            <View className="flex-1 flex-col justify-end pb-4">
              <Text className="text-white text-[32px] font-bold leading-tight px-4 text-center">
                {t('home.subtitle')}
              </Text>
              <Text className="text-white/90 text-base font-normal leading-normal pt-2 px-4 text-center">
                {t('home.description')}
              </Text>
            </View>

            {/* Footer */}
            <View style={{ paddingBottom: insets.bottom + 16 }} className="flex-shrink-0">
              <View className="px-4 py-3 gap-3">
                <Button
                  size="lg"
                  onPress={handleStartPlanning}
                  className="bg-primary h-12 rounded-lg"
                >
                  <Text className="text-white text-base font-bold tracking-wide">
                    {t('home.createPlan')}
                  </Text>
                </Button>

                <Button
                  size="lg"
                  onPress={handleMyPlans}
                  className="bg-white/95 h-12 rounded-lg"
                >
                  <Text className="text-primary text-base font-bold tracking-wide">
                    {t('navigation.myPlans')}
                  </Text>
                </Button>
              </View>

              <Pressable onPress={handleLogin} className="active:opacity-70">
                <Text className="text-white/90 text-sm font-normal leading-normal pt-1 px-4 text-center underline">
                  {t('settings.comingSoon')}
                </Text>
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
