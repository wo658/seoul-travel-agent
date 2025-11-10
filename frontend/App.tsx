import React, { useState } from 'react';
import { Alert } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import {
  HomeScreen,
  TravelPlanInputScreen,
  PlanViewerDemoScreen,
} from '@/screens';
import { GeneratePlanApiResponse, TravelPlan } from '@/types';
import './global.css';

type Screen = 'home' | 'planInput' | 'planViewer';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('home');
  const [currentPlan, setCurrentPlan] = useState<TravelPlan | null>(null);

  console.log('[App] Current screen:', currentScreen);

  const handleStartPlanning = () => {
    console.log('[App] Navigating to plan input screen');
    setCurrentScreen('planInput');
  };

  const handleBackToHome = () => {
    setCurrentScreen('home');
  };

  const handleBackToPlanInput = () => {
    setCurrentScreen('planInput');
  };

  const handlePlanGenerated = (response: GeneratePlanApiResponse) => {
    console.log('[App] Plan generated:', response);
    setCurrentPlan(response.plan);
    setCurrentScreen('planViewer');
  };

  const handleSavePlan = (plan: TravelPlan) => {
    console.log('[App] Saving plan:', plan);
    // TODO: Implement plan saving to backend
    Alert.alert('성공', '계획이 저장되었습니다!', [
      { text: '확인', onPress: () => setCurrentScreen('home') }
    ]);
  };

  return (
    <SafeAreaProvider>
      {currentScreen === 'home' && (
        <HomeScreen onStartPlanning={handleStartPlanning} />
      )}

      {currentScreen === 'planInput' && (
        <TravelPlanInputScreen
          onPlanGenerated={handlePlanGenerated}
          onBack={handleBackToHome}
        />
      )}

      {currentScreen === 'planViewer' && currentPlan && (
        <PlanViewerDemoScreen
          plan={currentPlan}
          onBack={handleBackToPlanInput}
          onSave={handleSavePlan}
        />
      )}
    </SafeAreaProvider>
  );
}
