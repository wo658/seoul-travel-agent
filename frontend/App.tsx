import React, { useState } from 'react';
import { Alert } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { ChatProvider } from '@/contexts/ChatContext';
import {
  HomeScreen,
  ChatScreen,
  ConversationListScreen,
  TravelPlanInputScreen,
  PlanReviewScreen,
} from '@/screens';
import { GeneratePlanApiResponse, TravelPlan } from '@/types';
import './global.css';

type Screen = 'home' | 'conversations' | 'chat' | 'planInput' | 'planReview';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('home');
  const [selectedConversationId, setSelectedConversationId] = useState<
    string | undefined
  >();
  const [currentPlan, setCurrentPlan] = useState<TravelPlan | null>(null);

  const handleStartChat = () => {
    setSelectedConversationId(undefined);
    setCurrentScreen('chat');
  };

  const handleStartPlanning = () => {
    setCurrentScreen('planInput');
  };

  const handleViewConversations = () => {
    setCurrentScreen('conversations');
  };

  const handleConversationSelect = (id: string) => {
    setSelectedConversationId(id);
    setCurrentScreen('chat');
  };

  const handleBackToHome = () => {
    setCurrentScreen('home');
  };

  const handleBackToConversations = () => {
    setCurrentScreen('conversations');
  };

  const handleBackToPlanInput = () => {
    setCurrentScreen('planInput');
  };

  const handlePlanGenerated = (response: GeneratePlanApiResponse) => {
    setCurrentPlan(response.plan);
    setCurrentScreen('planReview');
  };

  const handleSavePlan = (plan: TravelPlan) => {
    console.log('Saving plan:', plan);
    // TODO: Implement plan saving to backend
    Alert.alert('성공', '계획이 저장되었습니다!');
  };

  const handleRegeneratePlan = () => {
    setCurrentScreen('planInput');
  };

  return (
    <SafeAreaProvider>
      <ChatProvider>
        {currentScreen === 'home' && (
          <HomeScreen
            onStartChat={handleStartChat}
            onStartPlanning={handleStartPlanning}
            onViewConversations={handleViewConversations}
          />
        )}

        {currentScreen === 'conversations' && (
          <ConversationListScreen
            onConversationSelect={handleConversationSelect}
            onNewConversation={handleStartChat}
          />
        )}

        {currentScreen === 'chat' && (
          <ChatScreen
            conversationId={selectedConversationId}
            onBack={handleBackToConversations}
            onPlanGenerated={(planId: string) => {
              console.log('Plan generated:', planId);
              // Legacy handler - not used in new flow
            }}
          />
        )}

        {currentScreen === 'planInput' && (
          <TravelPlanInputScreen
            onPlanGenerated={handlePlanGenerated}
            onBack={handleBackToHome}
          />
        )}

        {currentScreen === 'planReview' && currentPlan && (
          <PlanReviewScreen
            plan={currentPlan}
            onBack={handleBackToPlanInput}
            onSave={handleSavePlan}
            onRegenerate={handleRegeneratePlan}
          />
        )}
      </ChatProvider>
    </SafeAreaProvider>
  );
}
