import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { TravelPlan } from '@/types';

// Root Stack Navigator
export type RootStackParamList = {
  Home: undefined;
  MyPlans: undefined;
  Settings: undefined;
  PlanInput: undefined;
  PlanViewer: {
    plan: TravelPlan;
  };
};

// Screen Props Types
export type RootStackScreenProps<T extends keyof RootStackParamList> =
  NativeStackScreenProps<RootStackParamList, T>;

declare global {
  namespace ReactNavigation {
    interface RootParamList extends RootStackParamList {}
  }
}
