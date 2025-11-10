import React from 'react';
import { View, ScrollView, Pressable, Alert, Switch } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { useTranslation } from 'react-i18next';
import { useSettings } from '@/contexts';
import { SUPPORTED_LANGUAGES, type LanguageCode } from '@/i18n';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  Text,
  Separator,
} from '@/components/ui';
import {
  User,
  Bell,
  Globe,
  Palette,
  Shield,
  HelpCircle,
  Info,
  LogOut,
  ChevronRight,
} from '@/lib/icons';

interface SettingItemProps {
  icon: React.ComponentType<{ size?: number; className?: string }>;
  title: string;
  description?: string;
  onPress?: () => void;
  showChevron?: boolean;
  rightElement?: React.ReactNode;
}

function SettingItem({
  icon: Icon,
  title,
  description,
  onPress,
  showChevron = true,
  rightElement,
}: SettingItemProps) {
  const content = (
    <View className="flex-row items-center justify-between py-4">
      <View className="flex-row items-center gap-3 flex-1">
        <View className="w-10 h-10 rounded-full bg-primary/10 items-center justify-center">
          <Icon className="text-primary" size={20} />
        </View>
        <View className="flex-1">
          <Text className="text-base font-medium text-foreground">{title}</Text>
          {description && (
            <Text className="text-sm text-muted-foreground mt-0.5">
              {description}
            </Text>
          )}
        </View>
      </View>
      {rightElement || (showChevron && <ChevronRight className="text-muted-foreground" size={20} />)}
    </View>
  );

  if (onPress) {
    return (
      <Pressable onPress={onPress} className="active:opacity-70">
        {content}
      </Pressable>
    );
  }

  return content;
}

