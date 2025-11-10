import React, { createContext, useContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useTranslation } from 'react-i18next';
import type { LanguageCode } from '@/i18n';

interface UserPreferences {
  language: LanguageCode;
  theme: 'light' | 'dark' | 'system';
  notifications: {
    enabled: boolean;
    tripReminders: boolean;
    recommendations: boolean;
  };
}

interface SettingsContextType {
  preferences: UserPreferences;
  setLanguage: (language: LanguageCode) => Promise<void>;
  setTheme: (theme: UserPreferences['theme']) => Promise<void>;
  setNotifications: (notifications: UserPreferences['notifications']) => Promise<void>;
  isLoading: boolean;
}

const DEFAULT_PREFERENCES: UserPreferences = {
  language: 'ko',
  theme: 'light',
  notifications: {
    enabled: true,
    tripReminders: true,
    recommendations: true,
  },
};

const STORAGE_KEY = '@user_preferences';

const SettingsContext = createContext<SettingsContextType | undefined>(undefined);

export function SettingsProvider({ children }: { children: React.ReactNode }) {
  const { i18n } = useTranslation();
  const [preferences, setPreferences] = useState<UserPreferences>(DEFAULT_PREFERENCES);
  const [isLoading, setIsLoading] = useState(true);

  // Load preferences from storage
  useEffect(() => {
    loadPreferences();
  }, []);

  const loadPreferences = async () => {
    try {
      const stored = await AsyncStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored) as UserPreferences;
        setPreferences(parsed);
        await i18n.changeLanguage(parsed.language);
      }
    } catch (error) {
      console.error('Failed to load preferences:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const savePreferences = async (newPreferences: UserPreferences) => {
    try {
      await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(newPreferences));
      setPreferences(newPreferences);
    } catch (error) {
      console.error('Failed to save preferences:', error);
      throw error;
    }
  };

  const setLanguage = async (language: LanguageCode) => {
    await i18n.changeLanguage(language);
    await savePreferences({ ...preferences, language });
  };

  const setTheme = async (theme: UserPreferences['theme']) => {
    await savePreferences({ ...preferences, theme });
  };

  const setNotifications = async (notifications: UserPreferences['notifications']) => {
    await savePreferences({ ...preferences, notifications });
  };

  return (
    <SettingsContext.Provider
      value={{
        preferences,
        setLanguage,
        setTheme,
        setNotifications,
        isLoading,
      }}
    >
      {children}
    </SettingsContext.Provider>
  );
}

export function useSettings() {
  const context = useContext(SettingsContext);
  if (context === undefined) {
    throw new Error('useSettings must be used within a SettingsProvider');
  }
  return context;
}
