import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { HomeScreen } from '@/screens/HomeScreen';
import { MyPlansScreen } from '@/screens/MyPlansScreen';
import { SettingsScreen } from '@/screens/SettingsScreen';
import { TravelPlanInputScreen } from '@/screens/TravelPlanInputScreen';
import { PlanViewerDemoScreen } from '@/screens/PlanViewerDemoScreen';
import type { RootStackParamList } from './types';

const Stack = createNativeStackNavigator<RootStackParamList>();

export function RootNavigator() {
  return (
    <Stack.Navigator
      initialRouteName="Home"
      screenOptions={{
        headerShown: false,
        animation: 'slide_from_right',
      }}
    >
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="MyPlans" component={MyPlansScreen} />
      <Stack.Screen name="Settings" component={SettingsScreen} />
      <Stack.Screen name="PlanInput" component={TravelPlanInputScreen} />
      <Stack.Screen name="PlanViewer" component={PlanViewerDemoScreen} />
    </Stack.Navigator>
  );
}

export * from './types';