export function SettingsScreen() {
  const { t } = useTranslation();
  const { preferences, setLanguage, setTheme, setNotifications } = useSettings();
  const [showLanguageOptions, setShowLanguageOptions] = React.useState(false);

  const handleLanguageChange = async (code: LanguageCode) => {
    await setLanguage(code);
    setShowLanguageOptions(false);
    Alert.alert(
      t('settings.languageChanged'),
      t('settings.languageChangedDesc')
    );
  };

  const handleThemePress = () => {
    Alert.alert(
      t('settings.theme'),
      '',
      [
        {
          text: t('settings.themeLight'),
          onPress: () => setTheme('light'),
          style: preferences.theme === 'light' ? 'default' : 'cancel',
        },
        {
          text: t('settings.themeDark'),
          onPress: () => setTheme('dark'),
          style: preferences.theme === 'dark' ? 'default' : 'cancel',
        },
        {
          text: t('common.cancel'),
          style: 'cancel',
        },
      ]
    );
  };

  const handleProfilePress = () => {
    Alert.alert(t('settings.profile'), t('settings.featureComingSoon'));
  };

  const handleNotificationPress = () => {
    Alert.alert(t('settings.notifications'), t('settings.featureComingSoon'));
  };

  const handlePrivacyPress = () => {
    Alert.alert(t('settings.privacy'), t('settings.featureComingSoon'));
  };

  const handleHelpPress = () => {
    Alert.alert(t('settings.help'), t('settings.featureComingSoon'));
  };

  const handleAboutPress = () => {
    Alert.alert(t('settings.about'), 'Seoul AI Travel Planner v1.0.0');
  };

  const handleLogoutPress = () => {
    Alert.alert(t('settings.logout'), t('settings.logoutConfirm'), [
      { text: t('common.cancel'), style: 'cancel' },
      { text: t('settings.logout'), style: 'destructive' },
    ]);
  };

  const currentLanguageName = SUPPORTED_LANGUAGES[preferences.language];
  const currentThemeName = preferences.theme === 'light'
    ? t('settings.themeLight')
    : preferences.theme === 'dark'
    ? t('settings.themeDark')
    : 'System';

  return (
    <View className="flex-1 bg-background">
      <StatusBar style="auto" />

      <ScrollView className="flex-1">
        <View className="p-6 pt-12 gap-6">
          {/* Header */}
          <View className="gap-2">
            <Text className="text-4xl font-bold text-foreground">
              {t('settings.title')}
            </Text>
            <Text className="text-base text-muted-foreground">
              {t('settings.description')}
            </Text>
          </View>

          {/* Account Section */}
          <Card>
            <CardHeader>
              <CardTitle>{t('settings.account')}</CardTitle>
            </CardHeader>
            <CardContent className="gap-0">
              <SettingItem
                icon={User}
                title={t('settings.profile')}
                description={t('settings.profileDesc')}
                onPress={handleProfilePress}
              />
              <Separator />
              <SettingItem
                icon={Bell}
                title={t('settings.notifications')}
                description={t('settings.notificationsDesc')}
                onPress={handleNotificationPress}
              />
            </CardContent>
          </Card>

          {/* Preferences Section */}
          <Card>
            <CardHeader>
              <CardTitle>{t('settings.preferences')}</CardTitle>
            </CardHeader>
            <CardContent className="gap-0">
              <SettingItem
                icon={Globe}
                title={t('settings.language')}
                description={currentLanguageName}
                onPress={() => setShowLanguageOptions(!showLanguageOptions)}
              />

              {showLanguageOptions && (
                <View className="pl-14 pr-4 pb-3 gap-2">
                  {Object.entries(SUPPORTED_LANGUAGES).map(([code, name]) => (
                    <Pressable
                      key={code}
                      onPress={() => handleLanguageChange(code as LanguageCode)}
                      className="active:opacity-70"
                    >
                      <View className="flex-row items-center justify-between py-2 px-3 rounded-lg bg-muted/30">
                        <Text className="text-base text-foreground">{name}</Text>
                        {preferences.language === code && (
                          <View className="w-5 h-5 rounded-full bg-primary items-center justify-center">
                            <Text className="text-xs text-primary-foreground">✓</Text>
                          </View>
                        )}
                      </View>
                    </Pressable>
                  ))}
                </View>
              )}

              <Separator />
              <SettingItem
                icon={Palette}
                title={t('settings.theme')}
                description={currentThemeName}
                onPress={handleThemePress}
              />
            </CardContent>
          </Card>

          {/* Notifications Preferences */}
          <Card>
            <CardHeader>
              <CardTitle>{t('settings.notifications')}</CardTitle>
              <CardDescription>
                Customize your notification preferences
              </CardDescription>
            </CardHeader>
            <CardContent className="gap-0">
              <SettingItem
                icon={Bell}
                title="Trip Reminders"
                description="Get reminded about upcoming trips"
                showChevron={false}
                rightElement={
                  <Switch
                    value={preferences.notifications.tripReminders}
                    onValueChange={(value) =>
                      setNotifications({
                        ...preferences.notifications,
                        tripReminders: value,
                      })
                    }
                  />
                }
              />
              <Separator />
              <SettingItem
                icon={Bell}
                title="Recommendations"
                description="Receive personalized travel suggestions"
                showChevron={false}
                rightElement={
                  <Switch
                    value={preferences.notifications.recommendations}
                    onValueChange={(value) =>
                      setNotifications({
                        ...preferences.notifications,
                        recommendations: value,
                      })
                    }
                  />
                }
              />
            </CardContent>
          </Card>

          {/* Support Section */}
          <Card>
            <CardHeader>
              <CardTitle>{t('settings.support')}</CardTitle>
            </CardHeader>
            <CardContent className="gap-0">
              <SettingItem
                icon={Shield}
                title={t('settings.privacy')}
                onPress={handlePrivacyPress}
              />
              <Separator />
              <SettingItem
                icon={HelpCircle}
                title={t('settings.help')}
                onPress={handleHelpPress}
              />
              <Separator />
              <SettingItem
                icon={Info}
                title={t('settings.about')}
                description={t('settings.version')}
                onPress={handleAboutPress}
              />
            </CardContent>
          </Card>

          {/* Logout */}
          <Pressable onPress={handleLogoutPress} className="active:opacity-70">
            <Card className="border-destructive/20">
              <CardContent className="py-4">
                <View className="flex-row items-center justify-center gap-2">
                  <LogOut className="text-destructive" size={20} />
                  <Text className="text-base font-medium text-destructive">
                    {t('settings.logout')}
                  </Text>
                </View>
              </CardContent>
            </Card>
          </Pressable>

          {/* Bottom spacing */}
          <View className="h-8" />
        </View>
      </ScrollView>
    </View>
  );
}
