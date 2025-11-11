import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { useTranslation } from 'react-i18next';
import { Platform, View } from 'react-native';
import { HomeScreen } from '@/screens/HomeScreen';
import { MyPlansScreen } from '@/screens/MyPlansScreen';
import { SettingsScreen } from '@/screens/SettingsScreen';
import { TravelPlanInputScreen } from '@/screens/TravelPlanInputScreen';
import { PlanViewerDemoScreen } from '@/screens/PlanViewerDemoScreen';
import { Home, Calendar, Settings } from '@/lib/icons';
import { Text } from '@/components/ui';
import type { RootStackParamList, BottomTabParamList } from './types';

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<BottomTabParamList>();

function BottomTabNavigator() {
  const { t } = useTranslation();

  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: 'hsl(var(--primary))',
        tabBarInactiveTintColor: 'hsl(var(--muted-foreground))',
        tabBarStyle: {
          backgroundColor: 'hsl(var(--card))',
          borderTopColor: 'hsl(var(--border))',
          borderTopWidth: 1,
          height: Platform.select({ web: 70, default: 65 }),
          paddingBottom: Platform.select({ web: 8, default: 8 }),
          paddingTop: Platform.select({ web: 8, default: 8 }),
        },
        tabBarShowLabel: true,
      }}
    >
      <Tab.Screen
        name="HomeTab"
        component={HomeScreen}
        options={{
          tabBarIcon: ({ color, focused }) => (
            <View className="items-center justify-center">
              <Home
                color={color}
                size={24}
                style={{ transform: [{ scale: focused ? 1.05 : 1 }] }}
              />
            </View>
          ),
          tabBarLabel: ({ focused }) => (
            <Text
              className={`text-xs ${focused ? 'font-semibold' : 'font-normal'}`}
              style={{ color: focused ? 'hsl(var(--primary))' : 'hsl(var(--muted-foreground))' }}
            >
              {t('navigation.home')}
            </Text>
          ),
        }}
      />
      <Tab.Screen
        name="MyPlans"
        component={MyPlansScreen}
        options={{
          tabBarIcon: ({ color, focused }) => (
            <View className="items-center justify-center">
              <Calendar
                color={color}
                size={24}
                style={{ transform: [{ scale: focused ? 1.05 : 1 }] }}
              />
            </View>
          ),
          tabBarLabel: ({ focused }) => (
            <Text
              className={`text-xs ${focused ? 'font-semibold' : 'font-normal'}`}
              style={{ color: focused ? 'hsl(var(--primary))' : 'hsl(var(--muted-foreground))' }}
            >
              {t('navigation.myPlans')}
            </Text>
          ),
        }}
      />
      <Tab.Screen
        name="Settings"
        component={SettingsScreen}
        options={{
          tabBarIcon: ({ color, focused }) => (
            <View className="items-center justify-center">
              <Settings
                color={color}
                size={24}
                style={{ transform: [{ scale: focused ? 1.05 : 1 }] }}
              />
            </View>
          ),
          tabBarLabel: ({ focused }) => (
            <Text
              className={`text-xs ${focused ? 'font-semibold' : 'font-normal'}`}
              style={{ color: focused ? 'hsl(var(--primary))' : 'hsl(var(--muted-foreground))' }}
            >
              {t('navigation.settings')}
            </Text>
          ),
        }}
      />
    </Tab.Navigator>
  );
}

export function RootNavigator() {
  return (
    <Stack.Navigator
      initialRouteName="MainTabs"
      screenOptions={{
        headerShown: false,
        animation: 'slide_from_right',
      }}
    >
      <Stack.Screen name="MainTabs" component={BottomTabNavigator} />
      <Stack.Screen name="PlanInput" component={TravelPlanInputScreen} />
      <Stack.Screen name="PlanViewer" component={PlanViewerDemoScreen} />
    </Stack.Navigator>
  );
}

export * from './types';
