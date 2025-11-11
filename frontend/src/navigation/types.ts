import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import type { BottomTabScreenProps as RNBottomTabScreenProps } from '@react-navigation/bottom-tabs';
import type { CompositeScreenProps } from '@react-navigation/native';
import { TravelPlan } from '@/types';

// Bottom Tab Navigator
export type BottomTabParamList = {
  HomeTab: undefined;
  MyPlans: undefined;
  Settings: undefined;
};

// Root Stack Navigator
export type RootStackParamList = {
  MainTabs: undefined;
  PlanInput: undefined;
  PlanViewer: {
    plan: TravelPlan;
  };
};

// Screen Props Types
export type RootStackScreenProps<T extends keyof RootStackParamList> =
  NativeStackScreenProps<RootStackParamList, T>;

export type BottomTabScreenProps<T extends keyof BottomTabParamList> =
  CompositeScreenProps<
    RNBottomTabScreenProps<BottomTabParamList, T>,
    NativeStackScreenProps<RootStackParamList>
  >;

declare global {
  namespace ReactNavigation {
    interface RootParamList extends RootStackParamList {}
  }
}
