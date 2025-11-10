# Internationalization (i18n) Implementation Guide

## Overview

This project now supports multiple languages:
- 🇰🇷 Korean (한국어) - Default
- 🇺🇸 English
- 🇨🇳 Chinese (中文)

## Structure

```
src/
├── i18n/
│   ├── config.ts           # i18n configuration
│   ├── index.ts            # Exports
│   └── translations/
│       ├── en.ts           # English translations
│       ├── ko.ts           # Korean translations
│       ├── zh.ts           # Chinese translations
│       └── index.ts
├── contexts/
│   └── SettingsContext.tsx # User preferences & language state
```

## Usage

### 1. In Functional Components

```tsx
import { useTranslation } from 'react-i18next';

export function MyComponent() {
  const { t } = useTranslation();

  return (
    <Text>{t('home.title')}</Text>
  );
}
```

### 2. Accessing Settings Context

```tsx
import { useSettings } from '@/contexts';

export function MyComponent() {
  const { preferences, setLanguage } = useSettings();

  const changeLanguage = async () => {
    await setLanguage('en'); // 'en' | 'ko' | 'zh'
  };

  return (
    <Text>Current language: {preferences.language}</Text>
  );
}
```

### 3. Adding New Translations

1. Add keys to `src/i18n/translations/en.ts` (source of truth)
2. Add corresponding translations to `ko.ts` and `zh.ts`
3. TypeScript will ensure type safety across all languages

Example:
```typescript
// en.ts
export const en = {
  myFeature: {
    title: 'My Feature',
    description: 'Feature description',
  },
};

// ko.ts
export const ko: TranslationKeys = {
  myFeature: {
    title: '내 기능',
    description: '기능 설명',
  },
};

// zh.ts
export const zh: TranslationKeys = {
  myFeature: {
    title: '我的功能',
    description: '功能描述',
  },
};
```

## Available Translation Keys

See `src/i18n/translations/en.ts` for the complete list of available keys.

Key categories:
- `common.*` - Common UI elements (buttons, labels, etc.)
- `navigation.*` - Navigation labels
- `home.*` - Home screen
- `myPlans.*` - My Plans screen
- `settings.*` - Settings screen
- `planInput.*` - Plan input form
- `planViewer.*` - Plan viewer

## Settings Features

The app includes comprehensive settings:

### Language Settings
- Switch between Korean, English, and Chinese
- Persisted across sessions using AsyncStorage
- Immediate UI update on language change

### Theme Settings
- Light/Dark mode support
- System theme detection (planned)

### Notification Preferences
- Trip reminders toggle
- Recommendations toggle
- Granular control over notification types

## Implementation Checklist

When adding i18n to a screen:

- [ ] Import `useTranslation` hook
- [ ] Replace hardcoded strings with `t('key')` calls
- [ ] Add translation keys to all three language files
- [ ] Test language switching
- [ ] Verify layout works in all languages (especially Chinese which can be longer)

## Best Practices

1. **Never hardcode user-facing text** - Always use translation keys
2. **Keep keys organized** - Group related translations together
3. **Use descriptive key names** - `home.ctaTitle` instead of `home.text1`
4. **Consider text length** - Chinese/English text may be longer than Korean
5. **Test all languages** - Verify UI doesn't break with different text lengths
6. **Use proper pluralization** - i18next supports plural forms
7. **Format dates/numbers** - Use locale-aware formatting

## Examples

### Simple Text
```tsx
<Text>{t('common.loading')}</Text>
```

### With Variables
```tsx
// Translation: "Welcome, {{name}}!"
<Text>{t('common.welcome', { name: userName })}</Text>
```

### Pluralization
```tsx
// Translation: "{{count}} item" / "{{count}} items"
<Text>{t('common.itemCount', { count: items.length })}</Text>
```

## Troubleshooting

**Language not changing?**
- Check that `SettingsProvider` wraps your app in `App.tsx`
- Verify `i18n` is imported before components load

**Missing translations?**
- Check console for i18n warnings
- Ensure all language files have the same keys
- TypeScript will catch missing keys at compile time

**AsyncStorage errors?**
- Ensure `@react-native-async-storage/async-storage` is installed
- Check that storage permissions are granted (mobile apps)

## Future Enhancements

- [ ] RTL language support (Arabic, Hebrew)
- [ ] Dynamic translation loading (reduce bundle size)
- [ ] Translation management platform integration
- [ ] Automatic missing translation detection in CI/CD
- [ ] Context-aware translations based on user location
