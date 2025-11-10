import React from 'react';
import { View, ScrollView, Pressable, Alert } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RouteProp } from '@react-navigation/native';
import { PlanSummary, PlanTimeline } from '@/components/travel';
import { ScreenHeader } from '@/components/navigation';
import { Save, MoreVertical } from '@/lib/icons';
import type { RootStackParamList } from '@/navigation';

/**
 * 여행 계획 뷰어 화면
 * 생성된 여행 계획을 확인하고 저장할 수 있습니다.
 */

type PlanViewerDemoScreenNavigationProp = NativeStackNavigationProp<
  RootStackParamList,
  'PlanViewer'
>;

type PlanViewerDemoScreenRouteProp = RouteProp<RootStackParamList, 'PlanViewer'>;

export function PlanViewerDemoScreen() {
  const navigation = useNavigation<PlanViewerDemoScreenNavigationProp>();
  const route = useRoute<PlanViewerDemoScreenRouteProp>();
  const { plan } = route.params;

  const handleSave = () => {
    // TODO: Implement plan saving to backend
    Alert.alert('성공', '계획이 저장되었습니다!', [
      {
        text: '확인',
        onPress: () => navigation.navigate('Home'),
      },
    ]);
  };

  const handleMoreOptions = () => {
    // TODO: Implement more options menu
    Alert.alert('더보기', '추가 옵션이 곧 제공됩니다.');
  };

  return (
    <View className="flex-1 bg-background">
      <ScreenHeader
        title="여행 계획"
        rightIcon={MoreVertical}
        onRightPress={handleMoreOptions}
      />

      {/* Content */}
      <ScrollView className="flex-1">
        <View className="p-4 gap-4">
          {/* Summary */}
          <PlanSummary plan={plan} />

          {/* Timeline */}
          <PlanTimeline days={plan.days} />
        </View>

        {/* Bottom padding */}
        <View className="h-24" />
      </ScrollView>

      {/* Save Button */}
      <View className="absolute bottom-6 right-4">
        <Pressable
          onPress={handleSave}
          className="w-14 h-14 rounded-full bg-primary items-center justify-center shadow-lg active:scale-95"
        >
          <Save size={24} className="text-primary-foreground" />
        </Pressable>
      </View>
    </View>
  );
}
