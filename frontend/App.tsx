import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { RootNavigator } from '@/navigation';
import { SettingsProvider } from '@/contexts';
import '@/i18n';
import './global.css';

export default function App() {
  return (
    <SafeAreaProvider>
      <SettingsProvider>
        <NavigationContainer>
          <RootNavigator />
        </NavigationContainer>
      </SettingsProvider>
    </SafeAreaProvider>
  );
}
