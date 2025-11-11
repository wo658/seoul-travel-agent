import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import { en, ko, zh } from './translations';

export const SUPPORTED_LANGUAGES = {
  en: 'English',
  ko: '한국어',
  zh: '中文',
} as const;

export type LanguageCode = keyof typeof SUPPORTED_LANGUAGES;

const resources = {
  en: { translation: en },
  ko: { translation: ko },
  zh: { translation: zh },
};

i18n.use(initReactI18next).init({
  resources,
  lng: 'ko', // Default language
  fallbackLng: 'en',
  compatibilityJSON: 'v4',
  interpolation: {
    escapeValue: false,
  },
});

export default i18n;
