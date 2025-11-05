import React, { useState } from 'react';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { ChatProvider } from '@/contexts/ChatContext';
import { HomeScreen, ChatScreen, ConversationListScreen } from '@/screens';
import './global.css';

type Screen = 'home' | 'conversations' | 'chat';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('home');
  const [selectedConversationId, setSelectedConversationId] = useState<
    string | undefined
  >();

  const handleStartChat = () => {
    setSelectedConversationId(undefined);
    setCurrentScreen('chat');
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

  const handlePlanGenerated = (planId: string) => {
    console.log('Travel plan generated:', planId);
    // TODO: Navigate to plan screen
  };

  return (
    <SafeAreaProvider>
      <ChatProvider>
        {currentScreen === 'home' && (
          <HomeScreen
            onStartChat={handleStartChat}
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
            onPlanGenerated={handlePlanGenerated}
          />
        )}
      </ChatProvider>
    </SafeAreaProvider>
  );
}
